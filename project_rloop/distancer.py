import argparse
import gzip
import math
import subprocess
import sys

#########
# funcs #
#########

def read_fasta(filename):

	label = None
	seq = []

	fp = None
	if    filename == '-':         fp = sys.stdin
	elif filename.endswith('.gz'): fp = gzip.open(filename, 'rt')
	else:                          fp = open(filename)

	while True:
		line = fp.readline()
		if line == '': break
		line = line.rstrip()
		if line.startswith('>'):
			if len(seq) > 0:
				seq = ''.join(seq)
				yield(label, seq)
				label = line[1:]
				seq = []
			else:
				label = line[1:]
		else:
			seq.append(line)
	yield(label, ''.join(seq))
	fp.close()

def manhattan(P, Q):
	d = 0
	for kmer in P:
		d += abs(P[kmer] - Q[kmer])
	return d

def kld(P, Q):
	d = 0
	for kmer in P:
		d += P[kmer] * math.log2(P[kmer]/Q[kmer])
	return d

def revcomp(seq):
	comp = str.maketrans('ACGTRYMKWSBDHVN', 'TGCAYRKMWSVHDBN')
	anti = seq.translate(comp)[::-1]
	return anti

#######
# CLI #
#######

parser = argparse.ArgumentParser(
	description='Experiments in k-mer distances')
parser.add_argument('fasta', type=str, metavar='<fasta>',
	help='fasta file')
parser.add_argument('files', type=str, nargs='+', metavar='<bed>',
	help='bed files')
parser.add_argument('--blacklist', required=False, type=str,
	metavar='<file>', help='use named black list file')
parser.add_argument('--window', required=False, type=int, default=100,
	metavar='<int>', help='window size [%(default)i]')
parser.add_argument('--depth', required=False, type=int, default=10,
	metavar='<int>', help='minimum depth [%(default)i]')
parser.add_argument('--kmer', required=False, type=int, default=3,
	metavar='<int>', help='k-mer size [%(default)i]')
parser.add_argument('--anti', action='store_true',
	help='count kmers in both directions')
parser.add_argument('--kld', action='store_true',
	help='use Kullback-Leibler distance [default is Manhattan]')
parser.add_argument('--noisy', action='store_true',
	help='print status messages to stderr]')
arg = parser.parse_args()

#################
# Catalog Peaks #
#################

peaks = {}
for f in arg.files:
	cli = f'python3 wtf.py --window {arg.window} --depth {arg.depth} {f}'
	if arg.blacklist: cli += f' --blacklist {arg.blacklist}'
	if arg.noisy: print(cli, file=sys.stderr)

	for line in subprocess.run(cli, shell=True, capture_output=True)\
			.stdout.decode().split('\n'):
		if len(line) == 0: continue
		c, b, e, n = line.split()
		if f not in peaks: peaks[f] = {}
		if c not in peaks[f]: peaks[f][c] = []
		peaks[f][c].append( (int(b), int(e)) )

###############
# Count Peaks #
###############
count = {}
for chrom, seq in read_fasta(arg.fasta):
	if '_' in chrom: break # not bothering with those weird chroms or MT
	if arg.noisy: print(f'processing {chrom}', file=sys.stderr)
	seq = seq.upper()
	for file in peaks:
		for beg, end in peaks[file][chrom]:
			sseq = seq[beg-1:end]
			if file not in count: count[file] = {}
			for i in range(0, len(sseq) -arg.kmer +1):
				kmer = sseq[i:i+arg.kmer]
				if 'N' in kmer: continue
				if kmer not in count[file]: count[file][kmer] = 0
				count[file][kmer] += 1
			if not arg.anti: continue

			sseq = revcomp(sseq)
			for i in range(0, len(sseq) -arg.kmer +1):
				kmer = sseq[i:i+arg.kmer]
				if 'N' in kmer: continue
				if kmer not in count[file]: count[file][kmer] = 0
				count[file][kmer] += 1

freq = {}
for file in count:
	freq[file] = {}
	tot = 0
	for kmer in count[file]: tot += count[file][kmer]
	for kmer in count[file]: freq[file][kmer] = count[file][kmer] / tot

####################
# Make comparisons #
####################

if arg.kld: distance = kld
else:       distance = manhattan
for i in range(len(arg.files)):
	f1 = arg.files[i]
	if f1 not in freq:
		print(f'{f1} nothing')
		continue
	for j in range(i + 1, len(arg.files)):
		f2 = arg.files[j]
		if f2 not in freq:
			print(f'{f2} nothing')
			continue
		print(f1, f2, distance(freq[f1], freq[f2]))

