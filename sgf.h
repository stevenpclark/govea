#ifndef _sgf
#define _sgf

#include "gogame.h"

#define MAX_SGF_BYTES 4096

GoGame * createGameFromSGF(char * sgfData);

#endif