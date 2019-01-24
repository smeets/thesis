#ifndef _GLOBALS_H
#define _GLOBALS_H

#define MacHead 224 // 272 
#define BlockAckReq 192
#define BlockAck 1216 
#define Service 24
#define ACK	112
#define RTS     160
#define PhyHead 20 // 192  //128
#define Tslot   9  // 20    //50
#define DIFS    34 // 50    //128
#define SIFS    16 // 10 
#define BasicRate 6 // 2

extern	int	R;
extern 	int	Wi[20];
extern 	double	rate;
extern	int	N;
extern	int	A;
extern	int	D;

extern void InputScenario();
extern double solve(int c, int n, int r, int* W);


#endif
