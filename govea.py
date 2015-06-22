B = -1
W = 1
EMPTY = 0

color_to_str = {B:'B', W:'W'}
str_to_color = {'B':B, 'W':W}

def opposite_color(c):
	return -c

class Player(object):
	def __init__(self, color, name=None, rank=None):
		self.color = color
		self.name = name
		self.rank = rank

	def __repr__(self):
		return '%s: %s [%s]' % (color_to_str[self.color], self.name, self.rank)


class Move(object):
	def __init__(self, color, coord):
		#coord is a (row, col) tuple, or None if the move is a Pass
		self.color = color
		if coord:
			self.r, self.c = coord
		else:
			self.r = self.c = None

	def is_pass(self):
		return self.r == None

	def __repr__(self):
		cs = color_to_str[self.color]
		if self.is_pass():
			return '(%s: Pass)'%cs
		else:
			return '(%s: %d,%d)'%(cs, self.r, self.c)

	def __eq__(self, other):
		return self.color == other.color and self.r == other.r and self.c == other.c


