/*----------------------------------------------------------------------*/
/*                                                                      */
/*                               easyio.h                               */
/*                                                                      */
/*      This module contains the header for the functions exported by   */
/*			the easyio C++ package				*/
/*                                                                      */
/*----------------------------------------------------------------------*/

#ifndef _EASYIOPLUS_H
#define _EASYIOPLUS_H

#define EASYIO_MAX_INT_LEN 		9   /* max integer = (10E10 - 1) */
#define EASYIO_MAX_FLOAT_LEN 		15
#define EASYIO_MAX_STR_LEN 		80
#define EASYIO_MAX_BUF_LEN 		80

#define	EIO_MIN_INT 			-1000000000
#define	EIO_MAX_INT  			1000000000
#define EASYIO_OKAY 			0
#define EASYIO_ERROR 			1
#define EASYIO_DEFAULT 			2

#define true 				1
#define false 				0

extern		int	scandigit (int *);
extern		int	scanint (int *);
extern		int	scanlong (long *);
extern		int	scandouble (double *);
extern		int	scanstring (char *);

extern		void 	clear_screen();
extern		void 	beep();
extern		void 	pausa();
extern		char	readln ();

extern	 	short 	read_bool(char *, short);
extern		short 	read_bool(char *);

extern	 	int 	read_digit(char *, int, int, int);
extern		int 	read_digit(char *, int);
extern		int 	read_digit(char *);

extern		int 	read_int(char *, char *, int, int, int);
extern		int 	read_int(char *, int, int, int);
extern		int 	read_int(char *, char *, int);
extern		int 	read_int(char *, int);
extern		int 	read_int(char *);

extern		long 	read_long(char *, char *, long, long, long);
extern		long 	read_long(char *, long, long, long);
extern		long 	read_long(char *, char *, long);
extern		long 	read_long(char *, long);
extern		long 	read_long(char *);

extern		double 	read_double(char *, char *, double, double, double);
extern		double 	read_double(char *, double, double, double);
extern		double 	read_double(char *, char *, double);
extern		double 	read_double(char *, double);
extern		double 	read_double(char *);

extern		char * 	read_string(char *, char *);
extern		char * 	read_string(char *);

#endif    // _EASYIOPLUS_H
