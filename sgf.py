from os import path
from datetime import datetime
from govea import B, W, Move, Player

"""Classes and utilities for parsing SGF game record files.
SGF stands for Smart Game Format -- specifications here:
http://www.red-bean.com/sgf/
http://www.red-bean.com/sgf/sgf4.html

There are a couple of approaches we could take for parsing SGF files.
I experimented with regexes, e.g.,
pat = re.compile('([A-Z]{1,2})\[(.*?)(?<!\\\\)\]', re.DOTALL)
but ran into trouble with multiple chained AB / AW handicap stone placement.
Also, I wanted to be able to handle arbitrary nesting of variations.
For these reasons, I went with a state-machine-based approach.

This is not intended to be a comprehensive implementation of SGF.
It is solely to extract data for the purposes of training neural nets.
"""

class SGF(object):
	OUTSIDE_BRACKETS, INSIDE_BRACKETS = range(2) #2 possible states of parser

	def __init__(self, f):
		self.filename = f.name
		s = f.read()

		num_chars = len(s)
		current_node = None
		self.base_node = None
		state = SGF.OUTSIDE_BRACKETS
		variation_stack = [] #push a new node when we encounter (, pop when we encounter )
		max_variation_depth = 0 #keep track of stack high-water mark
		prop_name = None
		i = 0
		prev_i = 0 #left edge for string extraction
		while i < num_chars:
			c = s[i]
			if state == SGF.OUTSIDE_BRACKETS:
				#paying attention to the following characters: ( ) [ ;
				if c == '(':
					#creating a new variation
					if current_node is not None:
						variation_stack.append(current_node)
						max_variation_depth = max(max_variation_depth, len(variation_stack))
					prev_i = i
					prop_name = None
				elif c == ';':
					#creating a new node
					if current_node is not None:
						parent_node = current_node
						current_node = Node(parent_node)
						parent_node.add_child(current_node)
					else:
						#creating first node
						self.base_node = Node()
						current_node = self.base_node
					prev_i = i
					prop_name = None
				elif c == '[':
					#parsing a property value to pair with the property name
					possible_names = s[prev_i+1:i].split()
					if len(possible_names) > 0:
						prop_name = possible_names[-1].upper()
					state = SGF.INSIDE_BRACKETS
					prev_i = i
				elif c ==')':
					#ending a variation
					if len(variation_stack) > 0:
						current_node = variation_stack.pop()
					else:
						current_node = None
					prev_i = i
					prop_name = None
			elif state == SGF.INSIDE_BRACKETS:
				#we are looking for a closing bracket which is not escaped with a backslash
				if c ==']' and s[i-1] != '\\':
					prop_val = s[prev_i+1:i]
					assert(prop_name != None) #check that we've recently seen a property name
					current_node.add_property(prop_name, prop_val)
					state = SGF.OUTSIDE_BRACKETS
					prev_i = i
			i += 1
		self.max_variation_depth = max_variation_depth

		
		#GM, FF, SZ, KM, PW, PB, WR, BR, DT, RE, HA
		base_props = self.base_node.props
		self.game_type = int(base_props.get('GM'))
		self.file_format = int(base_props.get('FF'))
		#size can be 'n' or 'xsize:ysize'
		try:
			size = int(base_props.get('SZ'))
			self.board_shape = (size, size)
		except ValueError:
			strs = base_props.get('SZ').split(':')
			self.board_shape = (int(strs[1]), int(strs[0])) #store 
		self.komi = float(base_props.get('KM', 0))

		#sgf.player_w
		pw = base_props.get('PW', None)
		pb = base_props.get('PB', None)
		wr = base_props.get('WR', None)
		br = base_props.get('BR', None)
		self.player_w = Player(W, name=pw, rank=wr)
		self.player_b = Player(B, name=pb, rank=br)
		
		date_str = base_props.get('DT', None)
		if date_str:
			self.date = datetime.strptime('2013-01-11', '%Y-%m-%d').date()
		else:
			self.date = None
		self.result = base_props.get('RE', None)
		self.handicap = int(base_props.get('HA', 0))


		#since SGF can be a tree structure, it's somewhat ambiguous what it means to extract a list of moves.
		#for our purposes, we will always traverse each node's last child
		#(assuming that this will give the longest move list)
		#this should work for the common case of undos / mouse-slips
		moves = []
		n = self.base_node
		while True:
			m = n.move
			if m:
				moves.append(m)
			if n.children:
				n = n.children[-1]
			else:
				break
		self.moves = moves

		#save any stones that were placed initially (for handicap, or otherwise)
		self.initial_moves = []
		for coord_str in base_props.get('AB', []):
			self.initial_moves.append(Move(B, parse_coords(coord_str)))
		for coord_str in base_props.get('AW', []):
			self.initial_moves.append(Move(W, parse_coords(coord_str)))



	def get_moves(self):
		
		moves = []
		n = self.base_node
		while True:
			m = n.move
			if m:
				moves.append(m)
			if n.children:
				n = n.children[-1]
			else:
				break
		return moves


class Node(object):
	def __init__(self, parent=None):
		self.parent = parent
		self.props = dict()
		self.children = []
		self.move = None #a node may or may not have a move associated. base node will not, typically

	def add_child(self, node):
		self.children.append(node)

	def add_property(self, prop_name, prop_val):
		#save most prop_vals as strings, except in a few cases which result in lists
		if prop_name in ['AB', 'AW']: #TODO: others?
			if prop_name in self.props:
				self.props[prop_name].append(prop_val)
			else:
				self.props[prop_name] = [prop_val]
		else:
			self.props[prop_name] = prop_val
			if prop_name == 'W':
				self.move = Move(W, parse_coords(prop_val))
			elif prop_name == 'B':
				self.move = Move(B, parse_coords(prop_val))

	def __repr__(self, indent=0):
		#return string tree-structure with nested indentation
		spacer = ' '*indent
		children_str = '\n'.join([c.__repr__(indent+2) for c in self.children])
		return '%s%s\n%s' % (spacer, self.props.items(), children_str)




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


if __name__ == '__main__':
	fn = 'Hutoshi4-kghin.sgf'
	#fn = 'variation_test.sgf'
	#fn = 'variation_test2.sgf'
	with open(path.join('data', 'sgf', fn)) as f:
		sgf = SGF(f)
		#print sgf.base_node
		print sgf.moves