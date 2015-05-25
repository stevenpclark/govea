from os import path
from sgf import SGF
import numpy as np


class GoGame(object):
	def __init__(self, sgf):
		#iterate through sgf.moves, creating self.boardstates
		#first boardstate is empty
		assert(sgf.handicap == 0) #TODO handle handicap games
		self.board_shape = sgf.board_shape

		initial_state = BoardState(None, None, self.board_shape)
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
			self.grid = np.zeros(shape, np.int8)
		else:
			self.grid = prev_state.grid.copy()
			if not move.isPass:
				self.grid[move.r,move.c] = move.p

	def __repr__(self):
		return str(self.grid)


if __name__ == '__main__':
	with open(path.join('sgf', 'Hutoshi4-kghin.sgf')) as f:
		s = f.read()
		sgf = SGF(s)
		game = GoGame(sgf)