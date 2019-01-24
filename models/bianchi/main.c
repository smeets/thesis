
#include <stdio.h>
#include <stdlib.h>
#include "globals.h"
#include <math.h>
#include "easyio.h"
#include <iostream>

using namespace std;

int 	A;				// tau rule: Bianchi 1, Ziouva 2 
int	Wi[20];
int 	N;
int 	R;
int     D;
double  rate;

int main(){
	InputScenario();

        double B0 = 1/Wi[0];
	if (A!=3) B0 = 0;
	cout << "A " << A << endl;
	double t = solve(A, N, R, Wi);
	double p = 1 - pow(1-t, N-1);
	double Pidle = pow(1-t, N);
	double PS = N*t*(1-p);
	double Tsucc =  ( 4*ceil((D+MacHead+Service)/(4*rate)) + DIFS + ACK/BasicRate + 2*PhyHead + SIFS + 2)/(1-B0) + Tslot;
	double Tcoll =  4*ceil( (D+MacHead+Service)/(4*rate) ) + DIFS + ACK/BasicRate + 2*PhyHead + SIFS + 1+ Tslot;

// rts-cts
//	double Tcoll =  RTS/BasicRate + DIFS + ACK/BasicRate + 2*PhyHead + SIFS + 1+ Tslot;
//	double Tsucc =  ( (D+MacHead+Service)/rate + DIFS + 2*ACK/BasicRate + 4*PhyHead + 3*SIFS + 4
//			+ RTS/BasicRate )/(1-B0) + Tslot;

	double s = Pidle*Tslot + PS*Tsucc + (1-PS-Pidle)*Tcoll;
	double P = D/(1-B0);
	double thr = PS*P/s;

	double w = 0; double pp = pow(p, R+1);
	for(int i=0; i<R+1; i++)
		w += 1 + (Wi[i]-1)/2;
	double pdrop = t*(1-p)*pp/(1-pp)*w;
	double del = N*(1-pdrop)/thr*P - Tsucc;
	
	cout << "Contending Stations: " << N << ":\n" << "Low level figures: tau " << t << " p " << p << endl;
	cout << "PS " << PS/(1-Pidle) << " Pidle " << Pidle/(1-Pidle) << " Slot " << s << endl;
	cout << "Ts " << Tsucc << " Tc " << Tcoll << " Bk " << Tslot/(1-Pidle) << endl;
	cout << "Confirmed MSDU Traffic: " << thr << endl;
	cout << "Access Delay: " << del << " Pdrop:" << pdrop << " N medio: " << N*(1-pdrop) << endl;

}

                        
	
