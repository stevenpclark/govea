from os import path
from sgf import SGF

class GoGame(object):
	def __init__(self, sgf):
		pass

class BoardState(object):
	def __init__(self):
		pass


if __name__ == '__main__':
	with open(path.join('sgf', 'Hutoshi4-kghin.sgf')) as f:
		s = f.read()
		sgf = SGF(s)
		game = GoGame(sgf)