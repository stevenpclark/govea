import unittest
import numpy as np
from pattern_extract import NNPattern
from gogame import GRID_DTYPE
from govea import B, W, Move


class PatternExtractTestCase(unittest.TestCase):
	def test_pattern_extract(self):
		grid = np.array([[B, W, 0],
						 [0, B, 0],
						 [0, W, 0]], dtype=GRID_DTYPE)
		prev_move = Move(W, (0, 1))
		next_move = Move(B, (0, 2))

		patterns = NNPattern.get_patterns(grid, prev_move, next_move)

		base_pattern = patterns[0]
		mirrored_pattern = patterns[1]
		rotated_pattern = patterns[2]

		assert(np.array_equal(base_pattern.stimulus[:,:,NNPattern.EMPTY_LAYER],
			[[0,0,1],
			 [1,0,1],
			 [1,0,1]]))
		assert(np.array_equal(base_pattern.stimulus[:,:,NNPattern.ENEMY_LAYER],
			[[0,1,0],
			 [0,0,0],
			 [0,1,0]]))
		assert(np.array_equal(base_pattern.stimulus[:,:,NNPattern.FRIENDLY_LAYER],
			[[1,0,0],
			 [0,1,0],
			 [0,0,0]]))
		assert(np.array_equal(base_pattern.stimulus[:,:,NNPattern.LAST_MOVE_LAYER],
			[[0,1,0],
			 [0,0,0],
			 [0,0,0]]))
		assert(np.array_equal(base_pattern.response[:,:],
			[[0,0,1],
			 [0,0,0],
			 [0,0,0]]))

		assert(np.array_equal(mirrored_pattern.stimulus[:,:,NNPattern.EMPTY_LAYER],
			[[1,0,0],
			 [1,0,1],
			 [1,0,1]]))
		assert(np.array_equal(mirrored_pattern.stimulus[:,:,NNPattern.ENEMY_LAYER],
			[[0,1,0],
			 [0,0,0],
			 [0,1,0]]))
		assert(np.array_equal(mirrored_pattern.stimulus[:,:,NNPattern.FRIENDLY_LAYER],
			[[0,0,1],
			 [0,1,0],
			 [0,0,0]]))
		assert(np.array_equal(mirrored_pattern.stimulus[:,:,NNPattern.LAST_MOVE_LAYER],
			[[0,1,0],
			 [0,0,0],
			 [0,0,0]]))
		assert(np.array_equal(mirrored_pattern.response[:,:],
			[[1,0,0],
			 [0,0,0],
			 [0,0,0]]))

		assert(np.array_equal(rotated_pattern.stimulus[:,:,NNPattern.EMPTY_LAYER],
			[[1,1,1],
			 [0,0,0],
			 [0,1,1]]))
		assert(np.array_equal(rotated_pattern.stimulus[:,:,NNPattern.ENEMY_LAYER],
			[[0,0,0],
			 [1,0,1],
			 [0,0,0]]))
		assert(np.array_equal(rotated_pattern.stimulus[:,:,NNPattern.FRIENDLY_LAYER],
			[[0,0,0],
			 [0,1,0],
			 [1,0,0]]))
		assert(np.array_equal(rotated_pattern.stimulus[:,:,NNPattern.LAST_MOVE_LAYER],
			[[0,0,0],
			 [1,0,0],
			 [0,0,0]]))
		assert(np.array_equal(rotated_pattern.response[:,:],
			[[1,0,0],
			 [0,0,0],
			 [0,0,0]]))




if __name__ == '__main__':
	unittest.main()