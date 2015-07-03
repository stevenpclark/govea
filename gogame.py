from os import path
from sgf import SGF
import numpy as np
import logging
import time
from govea import B, W, opposite_color


GRID_DTYPE = np.int8


class GoGame(object):
	def __init__(self, sgf, debug=False):
		#iterate through sgf.moves, creating self.boardstates
		#first boardstate is empty, or has handicap stones
		#move i gets applied to state i to produce state i+1
		#so if we have m moves, we have m+1 states
		self.board_shape = sgf.board_shape
		self.handicap = sgf.handicap
		self.komi = sgf.komi
		self.player_w = sgf.player_w
		self.player_b = sgf.player_b
		self.date = sgf.date
		self.result = sgf.result
		self.moves = sgf.moves
		#TODO copy more fields

		initial_state = BoardState.empty_board(self.board_shape)
		for m in sgf.initial_moves:
			initial_state.grid[m.r,m.c] = m.color

		self.states = [initial_state]
		prev_state = initial_state
		
		for i, m in enumerate(self.moves):
			if debug: #FIXME
				print "about to play move %d: %s" % (i, m)
			try:
				state = BoardState(prev_state, m)
			except InconsistentBoardStateError as e:
				e.msg = "Inconsistent board state noticed at move %d (%s) in sgf %s" % (i, m, sgf.filename)
				raise e
			if debug:
				print "resulting state:"
				print state
				time.sleep(1.0)
			self.states.append(state)
			prev_state = state


		#or s in self.states:
		#	print(s)


class BoardState(object):
	def __init__(self, prev_state, move, shape=None):
		#board state results from applying move to prev_state
		self.prev_move = move
		if prev_state is None and move is None:
			self.shape = shape
			self.grid = np.zeros(shape, dtype=GRID_DTYPE)
			self._create_neighbor_map(shape)
			self.num_played_moves = 0
		else:
			self.shape = prev_state.shape
			self.grid = prev_state.grid.copy()
			self.neighbor_map = prev_state.neighbor_map #no need to copy this one
			self.num_played_moves = prev_state.num_played_moves + 1
			#print self.num_played_moves, move
			if not move.is_pass():
				if self.grid[move.r, move.c] != 0:
					raise InconsistentBoardStateError("")
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

		

class InconsistentBoardStateError(Exception):
	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return repr(self.msg)


if __name__ == '__main__':
	with open(path.join('data', 'sgf', 'Hutoshi4-kghin.sgf')) as f:
		sgf = SGF(f)
		game = GoGame(sgf)

