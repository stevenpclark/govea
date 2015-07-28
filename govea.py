B = -1
W = 1
EMPTY = 0

color_to_str = {B:'B', W:'W'}
str_to_color = {'B':B, 'W':W}

def opposite_color(c):
	return -c

def rank_str_to_num(s):
	"""input str is either <n>k, <n>d, or <n>p.
	e.g. 23k, 3d, 9p.
	<n>k -> -n
	<n>d -> n
	<n>p -> n+10
	This is somewhat subjective, but lets us at least compare ranks."""
	if s is None:
		return -35 #TODO: what to do about unspecified ranks?
	n = int(s[0:-1])
	c = s[-1]
	if c == 'k':
		return -n
	elif c == 'd':
		return n
	elif c == 'p':
		return n+10
	else:
		raise ValueError('rank final char needs to be one of [k,d,p]')


class Player(object):
	def __init__(self, color, name=None, rank_str=None):
		self.color = color
		self.name = name
		self.rank_str = rank_str
		self.rank_num = rank_str_to_num(rank_str)

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


