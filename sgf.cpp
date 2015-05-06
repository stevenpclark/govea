#include <cstdio>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include "sgf.h"
#include "gogame.h"

#define MAX_KEY_LEN 32
#define MAX_VALUE_LEN 64

enum ParserState {PREKEY, MIDKEY, PREVALUE, MIDVALUE};

GoGame * createGameFromSGF(char * path)
{
	FILE * f;
	char sgfBuf[MAX_SGF_BYTES];
	GoGame * game = NULL;
	int numBytesConsumed = 0;
	char c;
	ParserState state = PREKEY;
	char key[MAX_KEY_LEN];
	char value[MAX_VALUE_LEN];
	int keyLen;
	int valueLen;
	int startInd;
	int boardSize = 19;
	int handicap = 0;
	Move moves[MAX_MOVES];
	int numMoves = 0;
	Vertex v;
	Move m;
	Player p = B;
	
	f = fopen(path, "rb");
	if(f == NULL) {
		printf("bad file\n");
		return NULL;
	}
	int numBytes = fread(sgfBuf, 1, MAX_SGF_BYTES, f);
	fclose(f);
	
	if(numBytes < 500) {
		//printf("file too short\n");
		return NULL;
	}
	
	while(numBytesConsumed < numBytes) {
		c = sgfBuf[numBytesConsumed];
		
		switch(state) {
			case PREKEY:
				if(isalpha(c)) {
					state = MIDKEY;
					startInd = numBytesConsumed;
				}
				break;
				
			case MIDKEY:
				if(c == '[') {
					state = PREVALUE;
					keyLen = numBytesConsumed - startInd;
					if(keyLen+1 < MAX_KEY_LEN) {
						memcpy(key, sgfBuf+startInd, keyLen);
						key[keyLen] = '\0';
					}
				}
				break;
				
			case PREVALUE:
				if(!isspace(c)) {
					state = MIDVALUE;
					startInd = numBytesConsumed;
				}
				break;
				
			case MIDVALUE:
				if(c == ']') {
					state = PREKEY;
					valueLen = numBytesConsumed - startInd;
					if(valueLen+1 < MAX_VALUE_LEN) {
						memcpy(value, sgfBuf+startInd, valueLen);
						value[valueLen] = '\0';
						
						if(keyLen > 0 && valueLen > 0) {
							if(strcmp(key, "B")==0 || strcmp(key, "W")==0) {
								v.x = value[0]-'a';
								v.y = value[1]-'a';
								if(v.x >= 0 && v.y >= 0 && v.x < boardSize && v.y < boardSize) {
									m.v = v;
									m.p = p;
									p = FLIP_PLAYER(p);
									moves[numMoves] = m;
									numMoves++;
								}
							} else if(strcmp(key, "SZ")==0) {
								boardSize = atoi(value);
							} else if(strcmp(key, "HA")==0) {
								handicap = atoi(value);
							}
						}
					}
				}
				break;
		}
		numBytesConsumed++;
	}
	
	game = new GoGame(handicap, numMoves, moves);
	
	return game;
}