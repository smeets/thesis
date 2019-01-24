/*----------------------------------------------------------------------*/
/*                                                                      */
/*                               easyio_read.C                          */
/*                                                                      */
/*                                                                      */
/*                                                                      */
/*      This module contains procedures which print on the standard     */
/*      output a string containing user prompt and proposed default     */
/*      value.                                                          */
/*      a Read procedure (using the scan functions) is performed; in    */
/*      case of error or out of range value the read procedure is       */
/*      proposed again after a beep. A maximum number of attempts is    */
/*      defined to avoid loops in shells.                               */
/*          read_bool()                                                 */
/*          read_digit()                                                */
/*          read_int()                                                  */
/*          read_double()                                               */
/*          read_string()                                               */
/*                                                                      */
/*----------------------------------------------------------------------*/
#include <stdio.h>
#include <stdlib.h>
#include "easyio.h"

#define 	FPTR	stderr


//
// read_bool:
//	prompt: prompt user string;
//	def   : proposed default
//

short 	read_bool(char *prompt, short def) {
	int answer;
	for (int timeout = 0; timeout <=5; timeout++)  {
		if (def == false)
			fprintf(FPTR,"%s (y/n) [NO] > ",prompt);
		    else
			fprintf(FPTR,"%s (y/n) [YES] > ",prompt);
		answer = readln();
		switch(answer)  {
			case '\n':
				return(def);
			case 'y':
			case 'Y':
				return(true);
			case 'n':
			case 'N':
				return(false);
			default:
				beep();
				break;
			}
		}
	fprintf(FPTR, "\n FATAL ERROR: too many wrong attempts ");
	fprintf(FPTR, "in read_bool() \n");
	exit(-1);
	return(false); 	    // not used: just to be nice with the compiler
	}



//
// overloaded version without default
//
short 	read_bool(char *prompt) {
	return(read_bool(prompt, true));
	}



/*----------------------------------------------------------------------*/



//
// read_digit:
//	prompt: prompt user string;
//	def   : proposed default
//	min   : inferior limit
//	max   : superior limit
//
int 	read_digit (char *prompt, int def, int min, int max) {

	if (min < 0) min = 0;
	if (max < 0) max = 0;
	if (min > 9) min = 9;
	if (max > 9) max = 9;

	if (min > max) {
		int tmp = min;
		min = max;
		max = tmp;
		}

	if (def < min) def = min;
	if (def > max) def = max;

	short 	esito;
	int 	digit;
	short	failed = 0;

	for (int timeout = 0; timeout <= 5; timeout++)  {
		fprintf(FPTR,"%s ", prompt);
		if (failed) fprintf(FPTR, "(%d::%d) ", min, max);
		fprintf(FPTR,"[%d] > ",def);
		esito = scandigit(&digit);
		switch(esito)  {
			case EASYIO_DEFAULT:
				return(def);
			case EASYIO_OKAY:
				if ((digit >= min) && (digit <= max))
					return(digit);
			case EASYIO_ERROR:
				beep();
				failed = 1;
				break;
			}
		}
	fprintf(FPTR, "\n FATAL ERROR: too many wrong attempts ");
	fprintf(FPTR, "in read_digit() \n");
	exit(-1);
	return(false); 	    // not used: just to be nice with the compiler
	}


//
// overloaded version with no check
//
int 	read_digit (char *prompt, int def) {
	return(read_digit(prompt, def, 0, 9));
	}

//
// overloaded version with no check and default
//
int 	read_digit (char *prompt) {
	return(read_digit(prompt, 0, 0, 9));
	}


/*----------------------------------------------------------------------*/



//
// read_int:
//	prompt: prompt user string;
//	unit  : measurement unit of the reading value
//	def   : proposed default
//	min   : inferior limit
//	max   : superior limit
//

int 	read_int (char *prompt, char *unit, int def, int min, int max) {

        if (min > max) {
		int tmp = min;
	  	min = max;
	  	max = tmp;
		}

        if (def < min) def = min;
	if (def > max) def = max;

	int 	intero;
	short 	esito;
	short	failed = 0;

	for (int timeout = 0; timeout <= 5; timeout++)  {
		fprintf(FPTR,"%s ", prompt);
		if (failed) fprintf(FPTR, "(%d::%d) ", min, max);
		fprintf(FPTR,"[%d%s] > ", def, unit);
		esito = scanint(&intero);
		switch(esito)  {
			case EASYIO_DEFAULT :
				return(def);
			case EASYIO_OKAY :
				if ((intero >= min) && (intero <= max)) 
					return(intero);
			case EASYIO_ERROR :
				beep();
				failed = 1;
				break;
			}
		}
	fprintf(FPTR, "\n FATAL ERROR: too many wrong attempts ");
	fprintf(FPTR, "in read_int() \n");
	exit(-1);
	return(false); 	    // not used: just to be nice with the compiler
	}


//
// overloading without unit and/or range
//
int 	read_int (char *prompt, int def, int min, int max) {
	return( read_int(prompt, "", def, min, max));
	}
int 	read_int (char *prompt, char *unit, int def) {
	return( read_int(prompt, unit, def, EIO_MIN_INT, EIO_MAX_INT));
	}
int 	read_int (char *prompt, int def) {
	return( read_int(prompt, def, EIO_MIN_INT, EIO_MAX_INT));
	}
int 	read_int (char *prompt) {
	return( read_int(prompt, 0, EIO_MIN_INT, EIO_MAX_INT));
	}

/*----------------------------------------------------------------------*/


//
// read_long:
//	prompt: prompt user string;
//	unit  : measurement unit of the reading value
//	def   : proposed default
//	min   : inferior limit
//	max   : superior limit
//

long 	read_long (char *prompt, char *unit, long def, long min, long max) {

		  if (min > max) {
		long tmp = min;
		min = max;
		max = tmp;
		}

		  if (def < min) def = min;
	if (def > max) def = max;

	long 	intero;
	short 	esito;
	short	failed = 0;

	for (int timeout = 0; timeout <= 5; timeout++)  {
		fprintf(FPTR,"%s ", prompt);
		if (failed) fprintf(FPTR, "(%ld::%ld) ", min, max);
		fprintf(FPTR,"[%ld%s] > ", def, unit);
		esito = scanlong(&intero);
		switch(esito)  {
			case EASYIO_DEFAULT :
				return(def);
			case EASYIO_OKAY :
				if ((intero >= min) && (intero <= max))
					return(intero);
			case EASYIO_ERROR :
				beep();
				failed = 1;
				break;
			}
		}
	fprintf(FPTR, "\n FATAL ERROR: too many wrong attempts ");
	fprintf(FPTR, "in read_long() \n");
	exit(-1);
	return(false); 	    // not used: just to be nice with the compiler
	}


//
// overloading without unit and/or range
//
long 	read_long (char *prompt, long def, long min, long max) {
	return( read_long(prompt, "", def, min, max));
	}
long 	read_long (char *prompt, char *unit, long def) {
	return( read_long(prompt, unit, def, EIO_MIN_INT, EIO_MAX_INT));
	}
long 	read_long (char *prompt, long def) {
	return( read_long(prompt, def, EIO_MIN_INT, EIO_MAX_INT));
	}
long 	read_long (char *prompt) {
	return( read_long(prompt, 0, EIO_MIN_INT, EIO_MAX_INT));
	}

/*----------------------------------------------------------------------*/


//
// read_double:
//	prompt: prompt user string;
//	unit  : measurement unit of the reading value
//	def   : proposed default
//	min   : inferior limit
//	max   : superior limit
//

double 	read_double (char *prompt, char *unit, double def,
			double min, double max) {

		  if (min > max) {
		double tmp = min;
		min = max;
		max = tmp;
		}

		  if (def < min) def = min;
	if (def > max) def = max;

	double 	doppio;
	short 	esito;
	short	failed = 0;

	for (int timeout = 0; timeout <= 5; timeout++)  {
		fprintf(FPTR,"%s ", prompt);
		if (failed) fprintf(FPTR, "(%.4lf::%.4lf) ", min, max);
		fprintf(FPTR,"[%.4lf%s] > ", def, unit);
		esito = scandouble(&doppio);
		switch(esito)  {
			case EASYIO_DEFAULT :
				return(def);
			case EASYIO_OKAY :
				if ((doppio >= min) && (doppio <= max)) 
					return(doppio);
			case EASYIO_ERROR :
				beep();
				failed = 1;
				break;
			}
		}
	fprintf(FPTR, "\n FATAL ERROR: too many wrong attempts ");
	fprintf(FPTR, "in read_double() \n");
	exit(-1);
	return(false); 	    // not used: just to be nice with the compiler
	}

//
// overloading without unit and/or range
//
double 	read_double (char *prompt, double def, double min, double max) {
	return( read_double(prompt, "", def, min, max));
	}
double 	read_double (char *prompt, char *unit, double def) {
	return( read_double(prompt, unit, def, EIO_MIN_INT, EIO_MAX_INT));
	}
double 	read_double (char *prompt, double def) {
	return( read_double(prompt, def, EIO_MIN_INT, EIO_MAX_INT));
	}
double 	read_double (char *prompt) {
	return( read_double(prompt, 0, EIO_MIN_INT, EIO_MAX_INT));
	}



/*----------------------------------------------------------------------*/

//
// read_string:
//	prompt: prompt user string;
//	def   : proposed default
//

char * 	read_string (char *prompt, char *def) {

	short 	esito;
	static char 	stringa[EASYIO_MAX_STR_LEN];

	for (int timeout = 0; timeout <= 5; timeout++)  {
		fprintf(FPTR,"%s [%s] > ",prompt,def);
		esito = scanstring(stringa);
		switch(esito)  {
			case EASYIO_DEFAULT:
				return(def);
			case EASYIO_OKAY:
				return(stringa);
			case EASYIO_ERROR:
				beep();
				break;
			}
		}
	fprintf(FPTR, "\n FATAL ERROR: too many wrong attempts ");
	fprintf(FPTR, "in read_string() \n");
	exit(-1);
	return(false); 	    // not used: just to be nice with the compiler
	}


//
// overloading without default
//
char * 	read_string (char *prompt) {
	return( read_string(prompt, ""));
	}

