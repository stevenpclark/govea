from os import path
import re
import logging
from collections import defaultdict
from datetime import datetime
from govea import B, W, Move, Player


def parse_coords(s):
	#sgf coords are stored as xy chars whereas we store (row, col)
	#e.g. convert s='ab' to (r=1, c=0)
	#empty string means pass (return None in this case)

	if s:
		r = ord(s[1]) - 97 #97 is ord('a')
		c = ord(s[0]) - 97
		assert 0 <= r <= 19
		assert 0 <= c <= 19
		return (r,c)
	else:
		#move is a pass.
		return None
		

class SGF(object):
	#FIXME currently discarding tree structure info!
	#this will cause trouble for any games that have undos, etc.

	#list of prop, val pairs:
	pat = re.compile('([A-Z]{1,2})\[(.*?)(?<!\\\\)\]', re.DOTALL)

	def __init__(self, s):
		self.moves = []
		prop_val_pairs = re.findall(SGF.pat, s)
		prop_dict = defaultdict(list)
		for prop, val in prop_val_pairs:
			prop_dict[prop].append(val)
			#keep moves interleaved in proper order
			if prop == 'W':
				self.moves.append(Move(W, parse_coords(val)))
			if prop == 'B':
				self.moves.append(Move(B, parse_coords(val)))

		#unpack vals of length 1
		for prop, val in prop_dict.iteritems():
			if len(val) == 1:
				prop_dict[prop] = val[0]

		#GM, FF, SZ, KM, PW, PB, WR, BR, DT, RE, HA
		self.game_type = int(prop_dict.get('GM'))
		self.file_format = int(prop_dict.get('FF'))
		#size can be 'n' or 'xsize:ysize'
		try:
			size = int(prop_dict.get('SZ'))
			self.board_shape = (size, size)
		except ValueError:
			strs = prop_dict.get('SZ').split(':')
			self.board_shape = (int(strs[1]), int(strs[0])) #store 
		self.komi = float(prop_dict.get('KM'))

		#sgf.player_w
		pw = prop_dict.get('PW', None)
		pb = prop_dict.get('PB', None)
		wr = prop_dict.get('WR', None)
		br = prop_dict.get('BR', None)
		self.player_w = Player(W, name=pw, rank=wr)
		self.player_b = Player(B, name=pb, rank=br)
		
		date_str = prop_dict.get('DT', None)
		if date_str:
			self.date = datetime.strptime('2013-01-11', '%Y-%m-%d').date()
		else:
			self.date = None
		self.result = prop_dict.get('RE', None)
		self.handicap = prop_dict.get('HA', 0)


	


if __name__ == '__main__':
	with open(path.join('sgf', 'Hutoshi4-kghin.sgf')) as f:
		s = f.read()
		sgf = SGF(s)
