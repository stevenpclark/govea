#include <cstdio>
#include <string.h>
#include <stdlib.h>
#include <assert.h> //FIXME

#include "gogame.h"

Vertex::Vertex()
{
	x = -1;
	y = -1;
}

Vertex::Vertex(int _x, int _y)
{
	x = _x;
	y = _y;
}

int distanceFromEdge(Vertex v)
{
	int dx = HALF_INDEX-abs(HALF_INDEX-v.x);
	int dy = HALF_INDEX-abs(HALF_INDEX-v.y);
	
	return min(dx,dy);
}

int v2i(Vertex v)
{
	return v.y*BOARD_SIZE + v.x;
}

Move::Move()
{
	p = EMPTY;
}

Move::Move(Player _p, Vertex _v)
{
	p = _p;
	v = _v;
}

void Move::print()
{
	printf("%s: %02d %02d\n", p==B? "B" : "W", v.x, v.y);
}

GoGame::GoGame(int _handicap, int _numMoves, Move *_moves)
{
	handicap = _handicap;
	numMoves = _numMoves;
	moves = (Move*)malloc(numMoves*sizeof(Move));
	memcpy(moves, _moves, numMoves*sizeof(Move));
	
	states = (Board**)malloc(numMoves*sizeof(Board*));
	states[0] = new Board(); //FIXME assuming B first, no handicap
	for(int i=1; i<numMoves; i++) {
		//moves[i-1].print();
		states[i] = new Board(states[i-1], moves[i-1]);
	}
	
	/*for(int i=0; i<numMoves; i++) {
		moves[i].print();
		//states[i]->print();
	}*/
}

GoGame::~GoGame()
{
	free(moves);
	for(int i=0; i<numMoves; i++) {
		delete states[i];
	}
	free(states);
}


Board::Board()
{
	grid = (char*)calloc(BOARD_SIZE*BOARD_SIZE, sizeof(char));
	nextPlayer = B;
}

Board::Board(Board *prevBoard, Move m)
{
	int numBytes = BOARD_SIZE*BOARD_SIZE*sizeof(char);
	grid = (char*)malloc(numBytes);
	memcpy(grid, prevBoard->grid, numBytes);
	nextPlayer = FLIP_PLAYER(prevBoard->nextPlayer);
	playMove(m);
}

Board::~Board()
{
	free(grid);
}

void Board::playMove(Move m)
{
	//NOTE ASSUME M IS LEGAL!
	Vertex v = m.v;
	grid[v2i(v)] = m.p;
	
	//check if life status of adjacent enemy groups changed
	Vertex v2;
	bool visited[BOARD_SIZE*BOARD_SIZE];
	int numCapped = 0;
	if(getW(v, v2)) {
		if(grid[v2i(v2)] == nextPlayer) {
			bzero(visited, BOARD_SIZE*BOARD_SIZE);
			numCapped += removeIfCaptured(v2, visited);
		}
	}
	if(getE(v, v2)) {
		if(grid[v2i(v2)] == nextPlayer) {
			bzero(visited, BOARD_SIZE*BOARD_SIZE);
			numCapped += removeIfCaptured(v2, visited);
		}
	}
	if(getN(v, v2)) {
		if(grid[v2i(v2)] == nextPlayer) {
			bzero(visited, BOARD_SIZE*BOARD_SIZE);
			numCapped += removeIfCaptured(v2, visited);
		}
	}
	if(getS(v, v2)) {
		if(grid[v2i(v2)] == nextPlayer) {
			bzero(visited, BOARD_SIZE*BOARD_SIZE);
			numCapped += removeIfCaptured(v2, visited);
		}
	}
	
	/*if(numCapped > 0) {
		printf("numCapped: %d\n", numCapped);
	}*/
}


int Board::removeIfCaptured(Vertex v, bool * visited)
{
	//Assume v is on board, belongs to enemy
	list<Vertex> stoneList;
	
	if(findLiberty(v, visited, &stoneList) == true) {
		return 0;
	} else {
		for (list<Vertex>::iterator it = stoneList.begin(); it != stoneList.end(); it++) {
    		//printf("kill: %d %d\n", (*it).x, (*it).y);
    		grid[v2i(*it)] = EMPTY;
    	}
		
		return stoneList.size(); //how many were captured
	}
}


bool Board::findLiberty(Vertex v, bool * visited, list<Vertex>* stoneList)
{
	visited[v2i(v)] = true;
	
	Vertex v2;
	int i2;
	
	if(getW(v, v2)) {
		i2 = v2i(v2);
		if(grid[i2] == EMPTY) {
			return true;
		} else if(grid[i2] == nextPlayer && !visited[i2]) {
			if(findLiberty(v2, visited, stoneList)) {
				return true;
			}
		}
	}
	if(getE(v, v2)) {
		i2 = v2i(v2);
		if(grid[i2] == EMPTY) {
			return true;
		} else if(grid[i2] == nextPlayer && !visited[i2]) {
			if(findLiberty(v2, visited, stoneList)) {
				return true;
			}
		}
	}
	if(getN(v, v2)) {
		i2 = v2i(v2);
		if(grid[i2] == EMPTY) {
			return true;
		} else if(grid[i2] == nextPlayer && !visited[i2]) {
			if(findLiberty(v2, visited, stoneList)) {
				return true;
			}
		}
	}
	if(getS(v, v2)) {
		i2 = v2i(v2);
		if(grid[i2] == EMPTY) {
			return true;
		} else if(grid[i2] == nextPlayer && !visited[i2]) {
			if(findLiberty(v2, visited, stoneList)) {
				return true;
			}
		}
	}
	
	stoneList->push_back(v);
	return false;
}


void Board::print()
{
	char * g = grid;
	for(int y=0; y<BOARD_SIZE; y++) {
		for(int x=0; x<BOARD_SIZE; x++) {
			switch(*g) {
				case 0:
					printf(".");
					break;
				case B:
					printf("X");
					break;
				case W:
					printf("O");
					break;
				default:
					printf("?");
					
			}
			g++;
		}
		printf("\n");
	}
}


inline bool Board::getW(Vertex &v1, Vertex &v2)
{
	if(v1.x <= 0) {
		return false;
	} else {
		v2.x = v1.x-1;
		v2.y = v1.y;
		return true;
	}
}

inline bool Board::getE(Vertex &v1, Vertex &v2)
{
	if(v1.x >= (BOARD_SIZE-1)) {
		return false;
	} else {
		v2.x = v1.x+1;
		v2.y = v1.y;
		return true;
	}
}

inline bool Board::getN(Vertex &v1, Vertex &v2)
{
	if(v1.y <= 0) {
		return false;
	} else {
		v2.x = v1.x;
		v2.y = v1.y-1;
		return true;
	}
}

inline bool Board::getS(Vertex &v1, Vertex &v2)
{
	if(v1.y >= (BOARD_SIZE-1)) {
		return false;
	} else {
		v2.x = v1.x;
		v2.y = v1.y+1;
		return true;
	}
}