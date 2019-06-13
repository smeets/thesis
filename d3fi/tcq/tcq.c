// GPL i guess

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <dlfcn.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <errno.h>

#include "linux/rtnetlink.h"
#include "tc_common.h"
#include "tc_util.h"
#include "utils.h"

#include "namespace.h"

int show_stats;
int show_details;
int show_raw;
int show_graph;
int timestamp;

int batch_mode;
int use_iec;
int force;
bool use_names;
int json;
int color;
int oneline;

static char *conf_file;

struct rtnl_handle rth;

static void *BODY;	/* cached handle dlopen(NULL) */
static struct qdisc_util *qdisc_list;
static struct filter_util *filter_list;


static int print_noqopt(struct qdisc_util *qu, FILE *f,
			struct rtattr *opt)
{
	if (opt && RTA_PAYLOAD(opt))
		fprintf(f, "[Unknown qdisc, optlen=%u] ",
			(unsigned int) RTA_PAYLOAD(opt));
	return 0;
}

static int parse_noqopt(struct qdisc_util *qu, int argc, char **argv,
			struct nlmsghdr *n, const char *dev)
{
	if (argc) {
		fprintf(stderr,
			"Unknown qdisc \"%s\", hence option \"%s\" is unparsable\n",
			qu->id, *argv);
		return -1;
	}
	return 0;
}

static int print_nofopt(struct filter_util *qu, FILE *f, struct rtattr *opt, __u32 fhandle)
{
	if (opt && RTA_PAYLOAD(opt))
		fprintf(f, "fh %08x [Unknown filter, optlen=%u] ",
			fhandle, (unsigned int) RTA_PAYLOAD(opt));
	else if (fhandle)
		fprintf(f, "fh %08x ", fhandle);
	return 0;
}

static int parse_nofopt(struct filter_util *qu, char *fhandle,
			int argc, char **argv, struct nlmsghdr *n)
{
	__u32 handle;

	if (argc) {
		fprintf(stderr,
			"Unknown filter \"%s\", hence option \"%s\" is unparsable\n",
			qu->id, *argv);
		return -1;
	}
	if (fhandle) {
		struct tcmsg *t = NLMSG_DATA(n);

		if (get_u32(&handle, fhandle, 16)) {
			fprintf(stderr, "Unparsable filter ID \"%s\"\n", fhandle);
			return -1;
		}
		t->tcm_handle = handle;
	}
	return 0;
}

struct qdisc_util *get_qdisc_kind(const char *str)
{
	void *dlh;
	char buf[256];
	struct qdisc_util *q;

	for (q = qdisc_list; q; q = q->next)
		if (strcmp(q->id, str) == 0)
			return q;

	snprintf(buf, sizeof(buf), "%s/q_%s.so", get_tc_lib(), str);
	dlh = dlopen(buf, RTLD_LAZY);
	if (!dlh) {
		/* look in current binary, only open once */
		dlh = BODY;
		if (dlh == NULL) {
			dlh = BODY = dlopen(NULL, RTLD_LAZY);
			if (dlh == NULL)
				goto noexist;
		}
	}

	snprintf(buf, sizeof(buf), "%s_qdisc_util", str);
	q = dlsym(dlh, buf);
	if (q == NULL)
		goto noexist;

reg:
	q->next = qdisc_list;
	qdisc_list = q;
	return q;

noexist:
	q = calloc(1, sizeof(*q));
	if (q) {
		q->id = strdup(str);
		q->parse_qopt = parse_noqopt;
		q->print_qopt = print_noqopt;
		goto reg;
	}
	return q;
}


struct filter_util *get_filter_kind(const char *str)
{
	void *dlh;
	char buf[256];
	struct filter_util *q;

	for (q = filter_list; q; q = q->next)
		if (strcmp(q->id, str) == 0)
			return q;

	snprintf(buf, sizeof(buf), "%s/f_%s.so", get_tc_lib(), str);
	dlh = dlopen(buf, RTLD_LAZY);
	if (dlh == NULL) {
		dlh = BODY;
		if (dlh == NULL) {
			dlh = BODY = dlopen(NULL, RTLD_LAZY);
			if (dlh == NULL)
				goto noexist;
		}
	}

	snprintf(buf, sizeof(buf), "%s_filter_util", str);
	q = dlsym(dlh, buf);
	if (q == NULL)
		goto noexist;

reg:
	q->next = filter_list;
	filter_list = q;
	return q;
noexist:
	q = calloc(1, sizeof(*q));
	if (q) {
		strncpy(q->id, str, 15);
		q->parse_fopt = parse_nofopt;
		q->print_fopt = print_nofopt;
		goto reg;
	}
	return q;
}

void dump_stats(FILE* fd, char d[16])
{
	struct tcmsg t;
	
	memset(&t, 0, sizeof(t));
	t.tcm_family = AF_UNSPEC;

	ll_init_map(&rth);

	if (d[0]) {
		if ((t.tcm_ifindex = ll_name_to_index(d)) == 0) {
			fprintf(stderr, "Cannot find device \"%s\"\n", d);
			return;
		}
		// filter_ifindex = t.tcm_ifindex;
	}

	if (rtnl_dump_request(&rth, RTM_GETQDISC, &t, sizeof(t)) < 0) {
		perror("Cannot send dump request");
		return;
	}

	if (rtnl_dump_filter(&rth, print_qdisc, fd) < 0) {
		fprintf(stderr, "Dump terminated\n");
		return;
	}
}

size_t seek_str(char *str, char *what)
{
	char *h1 = str;
	char *h2 = what;
	size_t step = 0;
	bool match = false;

	while (*h1 && *h2) {
		if (*h1 == *h2) {
			match = true;
			h2++;
		} else if (match) {
			h2 = what;
			match = false;
		}

		h1++;
		step++;
	}

	return step;
}

void parse_dump(char *dump, long *sent_pkts, long *bbytes, long *inqueue, long *dropped, long *requeued)
{
	size_t root = seek_str(dump, "qdisc mq 0: dev ");
	size_t sent = seek_str(dump + root, "Sent") - 4;
	size_t backlog = seek_str(dump + root, "backlog") - 7;

	long bytes, olmt;
	
	sscanf(dump + root + sent, 
		"Sent %ld bytes %ld pkt (dropped %ld, overlimits %ld requeues %ld)",
		&bytes, sent_pkts, dropped, &olmt, requeued);
	
	sscanf(dump + root + backlog, 
		"backlog %ldb %ldp requeues %ld",
		bbytes, inqueue, requeued);
}

int main(int argc, char const *argv[])
{
	tc_core_init();

	if (rtnl_open(&rth, 0) < 0) {
		fprintf(stderr, "Cannot open rtnetlink\n");
		return -1;
	}

	argc--; argv++; // remove ./tcq

	++show_stats;
	bool track = false;
	bool avg = false;
	char d[16] = { 0 };

	while (argc > 0) {
		if (strcmp(*argv, "dev") == 0) {
			NEXT_ARG();
			strncpy(d, *argv, sizeof(d)-1);
		} else if (strcmp(*argv, "track") == 0) {
			track = true;
		} else if (strcmp(*argv, "avg") == 0) {
			avg = true;
		} else if (matches(*argv, "help") == 0) {
			// usage();
		} else {
			fprintf(stderr, "What is \"%s\"? Try \"tc qdisc help\".\n", *argv);
			return -1;
		}

		argc--; argv++;
	}

	// dump output into memory-backed file descriptor,
	// then parse values from this memory region.
	char buf[8096] = { 0 };
	FILE *fd = fmemopen(buf, sizeof(buf), "w");
	long sent_pkts, backlog_bytes, backlog_pkts, pkts_dropped, pkts_requeued;
	long samples = 0;
	long prev_sent = 0, prev_pkts = 0;

	if (track)
		fprintf(stderr, "time,");
	fprintf(stderr, "sent,bytes,packets,dropped,requeued\n");
	do {
		dump_stats(fd, d);
		parse_dump(buf, &sent_pkts, &backlog_bytes, &backlog_pkts, &pkts_dropped, &pkts_requeued);
		bool changed = sent_pkts != prev_sent || backlog_pkts != prev_pkts;
		if (track && changed)
			fprintf(stderr, "%ld, ", samples);
		if (changed)
			fprintf(stderr, "%ld, %ld, %ld, %ld, %ld\n", sent_pkts, backlog_bytes, backlog_pkts, pkts_dropped, pkts_requeued);
		rewind(fd);
		if (track) {
			if (changed)
				samples++;
			prev_sent = sent_pkts;
			prev_pkts = backlog_pkts;
		}
	} while (track);

	fclose(fd);
	rtnl_close(&rth);
	return 0;
}

