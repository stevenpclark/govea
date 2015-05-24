from os import path
import unittest
from datetime import datetime

from sgf import SGF

class SGFTestCase(unittest.TestCase):
	"""Tests for 'sgf.py'."""

	def test_sgf_load(self):
		"""Test ability to correctly load and parse important SGF info"""

		with open(path.join('sgf', 'Hutoshi4-kghin.sgf')) as f:
			s = f.read()
			sgf = SGF(s)
			#Test some header fields.
			#Namely: GM, FF, SZ, KM, PW, PB, WR, BR, DT, RE, HA
			self.assertTrue(sgf.game_type == 1)
			self.assertTrue(sgf.file_format == 4)
			self.assertTrue(sgf.board_size == 19)
			self.assertTrue(sgf.komi == 6.5)
			self.assertTrue(sgf.player_w.name == "Hutoshi4")
			self.assertTrue(sgf.player_b.name == "kghin")
			self.assertTrue(sgf.player_w.rank == "8d")
			self.assertTrue(sgf.player_b.rank == "9d")
			expected_date = datetime.strptime("2013-01-11", "%Y-%m-%d").date()
			self.assertTrue(sgf.date == expected_date)
			self.assertTrue(sgf.result == "W+1.50")
			self.assertTrue(sgf.handicap == 0)


if __name__ == '__main__':
	unittest.main()