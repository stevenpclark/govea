import pattern
from utils import get_sgf_paths
from sgf import SGF
from gogame import GoGame

def is_acceptable_sgf(sgf):
	if sgf.handicap > 2:
		return False
	if sgf.player_b.rank_num < 5 or sgf.player_w.rank_num < 5:
		return False
	return True

def extract_patterns(max_num_patterns=1e9, exploit_symmetry=True):
	sgf_paths = get_sgf_paths()
	print '%d sgf files detected' % len(sgf_paths)
	
	patterns = []
	num_skipped_sgf = 0
	num_games_parsed = 0

	for p in sgf_paths:
		sgf = SGF(file(p))
		if not is_acceptable_sgf(sgf):
			num_skipped_sgf += 1
			continue
		game = GoGame(sgf)
		num_games_parsed += 1
		patterns.extend(pattern.get_all_game_patterns(game, exploit_symmetry=exploit_symmetry))
		if len(patterns) >= max_num_patterns:
			break
	patterns = patterns[:max_num_patterns]

	print '%d patterns extracted' % (len(patterns))
	print '%d games parsed' % num_games_parsed
	print '%d sgf skipped' % num_skipped_sgf

	return patterns


if __name__ == '__main__':
	patterns = extract_patterns(100000)
