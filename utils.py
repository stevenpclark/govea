from os import path
import glob

def get_sgf_paths():
	my_dir = path.dirname(__file__)
	sgf_dir = path.join(my_dir, 'data', 'sgf')
	paths = []
	#get the ones in the base dir:
	paths.extend(glob.glob(path.join(sgf_dir, '*.sgf')))
	paths.extend(glob.glob(path.join(sgf_dir, '*', '*.sgf')))
	return paths

if __name__ == '__main__':
	print(len(get_sgf_paths()))
