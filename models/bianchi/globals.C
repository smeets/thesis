#include "globals.h"
#include <stdio.h>
#include "easyio.h"
#include <stdlib.h>
#include <math.h>

void InputScenario(){ 

	// initialize global variables asap
N = read_int("competing stations", 10, 1, 500);
int CWmin = read_int("minimum contention window", 32, 2, 2048);
int CWmax = read_int("maximum contention window", 1024, 2, 2048);
R = read_int("retry limit", 7, 0, 20);

Wi[0]=CWmin;
for (int i=1; i<=R; i++) {
	Wi[i]=Wi[i-1]*2;
	if (Wi[i]>CWmax) Wi[i]=CWmax;
	}

fprintf(stderr, "using this sequence of backoff windows: \n");
for (int i=0; i<=R; i++) fprintf(stderr, "wi[%d]=%d\n",i, Wi[i]);

fprintf(stderr, "model:\n");
fprintf(stderr, "\t(1): Bianchi\n");
fprintf(stderr, "\t(2): Ziouva\n");
fprintf(stderr, "\t(3): Xiao\n");
A = read_digit("\t-->",1,1,3);

D = read_int("frame size","bit",8182,1,18300);
rate = read_double("Rate","Mbps", 1, 1, 54.);
}


	// basic functions
double p_tau(double t, int nn) {
	return (1.0 - pow((1.0-t), (nn-1)));
	}

double p_tau_inverse(double pp, int nn) {
	return (1.0 - pow((1.0-pp), 1.0/double(nn-1)));
	}

double tau_p(double pp, int nn, double a, int R, int* Wi) {
	double den=0;
	for(int i=0; i<=R; i++) {
		double average = (Wi[i]-1)/2.;
		den += pow(pp,double(i)) * average/a;
		}
	den *= (1-pp)/(1-pow(pp, double(R+1)));
	if (A==3) den = den - (1-pp)/2.;
	return 1/(den+1);
	}

double solve(int a, int N, int R, int* W){
		// compute p and tau
	double 	p=0;
	double	tau=0;
	double oldp = 0;
	double	err;
	double maxp = p_tau(2.0/double(W[0]+1),N);
	double minp = p_tau(2.0/double(W[R]*2), N);
	do 	{
		oldp = p;
		p = (maxp*0.5+minp*0.5);
		if (p==oldp) {p=0.3*p; minp = 0; maxp = 1;}
		tau = (a!=2) ? tau_p(p, N, 1.0, R, Wi) : tau_p(p, N, 1.0-p, R, Wi);
		err = tau - p_tau_inverse(p, N);
		if (err<0) maxp=p; else minp=p;
		fprintf(stderr, "p:(%f+%f)/2 ", minp, maxp);
		fprintf(stderr, "tau=%f err=%.1e\n", tau, err);
	} while (fabs(err) > 1.0e-08);
	return tau;
}

