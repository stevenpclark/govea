import numpy as np
import unittest
from gogame import BoardState, B, W, GoGame
from govea import Move
import glob
from os import path
import random
from utils import get_sgf_paths


class GoGameTestCase(unittest.TestCase):
	def test_capture1(self):
		state1 = BoardState.empty_board((19,19))
		state1.grid[:] = grid1a
		#print state1
		self.assertTrue(np.array_equal(state1.grid, grid1a))
		state2 = BoardState(state1, Move(B, (15,16)))
		self.assertTrue(np.array_equal(state2.grid, grid1b))
		state3 = BoardState(state2, Move(W, (14,14)))
		self.assertTrue(np.array_equal(state3.grid, grid1c))
		state4 = BoardState(state3, Move(B, (14,13)))
		self.assertTrue(np.array_equal(state4.grid, grid1d))
		state5 = BoardState(state4, Move(W, None))
		self.assertTrue(np.array_equal(state5.grid, grid1e))
		state6 = BoardState(state5, Move(B, (15,14)))
		self.assertTrue(np.array_equal(state6.grid, grid1f))

		state1 = BoardState.empty_board((19,19))
		state1.grid[:] = grid2a
		self.assertTrue(np.array_equal(state1.grid, grid2a))
		state2 = BoardState(state1, Move(B, (3,2)))
		self.assertTrue(np.array_equal(state2.grid, grid2b))

	def test_many_sgfs(self):
		from sgf import SGF
		paths = get_sgf_paths()
		random.shuffle(paths)
		num_test_sgfs = min(len(paths), 500)
		print '%d sgfs found, randomly parsing %d of them' % (len(paths), num_test_sgfs)
		for p in paths[:num_test_sgfs]:
			#print 'loading %s' % p
			with open(p, 'rb') as f:
				sgf = SGF(f)
				game = GoGame(sgf, debug=False)
				assert(len(game.moves)+1 == len(game.states))
				#print '%d moves' % len(sgf.moves)



def parse_board(s):
	s = s.replace('\n', '')
	s = s.replace(' ', ', ')
	s = s.replace('X', 'B')
	s = s.replace('O', 'W')
	s = s.replace('.', '0')
	return eval(s)


grid1a = parse_board("""
[[. . . . O . . X . . . . . . . . . . .]
 [. X O . . O X . X . . . . . O O . O .]
 [X O . . O . O X . . O X . X X O X X .]
 [. X X . . . O . . O . X . . . X O O .]
 [. X O . . O . . . . . . . X O X O . .]
 [. . . . . . . . . . . . . X O O X O .]
 [. X . . . . . . . . . . X O O . X . .]
 [. O X X X . . . . . . . X X O . . . .]
 [. O O O X . . . . . . . . . . . . . .]
 [. . . O X . . . . . . . . . . . X . .]
 [. . . O X . . . . . . . . . O O X O .]
 [. . . X O X . . . O . X . . . X O . O]
 [. . . . O . . . . . . . . . . X O O .]
 [. . O . O . . . . . . . . . X O X X .]
 [. . . . . . . . . . . . . . . O O X .]
 [. . X . O . . . . . . . . . . O . . .]
 [. . . X X . X . . . . . . O O X X . .]
 [. . . . . . . . . . . . . . . . . . .]
 [. . . . . . . . . . . . . . . . . . .]]""")

grid1b = parse_board("""
[[. . . . O . . X . . . . . . . . . . .]
 [. X O . . O X . X . . . . . O O . O .]
 [X O . . O . O X . . O X . X X O X X .]
 [. X X . . . O . . O . X . . . X O O .]
 [. X O . . O . . . . . . . X O X O . .]
 [. . . . . . . . . . . . . X O O X O .]
 [. X . . . . . . . . . . X O O . X . .]
 [. O X X X . . . . . . . X X O . . . .]
 [. O O O X . . . . . . . . . . . . . .]
 [. . . O X . . . . . . . . . . . X . .]
 [. . . O X . . . . . . . . . O O X O .]
 [. . . X O X . . . O . X . . . X O . O]
 [. . . . O . . . . . . . . . . X O O .]
 [. . O . O . . . . . . . . . X O X X .]
 [. . . . . . . . . . . . . . . O O X .]
 [. . X . O . . . . . . . . . . O X . .]
 [. . . X X . X . . . . . . O O X X . .]
 [. . . . . . . . . . . . . . . . . . .]
 [. . . . . . . . . . . . . . . . . . .]]""")

grid1c = parse_board("""
[[. . . . O . . X . . . . . . . . . . .]
 [. X O . . O X . X . . . . . O O . O .]
 [X O . . O . O X . . O X . X X O X X .]
 [. X X . . . O . . O . X . . . X O O .]
 [. X O . . O . . . . . . . X O X O . .]
 [. . . . . . . . . . . . . X O O X O .]
 [. X . . . . . . . . . . X O O . X . .]
 [. O X X X . . . . . . . X X O . . . .]
 [. O O O X . . . . . . . . . . . . . .]
 [. . . O X . . . . . . . . . . . X . .]
 [. . . O X . . . . . . . . . O O X O .]
 [. . . X O X . . . O . X . . . X O . O]
 [. . . . O . . . . . . . . . . X O O .]
 [. . O . O . . . . . . . . . X O X X .]
 [. . . . . . . . . . . . . . O O O X .]
 [. . X . O . . . . . . . . . . O X . .]
 [. . . X X . X . . . . . . O O X X . .]
 [. . . . . . . . . . . . . . . . . . .]
 [. . . . . . . . . . . . . . . . . . .]]""")

grid1d = parse_board("""
[[. . . . O . . X . . . . . . . . . . .]
 [. X O . . O X . X . . . . . O O . O .]
 [X O . . O . O X . . O X . X X O X X .]
 [. X X . . . O . . O . X . . . X O O .]
 [. X O . . O . . . . . . . X O X O . .]
 [. . . . . . . . . . . . . X O O X O .]
 [. X . . . . . . . . . . X O O . X . .]
 [. O X X X . . . . . . . X X O . . . .]
 [. O O O X . . . . . . . . . . . . . .]
 [. . . O X . . . . . . . . . . . X . .]
 [. . . O X . . . . . . . . . O O X O .]
 [. . . X O X . . . O . X . . . X O . O]
 [. . . . O . . . . . . . . . . X O O .]
 [. . O . O . . . . . . . . . X O X X .]
 [. . . . . . . . . . . . . X O O O X .]
 [. . X . O . . . . . . . . . . O X . .]
 [. . . X X . X . . . . . . O O X X . .]
 [. . . . . . . . . . . . . . . . . . .]
 [. . . . . . . . . . . . . . . . . . .]]""")

grid1e = parse_board("""
[[. . . . O . . X . . . . . . . . . . .]
 [. X O . . O X . X . . . . . O O . O .]
 [X O . . O . O X . . O X . X X O X X .]
 [. X X . . . O . . O . X . . . X O O .]
 [. X O . . O . . . . . . . X O X O . .]
 [. . . . . . . . . . . . . X O O X O .]
 [. X . . . . . . . . . . X O O . X . .]
 [. O X X X . . . . . . . X X O . . . .]
 [. O O O X . . . . . . . . . . . . . .]
 [. . . O X . . . . . . . . . . . X . .]
 [. . . O X . . . . . . . . . O O X O .]
 [. . . X O X . . . O . X . . . X O . O]
 [. . . . O . . . . . . . . . . X O O .]
 [. . O . O . . . . . . . . . X O X X .]
 [. . . . . . . . . . . . . X O O O X .]
 [. . X . O . . . . . . . . . . O X . .]
 [. . . X X . X . . . . . . O O X X . .]
 [. . . . . . . . . . . . . . . . . . .]
 [. . . . . . . . . . . . . . . . . . .]]""")

grid1f = parse_board("""
[[. . . . O . . X . . . . . . . . . . .]
 [. X O . . O X . X . . . . . O O . O .]
 [X O . . O . O X . . O X . X X O X X .]
 [. X X . . . O . . O . X . . . X O O .]
 [. X O . . O . . . . . . . X O X O . .]
 [. . . . . . . . . . . . . X O O X O .]
 [. X . . . . . . . . . . X O O . X . .]
 [. O X X X . . . . . . . X X O . . . .]
 [. O O O X . . . . . . . . . . . . . .]
 [. . . O X . . . . . . . . . . . X . .]
 [. . . O X . . . . . . . . . O O X O .]
 [. . . X O X . . . O . X . . . X O . O]
 [. . . . O . . . . . . . . . . X O O .]
 [. . O . O . . . . . . . . . X . X X .]
 [. . . . . . . . . . . . . X . . . X .]
 [. . X . O . . . . . . . . . X . X . .]
 [. . . X X . X . . . . . . O O X X . .]
 [. . . . . . . . . . . . . . . . . . .]
 [. . . . . . . . . . . . . . . . . . .]]""")

grid2a = parse_board("""
[[. . . . . . . . . . . . . . . . . . .]
 [. . . . . . X O O . . . . . . . . . .]
 [. . O X . . . X O . . . . O . X . . .]
 [. O . O O . . X O O O X . . . . X . .]
 [. X O X X X . X X X X O O O . O X . .]
 [. O X X O . . . . . . X . . . . . . .]
 [. X O O . . . . . . . . . . . . X . .]
 [X . X . . . . . . . . . . . . . . . .]
 [. X . . . . . . . . . . . . . . . . .]
 [. . . O . . . . . . . . . . . . . . .]
 [. . O . . . . . . . . . . . . . . . .]
 [. . X X . . . . . . . . . . . . . . .]
 [. . . . . . X X . . . . . . . . . . .]
 [. . X . X X O X . . . . . . . . O . .]
 [. O X . O O O O . . O . . . . . O . .]
 [. O O X X O . . . . O X X O . O X . .]
 [. . X O O X X . . X X O O X O . X . .]
 [. O X O . O . . . . O . O X X . . . .]
 [. . . . . . . . . . . O . . . . . . .]]""")

grid2b = parse_board("""
[[. . . . . . . . . . . . . . . . . . .]
 [. . . . . . X O O . . . . . . . . . .]
 [. . O X . . . X O . . . . O . X . . .]
 [. O X O O . . X O O O X . . . . X . .]
 [. X . X X X . X X X X O O O . O X . .]
 [. O X X O . . . . . . X . . . . . . .]
 [. X O O . . . . . . . . . . . . X . .]
 [X . X . . . . . . . . . . . . . . . .]
 [. X . . . . . . . . . . . . . . . . .]
 [. . . O . . . . . . . . . . . . . . .]
 [. . O . . . . . . . . . . . . . . . .]
 [. . X X . . . . . . . . . . . . . . .]
 [. . . . . . X X . . . . . . . . . . .]
 [. . X . X X O X . . . . . . . . O . .]
 [. O X . O O O O . . O . . . . . O . .]
 [. O O X X O . . . . O X X O . O X . .]
 [. . X O O X X . . X X O O X O . X . .]
 [. O X O . O . . . . O . O X X . . . .]
 [. . . . . . . . . . . O . . . . . . .]]""")


if __name__ == '__main__':
	unittest.main()
