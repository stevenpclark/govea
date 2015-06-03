from os import path
import requests
import glob
import subprocess

my_dir = path.dirname(__file__)
output_dir = path.join(my_dir, 'data', 'sgf')

dl_urls = ['http://dl.u-go.net/gamerecords/KGS-2015_04-19-900-.tar.bz2']

if __name__ == '__main__':
	#download all archive files
	#FIXME TODO Error handling
	for url in dl_urls:
		out_fn = path.join(output_dir, url.split('/')[-1])
		r = requests.get(url)
		with open(out_fn, 'wb') as f:
			f.write(r.content)
	print 'downloaded %d files' % len(dl_urls)

	#untar all archives. assume .bz2 format
	#FIXME TODO Error handling
	tarball_paths = glob.glob(path.join(output_dir, '*.tar.bz2'))
	for tbp in tarball_paths:
		fn = path.basename(tbp)
		subprocess.check_call(['tar', '-xjf', fn], cwd=output_dir)
	print 'unpacked %d files' % len(tarball_paths)