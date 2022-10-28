
import argparse
import gzip
import os
import re
import statistics
import sys

def read_record(filename):

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

def pairwise(aas):
	match = 0
	total = 0
	for i in range(len(aas)):
		for j in range(i + 1, len(aas)):
			if aas[i] == aas[j]: match += 1
			total += 1
	return match, total

def ppi(seqs):
	pct = []
	seqlen = len(seqs[0])
	match = 0
	total = 0
	for i in range(seqlen):
		aas = []
		for j in range(len(seqs)):
			aa = seqs[j][i]
			if aa == '-': continue
			aas.append(aa)
		m, t = pairwise(aas)
		match += m
		total += t
	return match / total

def find_mets(seqs):
	first_met = {}
	for seq in seqs:
		match = re.search('^(\-*M)', seq)
		if match:
			pos = len(match.group(1))
			if pos not in first_met: first_met[pos] = 0
			first_met[pos] += 1

	first_met = {k: v for k, v in sorted(first_met.items(),
		key=lambda item: item[1], reverse=True)}

	return first_met

parser = argparse.ArgumentParser(
	description='some kind of n-terminal analysis program')
parser.add_argument('directory', type=str, metavar='<path>',
	help='path to directory of multi-fasta alignment file')
parser.add_argument('--key', type=int, required=False,
	metavar='<int>', help='key organism id (e.g. 6239)')
parser.add_argument('--seqs', type=int, required=False, default=5,
	metavar='<int>', help='minimum number of sequences [%(default)i]')
parser.add_argument('--pct', type=float, required=False, default=0.75,
	metavar='<float>', help='minimum pairwise percent identity [%(default).3f]')
parser.add_argument('--met', type=float, required=False, default=0.50,
	metavar='<float>', help='minimum met agreement [%(default).3f]')
parser.add_argument('--off', type=int, required=False, default=3,
	metavar='<int>', help='minimum met offset [%(default)i]')
parser.add_argument('--adj', type=int, required=False, default=15,
	metavar='<int>', help='adjacent sequence to display [%(default)i]')
arg = parser.parse_args()

for filename in os.listdir(arg.directory):
	seqs = {}
	for name, s in read_record(f'{arg.directory}/{filename}'):
		seqs[name] = s

	# key species requirement?
	if arg.key:
		species = {}
		for name in seqs:
			f = name.split('.')
			species[int(f[0])] = True
		if arg.key not in species: continue

	# number of sequences in alignment
	num = len(seqs)
	if num < arg.seqs: continue

	# agreement on where the first MET is
	mets = find_mets(list(seqs.values()))
	best_pos = next(iter(mets))
	best_val = mets[best_pos]
	met_freq = best_val / num
	if met_freq < arg.met: continue
	if best_pos < arg.off: continue

	# pairwise percent identity
	pct = ppi(list(seqs.values()))
	if pct < arg.pct: continue

	# find the n-terminal outliers
	marker = ' ' * (best_pos -2)
	print(filename, pct, num, best_pos, num, best_val)
	print(marker, '*')
	for name, seq in seqs.items():
		print(seq[0:best_pos+15], name)
	print()
