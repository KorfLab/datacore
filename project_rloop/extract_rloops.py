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

parser = argparse.ArgumentParser(description='Extract rloops')
parser.add_argument('fasta', type=str, metavar='<fasta>', help='fasta file')
parser.add_argument('bed', type=str, metavar='<bed>', help='bed file')
parser.add_argument('--blacklist', required=False, type=str,
	metavar='<file>', help='use named black list file')
parser.add_argument('--window', required=False, type=int, default=100,
	metavar='<int>', help='window size [%(default)i]')
parser.add_argument('--depth', required=False, type=int, default=10,
	metavar='<int>', help='minimum depth [%(default)i]')
parser.add_argument('--noisy', action='store_true',
	help='print status messages to stderr]')
arg = parser.parse_args()

#############
# Get Peaks #
#############

peaks = {}
cli = f'python3 wtf.py --window {arg.window} --depth {arg.depth} {arg.bed}'
if arg.blacklist: cli += f' --blacklist {arg.blacklist}'
if arg.noisy: print(cli, file=sys.stderr)
for line in subprocess.run(cli, shell=True, capture_output=True)\
		.stdout.decode().split('\n'):
	if len(line) == 0: continue
	c, b, e, n = line.split()
	if c not in peaks: peaks[c] = []
	peaks[c].append( (int(b), int(e)) )

############
# Get Seqs #
############
sid = 1
for chrom, seq in read_fasta(arg.fasta):
	if '_' in chrom: break # not bothering with those weird chroms or MT
	if arg.noisy: print(f'processing {chrom}', file=sys.stderr)
	seq = seq.upper()
	for beg, end in peaks[chrom]:
		sseq = seq[beg-1:end]
		print(f'>seq-{sid}\n{sseq}')
		sid += 1
