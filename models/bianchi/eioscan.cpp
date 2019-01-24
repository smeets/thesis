/*----------------------------------------------------------------------*/
/*                                                                      */
/*                               easyio_scan.C                          */
/*                                                                      */
/*                                                                      */
/*      This module contains procedures similar to the scanf() function:*/
/*      a variable is read from the standard input; once a valid value  */
/*      is given, this value is stored in the 'parm' pointed location,  */
/*      otherwise the parm pointer is unchanged.                        */
/*      Functions:                                                      */
/*         scandigit()                                                  */
/*         scanint()                                                    */
/*         scandouble()                                                 */
/*         scanstring()                                                 */
/*      Return values:                                                  */
/*         - EASYIO_OKAY    : the value is valid;                       */
/*         - EASYIO_DEFAULT : the first character in input is <CR>;     */
/*         - EASYIO_ERROR   : error detected: string too long or        */
/*			      non valid characters included.            */
/*      As begin comment / EOL character, '#' is used.                  */
/*                                                                      */
/*----------------------------------------------------------------------*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "easyio.h"


//
// scandigit: max string length: 1 character;
//            valid characters: '0' to '9'
//

int	scandigit (int *parm) {
	int	c = readln();
	switch (c)  {
		case '\n' :
			return(EASYIO_DEFAULT);
		case '0':
		case '1':
		case '2':
		case '3':
		case '4':
		case '5':
		case '6':
		case '7':
		case '8':
		case '9':
			*parm = c -'0';
			return(EASYIO_OKAY);
		default:
			return(EASYIO_ERROR);
		}
	}


/*----------------------------------------------------------------------*/



//
// scanint:   max string length: EASYIO_MAX_INT_LEN;
//            valid characters: '0'-'9'
//

int	scanint (int *parm){

	int 	c;
	int	buf[EASYIO_MAX_BUF_LEN];
	int 	buf_len;

	for (buf_len=0; ((c=getchar()) != '\n') && (c != '#') && 
		(buf_len < EASYIO_MAX_BUF_LEN); buf_len++) buf[buf_len]=c;
	if (c=='#') c=readln();	/* empty buffer for next line */

	switch (buf_len)  {
		case 0:
			return(EASYIO_DEFAULT);
		case EASYIO_MAX_BUF_LEN:
			return(EASYIO_ERROR);
		default:
			break;
		}

	int 	intero=0;
	int 	count=0;
	short 	neg=1;

	for (int i=0; i<buf_len; i++) {
		c=buf[i];
		if ((c!=' ') && (c!='\t')) {
			if (count==-1) return(EASYIO_ERROR);
		      	else  count++;
			}
		if (count > EASYIO_MAX_INT_LEN) 
			return(EASYIO_ERROR);
		if (c=='-') 
			neg=-1;
		else if ((c >= '0') && (c <= '9'))
			intero=(intero*10)+buf[i]-'0';
	   	else if ((c==' ') || (c=='\t')) {
			if (count!=0) count=-1;
			}
		else return(EASYIO_ERROR);
		}

	*parm=neg*intero;
	return(EASYIO_OKAY);
	}


/*----------------------------------------------------------------------*/


//
// scanlong:   max string length: EASYIO_MAX_INT_LEN;
//            valid characters: '0'-'9'
//

int	scanlong (long *parm){

	int 	c;
	int	buf[EASYIO_MAX_BUF_LEN];
	int 	buf_len;

	for (buf_len=0; ((c=getchar()) != '\n') && (c != '#') &&
		(buf_len < EASYIO_MAX_BUF_LEN); buf_len++) buf[buf_len]=c;
	if (c=='#') c=readln();	/* empty buffer for next line */

	switch (buf_len)  {
		case 0:
			return(EASYIO_DEFAULT);
		case EASYIO_MAX_BUF_LEN:
			return(EASYIO_ERROR);
		default:
			break;
		}

	long 	intero=0;
	int 	count=0;
	short 	neg=1;

	for (int i=0; i<buf_len; i++) {
		c=buf[i];
		if ((c!=' ') && (c!='\t')) {
			if (count==-1) return(EASYIO_ERROR);
					else  count++;
			}
		if (count > EASYIO_MAX_INT_LEN)
			return(EASYIO_ERROR);
		if (c=='-')
			neg=-1;
		else if ((c >= '0') && (c <= '9'))
			intero=(intero*10)+buf[i]-'0';
			else if ((c==' ') || (c=='\t')) {
			if (count!=0) count=-1;
			}
		else return(EASYIO_ERROR);
		}

	*parm=neg*intero;
	return(EASYIO_OKAY);
	}


/*----------------------------------------------------------------------*/


//
// scandouble:   max string length: EASYIO_MAX_FLOAT_LEN;
//            valid characters: '0'-'9', '.'
//

int	scandouble (double *parm) {

	int 	c;
	int 	buf_len;
	int	buf[EASYIO_MAX_BUF_LEN];


	for (buf_len=0; ((c=getchar()) != '\n') && (c != '#') && 
		(buf_len < EASYIO_MAX_BUF_LEN); buf_len++) buf[buf_len]=c;
	if (c=='#') c=readln();		/* empty buffer for next line */

	switch (buf_len)  {
		case 0:
			return(EASYIO_DEFAULT);
		case EASYIO_MAX_BUF_LEN:
			return(EASYIO_ERROR);
		default:
			break;
		}

	double 	mantissa=0.0;
	int 	count=0;
	int 	pot=0;
	double 	potenza=1.0;
	short 	neg=1;

	for (int i=0; i<buf_len; i++) {
		c=buf[i];
		if ((c!=' ') && (c!='\t')) {
			if (count==-1) return(EASYIO_ERROR);
		      	else  count++;
			}
		if (count > EASYIO_MAX_FLOAT_LEN) 
			return(EASYIO_ERROR);
		if (c=='-') 
			neg=-1;
		else if ((c >= '0') && (c <= '9')) {
			mantissa=(mantissa*10)+buf[i]-'0';
			if (pot) potenza *= 10;
			}
	   	else if (c=='.') {
			if ((buf[i+1] <'0') || (buf[i+1]>'9'))
			   	return(EASYIO_ERROR);
			if (pot != 0)
			   	return(EASYIO_ERROR);
			pot=1;
			}
	   	else if ((c==' ') || (c=='\t')) {
			if (count!=0) count=-1;
			}
		else return(EASYIO_ERROR);
		}

	*parm=neg*mantissa/potenza;
	return(EASYIO_OKAY);
	}


/*----------------------------------------------------------------------*/


//
// scanstring:   max string length: EASYIO_MAX_STR_LEN;
//            valid characters:  '0'-'9','.','a'-'z','A','Z'
//

int	scanstring (char *parm) {
	int 	c;
	char 	buf[EASYIO_MAX_STR_LEN];
	int 	buf_len=0;

	for (buf_len=0; ((c=getchar()) != '\n') && (c != '#') && 
		(buf_len < EASYIO_MAX_STR_LEN); buf_len++) { 
			buf[buf_len]=c;
			if ((c != '.') && (c < '0') && (c > '9') && 
				(c < 'a') && (c > 'z') && (c < 'A') && 
				(c > 'Z'))  return(EASYIO_ERROR);
			}
	if (c=='#') c=readln();	/* empty buffer for next line */

	switch(buf_len)  {
		case 0:
			return(EASYIO_DEFAULT);
		case EASYIO_MAX_STR_LEN:
			return(EASYIO_ERROR);
		default:
			buf[buf_len] = '\0';
			strcpy(parm, buf);
			return(EASYIO_OKAY);
		}
	}
