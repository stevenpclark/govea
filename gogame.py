from os import path
from sgf import SGF
import numpy as np
import logging
import time
from govea import B, W, opposite_color




class GoGame(object):
	def __init__(self, sgf):
		#iterate through sgf.moves, creating self.boardstates
		#first boardstate is empty, or has handicap stones
		self.board_shape = sgf.board_shape
		#TODO copy more fields

		if sgf.handicap == 0:
			initial_state = BoardState.empty_board(self.board_shape)
		else:
			initial_state = BoardState.handicap_board(self.board_shape, sgf.handicap)
		self.states = [initial_state]
		prev_state = initial_state
		for m in sgf.moves:
			state = BoardState(prev_state, m)
			self.states.append(state)
			prev_state = state

		#or s in self.states:
		#	print(s)


class BoardState(object):
	def __init__(self, prev_state, move, shape=None):
		if prev_state is None and move is None:
			self.shape = shape
			self.grid = np.zeros(shape, dtype=np.int8)
			self._create_neighbor_map(shape)
			self.num_played_moves = 0
		else:
			self.shape = prev_state.shape
			self.grid = prev_state.grid.copy()
			self.neighbor_map = prev_state.neighbor_map #no need to copy this one
			self.num_played_moves = prev_state.num_played_moves + 1
			#print self.num_played_moves, move
			if not move.is_pass():
				assert(self.grid[move.r, move.c] == 0)
				color = move.color #the color of the player making the move
				enemy_color = opposite_color(color)
				r = move.r
				c = move.c
				self.grid[r,c] = color
				#assume move is legal. (not suicide, etc.)
				#for each adjacent enemy group, check to see if it has any liberties left
				#(send in a blank visit grid)
				#if not, remove that group and increment captures appropriately
				visited = np.zeros(self.shape, dtype=np.bool)
				for r2, c2 in self.neighbor_map[r,c]:
					if self.grid[r2,c2] == enemy_color:
						#it's an enemy group
						if visited[r2,c2]:
							continue #we've already thought about this group
						visited.fill(False)
						if not self._has_liberty(r2, c2, enemy_color, visited):
							#this enemy group has been killed!
							num_removed = np.count_nonzero(visited) #FIXME add to tally
							self.grid[visited] = 0
							logging.debug('Move %s killed %d stones', move, num_removed)
			
			#time.sleep(1.0)
			#print self
			

	@classmethod
	def empty_board(cls, shape):
		return cls(None, None, shape=shape)

	@classmethod
	def handicap_board(cls, shape, handicap):
		if handicap<2 or handicap>9:
			raise ValueError('handicap of %d not supported'%handicap)
		nr, nc = shape
		cl, cm, cr = 3, nc/2, nc-4
		rt, rm, rb = 3, nr/2, nr-4
		board = cls(None, None, shape=shape)
		
		board.grid[rt,cr] = B
		board.grid[rb,cl] = B
		if handicap >= 3:
			board.grid[rb,cr] = B
		if handicap >= 4:
			board.grid[rt,cl] = B
		if handicap in [5,7,9]:
			board.grid[rm,cm] = B
		if handicap >= 6:
			board.grid[rm,cl] = B
			board.grid[rm,cr] = B
		if handicap >= 8:
			board.grid[rt,cm] = B
			board.grid[rb,cm] = B

		return board


	def _create_neighbor_map(self, shape):
		self.neighbor_map = np.ndarray(shape, dtype=list)
		for r in range(shape[0]):
			for c in range(shape[1]): #TODO shortcut?
				neighbors = [] #will have 2,3, or 4 neighbors
				
				if r > 0: #Up
					neighbors.append((r-1,c))
				if c > 0: #Left
					neighbors.append((r,c-1))
				if r < shape[0]-1: #Down
					neighbors.append((r+1,c))
				if c < shape[1]-1: #Right
					neighbors.append((r,c+1))

				self.neighbor_map[r,c] = neighbors


	def __repr__(self):
		#TODO how much overhead in this approach?
		np.set_printoptions(formatter={'int_kind':lambda x: {B:'X', W:'O', 0:'.'}[x]})
		s = str(self.grid)
		np.set_printoptions() #reset to default
		return s



	def _has_liberty(self, r, c, color, visited):
		#return true if at least one liberty exists for color's group at r,c
		#modifies visited grid in the process
		if visited[r,c]:
			return False #we've already been here
		visited[r,c] = True
		#logging.debug("visiting %d %d (%d)", r, c, self.grid[r,c])
		
		for r2, c2 in self.neighbor_map[r,c]:
			x = self.grid[r2,c2]
			#logging.debug("considering %d %d (%d)", r2, c2, x)
			if x == 0 or (x==color and self._has_liberty(r2, c2, color, visited)):
				return True
		
		return False #exhausted all possibilities, give up

		


if __name__ == '__main__':
	with open(path.join('data', 'sgf', 'Hutoshi4-kghin.sgf')) as f:
		s = f.read()
		sgf = SGF(s)
		game = GoGame(sgf)