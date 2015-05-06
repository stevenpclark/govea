#ifndef _gogame
#define _gogame

#include <list>
using namespace std;

#define BOARD_SIZE 19
#define HALF_INDEX 9

#define MAX_MOVES 500

enum Player {EMPTY=0, B=-1, W=1};
#define FLIP_PLAYER(p) ((Player)(-p))

class Vertex
{
public:
	Vertex();
	Vertex(int x, int y);
	int x;
	int y;
};

int distanceFromEdge(Vertex v);
int v2i(Vertex v);

class Move
{
public:
	Move();
	Move(Player p, Vertex v);
	Player p;
	Vertex v;
	void print();
};

class Board
{
public:
	Board();
	Board(Board *prevBoard, Move m);
	~Board();
	void print();
	char * getGrid() { return grid; }
	
private:
	char * grid;
	Player nextPlayer;
	
	void playMove(Move m);
	inline bool getW(Vertex &v1, Vertex &v2);
	inline bool getE(Vertex &v1, Vertex &v2);
	inline bool getN(Vertex &v1, Vertex &v2);
	inline bool getS(Vertex &v1, Vertex &v2);
	int removeIfCaptured(Vertex v, bool * visited);
	bool findLiberty(Vertex v, bool * visited, list<Vertex>* stoneList);
};

class GoGame
{
public:
	GoGame(int _handicap, int _numMoves, Move *_moves);
	~GoGame();
	
	int getHandicap() { return handicap; }
	int getNumMoves() { return numMoves; }
	Move * getMoves() { return moves; }
	Board ** getBoards() { return states; }
	
private:
	int handicap;
	int numMoves;
	Move * moves;
	Board ** states;
};

#endif