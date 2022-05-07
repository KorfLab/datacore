import argparse
import gzip
import sys


def find_peaks(chunk, w, d):
	print(chunk) # debug

	# check length of chunk
	offset = chunk[0][1]
	last = chunk[-1][2]
	if (last - offset < w):
		print('chunk too short, skipping', last - offset, w)
		return []

	# create coverage over chunk
	cov = [0] * (last - offset)
	for c, b, e, v in chunk:
		for i in range(b, e):
			idx = i - offset
			cov[i-offset] = v

	# find first value >= d
	start = None
	for i, v in enumerate(cov):
		if v >= d:
			start = i
			break
	if start is None:
		print('chunk has no values >= d, skipping')
		return []

	# find last value >= d
	end = None
	for i in range(len(cov)-1, -1, -1):
		if cov[i] >= d:
			end = i + 1
			break
	if end - start < w:
		print('span too short, skipping', end - start, w)
		return []

	# there is some window in here worth reporting, possibley several
	pbeg = start
	pend = start
	for i in range(start, end -w +1):
		win = chunk[i:i+w]
		s = 0
		for c, b, e, v in win: s += v
		ave = s / w
		if ave >= d:
			pend = d
		else:
			print(pbeg, pend)



parser = argparse.ArgumentParser(description='Window-based peak finder')
parser.add_argument('bed', type=str, metavar='<bedfile>',
	help='path to bed file')
parser.add_argument('--blacklist', required=False, type=str,
	metavar='<path>', help='list of regions to ignore')
parser.add_argument('--window', required=False, type=int, default=100,
	metavar='<int>', help='window size [%(default)i]')
parser.add_argument('--depth', required=False, type=int, default=10,
	metavar='<int>', help='minimum read depth [%(default)i]')
arg = parser.parse_args()

if arg.bed.endswith('.gz'): fp = gzip.open(arg.bed, 'rt')
else:                       fp = open(arg.bed)

# separate into chunks of windowsize
chunk_chrom = None
chunk_start = 1 # starting coordinate
chunk_end = 1
chunk = []
while True:
	line = fp.readline()
	if line == '': break
	if line.startswith('#'): continue
	if line.startswith('\n'): continue
	chrom, beg, end, cov = line.split()
	cov = float(cov)
	beg = int(beg)
	end = int(end)
	gap = beg - chunk_end
	print('read', chrom, beg, end, cov)
	if chunk_chrom != chrom or gap > arg.window:
		# finish previous chunk
		if len(chunk) > 0: find_peaks(chunk, arg.window, arg.depth)

		# start new chunk
		chunk_chrom = chrom
		chunk_start = beg
		chunk_end = end
		chunk = []
		chunk.append( (chrom, beg, end, cov) )
	else:
		chunk_end = end
		chunk.append( (chrom, beg, end, cov) )
find_peaks(chunk, arg.window, arg.depth)

