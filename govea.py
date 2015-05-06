from os import path

import re

class SGF(object):
	#for now, just store a list of moves ((row,col) tuples)
	#search for instances of ;B[xx] or ;W[yy], where xx/yy are coord strings like 'qd'
	pat = re.compile(";[B|W]\[(\w*)\]")

	def __init__(self, s):
		self.moves = []

		move_pairs = re.findall(SGF.pat, s)
		print move_pairs
		#e.g. [('qd', ''), ('', 'pp'), ...]
		#FIXME Need to handle handicap games where W plays first
		turn = 0
		for mp in move_pairs:
			move = self._move_from_str(mp[turn])
			#print move
			turn = (turn+1)%2

		#lines = s.split('\n')
		#for li in lines:
		#	if li.startswith(';B[') or li.startswith(';W['):
		#		move = 
		#		print move



	def _move_from_str(self, s):
		#convert e.g. 'ab' to (0, 1)
		#empty string means pass
		if not s:
			return None
		r = ord(s[0]) - 97 #97 is ord('a')
		c = ord(s[1]) - 97
		assert 0 <= r <= 19
		assert 0 <= c <= 19
		return (r, c)

if __name__ == '__main__':
	with open(path.join('sgf', 'Hutoshi4-kghin.sgf')) as f:
		s = f.read()
		sgf = SGF(s)