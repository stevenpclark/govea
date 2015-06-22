"""a pattern is essentially an (stimulus, response) tuple.
using a 'one-hot' representation for our neural net.
stimulus = a numpy array of dim (numrows, numcols, 4)
	4 planes:
		0: empty
		1: enemy color
		2: friendly color 
		3: last move
			for 19x19, this 1444 inputs

	all values are either 0 or 1
	all row,col locations should have a 1 in exactly 1 of the
		first 3 planes
	inputs are normalized with respect to the active player.
		regardless of B or W, if it is their turn, their stones
		show up in layer 2, and opponent's in layer 1.

response = a numpy array of dim (numrows, numcols, 1)
	in a training example, the 'correct' move should be 1,
		and all other locations 0
	in a NN response, should be a softmax-style 0-1 values,
		with the whole array summing to 1"""

import numpy as np
from govea import EMPTY, opposite_color


class NNPattern(object):
	EMPTY_LAYER, ENEMY_LAYER, FRIENDLY_LAYER, LAST_MOVE_LAYER = range(4)

	def __init__(self, stimulus, response):
		self.stimulus = stimulus
		self.response = response

	def fliplr(self):
		#return a left-right mirrored copy of the pattern
		return NNPattern(np.fliplr(self.stimulus), np.fliplr(self.response))

	def rot90(self):
		#return a rotated CCW 90 copy of the pattern
		return NNPattern(np.rot90(self.stimulus), np.rot90(self.response))

	def __eq__(self, other):
		return (self.stimulus==other.stimulus) and (self.response==other.response)

	def __repr__(self):
		return '\n'.join([repr(self.stimulus[:,:,0]), repr(self.stimulus[:,:,1]), repr(self.stimulus[:,:,2]), repr(self.stimulus[:,:,3]), repr(self.response)])

	@classmethod
	def get_single_pattern(cls, grid, prev_move, next_move):
		#grid is the state after prev_move is applied, before next_move is applied
		#look at next_move to figure out friendly/active color, and fill in response
		#look at prev_move to fill in stimulus layer 3
		#look at grid to fill in stimulus layers 0,1,2
		#return a single pattern (no rotations/mirrors)
		friendly_color = next_move.color
		enemy_color = opposite_color(friendly_color)
		shape = grid.shape
		
		stimulus = np.zeros((shape[0], shape[1], 4), dtype=np.int8) #TODO dtype? use bool instead?
		stimulus[:,:,NNPattern.EMPTY_LAYER] = (grid == EMPTY)
		stimulus[:,:,NNPattern.ENEMY_LAYER] = (grid == enemy_color)
		stimulus[:,:,NNPattern.FRIENDLY_LAYER] = (grid == friendly_color)
		stimulus[prev_move.r, prev_move.c, NNPattern.LAST_MOVE_LAYER] = 1

		response = np.zeros(shape, dtype=np.int8)
		response[next_move.r, next_move.c] = 1

		return cls(stimulus, response)

	@classmethod
	def get_patterns(cls, grid, prev_move, next_move):
		#return a list of all 8 rotation/mirror symmetric patterns
		#TODO potential optimizations if lots of time spent here
		
		base_pattern = cls.get_single_pattern(grid, prev_move, next_move)
		mirrored_pattern = base_pattern.fliplr()
		results = [base_pattern, mirrored_pattern]
		for i in range(3):
			base_pattern = base_pattern.rot90()
			mirrored_pattern = mirrored_pattern.rot90()
			results.append(base_pattern)
			results.append(mirrored_pattern)
			
		return results


if __name__ == '__main__':
	from os import path
	from sgf import SGF
	from gogame import GoGame
	with open(path.join('data', 'sgf', 'Hutoshi4-kghin.sgf')) as f:
		sgf = SGF(f)
		game = GoGame(sgf)
		board_state = game.states[5]
		print board_state
		next_move = game.moves[5]
		print next_move

		pattern = NNPattern.get_patterns(board_state.grid, board_state.incoming_move, next_move)[0]
		print pattern.stimulus[:,:,0]
		print pattern.response