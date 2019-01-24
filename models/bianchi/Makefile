CC	      = g++
CFLAGS	      = -g -Wall
LIBFLAG       = -g -Wall
#CFLAGS	      = -O3
#LIBFLAG       = -O3

LIBS          = 

MAKEFILE      = Makefile

OBJS	      = eioprim.o \
		eioscan.o \
		eioread.o \
		globals.o \
		main.o

.C.o:
	$(CC) $(CFLAGS) -c $<

PROGRAM       = dcf

all:		$(PROGRAM)

$(PROGRAM):     $(OBJS) $(LIBS)
		@echo -n "Loading $(PROGRAM) ... "
		@$(CC) $(CFLAGS) $(OBJS) $(LIBS) -o $(PROGRAM) $(LIBFLAG)
		@echo "done"

clean:;		@rm -f $(OBJS) core *.bak

# DO NOT DELETE THIS LINE -- make depend depends on it.
