from os import path
import re
import logging
from collections import defaultdict

B = -1
empty = 0
W = 1
player_to_str = {B:'B', W:'W'}

class Player(object):
	def __init__(self, color, name=None, rank_str=None):
		self.color = color
		self.name = name
		self.rank_str = rank_str

class Move(object):
	def __init__(self, p, s):
		#convert e.g. 'ab' to (r=0, c=1)
		#empty string means pass

		self.p = p
		if s:
			self.r = ord(s[0]) - 97 #97 is ord('a')
			self.c = ord(s[1]) - 97
			assert 0 <= self.r <= 19
			assert 0 <= self.c <= 19
			self.isPass = False
		else:
			#move is a pass.
			self.r = None
			self.c = None
			self.isPass = True

	def __repr__(self):
		ps = player_to_str[self.p]
		if self.isPass:
			return '(%s: Pass)'%ps
		else:
			return '(%s: %d,%d)'%(ps, self.r, self.c)
		

class SGF(object):
	#list of prop, val pairs
	pat = re.compile('([A-Z]{1,2})\[(.*?)(?<!\\\\)\]', re.DOTALL)

	def __init__(self, s):
		prop_val_pairs = re.findall(SGF.pat, s) #FIXME discarding tree structure info!
		prop_dict = defaultdict(list)
		for prop, val in prop_val_pairs:
			prop_dict[prop].append(val)

		#unpack vals of length 1
		for prop, val in prop_dict.iteritems():
			if len(val) == 1:
				prop_dict[prop] = val[0]

		#GM, FF, SZ, KM, PW, PB, WR, BR, DT, RE, HA
		self.game_type = int(prop_dict.get('GM'))
		self.file_format = int(prop_dict.get('FF'))
		self.board_size = int(prop_dict.get('SZ'))
		self.komi = float(prop_dict.get('KM'))

		#sgf.player_w
		pw = prop_dict.get('PW', None)
		pb = prop_dict.get('PB', None)
		wr = prop_dict.get('WR', None)
		br = prop_dict.get('BR', None)
		
		#self.file_format = prop_dict.get('PW', None)
		#self.file_format = prop_dict.get('PB', None)
		#self.file_format = prop_dict.get('WR', None)
		#self.file_format = prop_dict.get('BR', None)

		self.date = prop_dict.get('DT', None)
		self.result = prop_dict.get('RE', None)
		self.handicap = prop_dict.get('HA', 0)

		#print(vars(self))
		

if __name__ == '__main__':
	with open(path.join('sgf', 'Hutoshi4-kghin.sgf')) as f:
		s = f.read()
		sgf = SGF(s)
