/*----------------------------------------------------------------------*/
/*                                                                      */
/*                               easyio_prim.C                          */
/*                                                                      */
/*      This module contains some procedures which help the input       */
/*      data process for an user program.                               */
/*      Function contained are the following:                           */
/*           - clear_screen : clear a page of the screen                */
/*           - readln       : read the first character ignoring the     */
/*			      remaining input stream until the          */
/*			      following <CR>                            */
/*           - beep         : beeps                                     */
/*           - pausa        : waits the user to press <CR>              */  
/*                                                                      */
/*----------------------------------------------------------------------*/
#include <stdio.h>
#include <stdlib.h>
#include "easyio.h"


void clear_screen() {
//        system("clear");
	return;
	}


char readln() {
	char d = getchar();
	char c = d;
	while (d!='\n')
		d=getchar();
	return (c);
	}


void beep() {
	putchar(7);
	return;
	}


void pausa() {
	fprintf(stdout,"\n\n");
        fprintf(stdout,"     *****   Press <RETURN> to continue   *****");
	readln();
	clear_screen();
	return;
	}
