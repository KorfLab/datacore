import argparse
import gzip
import sys

def find_peaks(chrom, chunk, w, d):

	offset = chunk[0][1]
	last = chunk[-1][2]
	cov = [0] * (last - offset)
	for c, b, e, v in chunk:
		for i in range(b, e):
			idx = i - offset
			cov[i-offset] = v

	stopped here, use faster algorithm
	pbeg = None
	pend = None
	for i in range(0, end -w +1):
		win = cov[i:i+w]
		ave = sum(win) / w
		if ave >= d:
			if pbeg is None and cov[i] >= d: pbeg = i
			if i+w < len(cov) and cov[i+w] >= d: pend = i+w
		else:
			if pbeg is not None and pend is not None and pend - pbeg + 1 >= w:
				yield (chrom, pbeg + offset, pend + offset, ave)
			pbeg = None
			pend = None
	if pbeg is not None and pend is not None and pend - pbeg + 1 >= w:
		yield (chrom, pbeg + offset, pend + offset, ave)

def overlap(peak, blacklist):
	chrom = peak[0]
	beg = peak[1]
	end = peak[2]
	if chrom not in blacklist: return 0
	for b, e in blacklist[chrom]:
		if b >= beg and b <= end: return 1
		if e >= beg and e <= end: return 1
		if b <= beg and e >= end: return 1
	return 0

def output(peak):
	print(peak[0], peak[1], peak[2], peak[3])

"""
+ Average depth of the window must be >= threshold
+ Window may be reported at less than W however
"""

parser = argparse.ArgumentParser(description='Windowing threshold finder')
parser.add_argument('bed', type=str, metavar='<bedfile>',
	help='path to bed file')
parser.add_argument('--blacklist', required=False, type=str,
	metavar='<path>', help='list of regions to ignore')
parser.add_argument('--window', required=False, type=int, default=100,
	metavar='<int>', help='window size [%(default)i]')
parser.add_argument('--depth', required=False, type=int, default=10,
	metavar='<int>', help='minimum read depth [%(default)i]')
#parser.add_argument('--json', action='store_true', help='output in json')
arg = parser.parse_args()

# get blacklist if there is one
blacklist = {}
if arg.blacklist:
	with open(arg.blacklist) as fp:
		for line in fp.readlines():
			if line.startswith('#'): continue
			if line.startswith('\n'): continue
			f = line.split()
			chrom = f[0]
			beg = int(f[1])
			end = int(f[2])
			if chrom not in blacklist: blacklist[chrom] = []
			blacklist[chrom].append( (beg, end) )

if arg.bed.endswith('.gz'): fp = gzip.open(arg.bed, 'rt')
else:                       fp = open(arg.bed)

# separate into chunks of windowsize
chunk_chrom = None
chunk_start = 1
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
	if chunk_chrom != chrom or gap > arg.window:
		# finish previous chunk
		if len(chunk) > 0:
			for peak in find_peaks(chrom, chunk, arg.window, arg.depth):
				if overlap(peak, blacklist): continue
				output(peak)
		# start new chunk
		chunk_chrom = chrom
		chunk_start = beg
		chunk_end = end
		chunk = []
		chunk.append( (chrom, beg, end, cov) )
	else:
		chunk_end = end
		chunk.append( (chrom, beg, end, cov) )

# report last chunk
for peak in find_peaks(chrom, chunk, arg.window, arg.depth):
	if overlap(peak, blacklist): continue
	output(peak)
