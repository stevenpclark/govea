from os import path
import unittest
import numpy as np
import random
from pattern import NNPattern, get_patterns, get_all_game_patterns
from gogame import GRID_DTYPE, GoGame
from govea import B, W, Move
import glob
from utils import get_sgf_paths


class PatternExtractTestCase(unittest.TestCase):
	def test_pattern_extract(self):
		grid = np.array([[B, W, 0],
						 [0, B, 0],
						 [0, W, 0]], dtype=GRID_DTYPE)
		prev_move = Move(W, (0, 1))
		next_move = Move(B, (0, 2))

		patterns = get_patterns(grid, prev_move, next_move)

		base_pattern = patterns[0]
		mirrored_pattern = patterns[1]
		rotated_pattern = patterns[2]

		assert(np.array_equal(base_pattern.stimulus[NNPattern.EMPTY_LAYER,:,:],
			[[0,0,1],
			 [1,0,1],
			 [1,0,1]]))
		assert(np.array_equal(base_pattern.stimulus[NNPattern.ENEMY_LAYER,:,:],
			[[0,1,0],
			 [0,0,0],
			 [0,1,0]]))
		assert(np.array_equal(base_pattern.stimulus[NNPattern.FRIENDLY_LAYER,:,:],
			[[1,0,0],
			 [0,1,0],
			 [0,0,0]]))
		assert(np.array_equal(base_pattern.stimulus[NNPattern.LAST_MOVE_LAYER,:,:],
			[[0,1,0],
			 [0,0,0],
			 [0,0,0]]))
		assert(np.array_equal(base_pattern.response[:,:],
			[[0,0,1],
			 [0,0,0],
			 [0,0,0]]))

		assert(np.array_equal(mirrored_pattern.stimulus[NNPattern.EMPTY_LAYER,:,:],
			[[1,0,0],
			 [1,0,1],
			 [1,0,1]]))
		assert(np.array_equal(mirrored_pattern.stimulus[NNPattern.ENEMY_LAYER,:,:],
			[[0,1,0],
			 [0,0,0],
			 [0,1,0]]))
		assert(np.array_equal(mirrored_pattern.stimulus[NNPattern.FRIENDLY_LAYER,:,:],
			[[0,0,1],
			 [0,1,0],
			 [0,0,0]]))
		assert(np.array_equal(mirrored_pattern.stimulus[NNPattern.LAST_MOVE_LAYER,:,:],
			[[0,1,0],
			 [0,0,0],
			 [0,0,0]]))
		assert(np.array_equal(mirrored_pattern.response[:,:],
			[[1,0,0],
			 [0,0,0],
			 [0,0,0]]))

		assert(np.array_equal(rotated_pattern.stimulus[NNPattern.EMPTY_LAYER,:,:],
			[[1,1,1],
			 [0,0,0],
			 [0,1,1]]))
		assert(np.array_equal(rotated_pattern.stimulus[NNPattern.ENEMY_LAYER,:,:],
			[[0,0,0],
			 [1,0,1],
			 [0,0,0]]))
		assert(np.array_equal(rotated_pattern.stimulus[NNPattern.FRIENDLY_LAYER,:,:],
			[[0,0,0],
			 [0,1,0],
			 [1,0,0]]))
		assert(np.array_equal(rotated_pattern.stimulus[NNPattern.LAST_MOVE_LAYER,:,:],
			[[0,0,0],
			 [1,0,0],
			 [0,0,0]]))
		assert(np.array_equal(rotated_pattern.response[:,:],
			[[1,0,0],
			 [0,0,0],
			 [0,0,0]]))


	def test_extract_game_patterns(self):
		from sgf import SGF
		paths = get_sgf_paths()
		random.shuffle(paths)
		num_test_sgfs = min(len(paths), 50)
		print '%d sgfs found, randomly parsing %d of them' % (len(paths), num_test_sgfs)
		all_patterns = []
		for p in paths[:num_test_sgfs]:
			#print 'loading %s' % p
			with open(p, 'rb') as f:
				sgf = SGF(f)
				game = GoGame(sgf, debug=False)
				assert(len(game.moves)+1 == len(game.states))
				game_patterns = get_all_game_patterns(game)
				assert(len(game_patterns) == 8*len(game.moves))
				all_patterns.extend(game_patterns)

		print len(all_patterns)



if __name__ == '__main__':
	unittest.main()
