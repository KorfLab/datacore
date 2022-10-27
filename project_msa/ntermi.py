
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

def ppi(aas):
	match = 0
	total = 0
	for i in range(len(aas)):
		for j in range(i + 1, len(aas)):
			if aas[i] == aas[j]: match += 1
			total += 1
	return match, total

def percent_identity(seqs):
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
		m, t = ppi(aas)
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
	description='not sure')
parser.add_argument('directory', type=str, metavar='<path>',
	help='path to directory of multi-fasta alignment file')
parser.add_argument('--seqs', type=int, required=False, default=5,
	metavar='<int>', help='minimum number of sequences [%(default)i]')
parser.add_argument('--pct', type=float, required=False, default=0.75,
	metavar='<float>', help='minimum pairwise percent identity [%(default).3f]')
parser.add_argument('--met', type=float, required=False, default=0.50,
	metavar='<float>', help='minimum met positioning [%(default).3f]')
arg = parser.parse_args()

orthologs = 0
for filename in os.listdir(arg.directory):
	seq = {}
	for name, s in read_record(f'{arg.directory}/{filename}'):
		seq[name] = s
	orthologs += 1

	# data cleaning
	# prune some of the sequences from the MSA?

	# minimum number of sequences
	num = len(seq)
	if num < arg.seqs: continue
	
	# minimum pairwise percent identity
	pct = percent_identity(list(seq.values()))
	if pct < arg.pct: continue
	
	# minimum agreement on where the first MET is
	mets = find_mets(list(seq.values()))
	best = mets[list(mets.keys())[0]]
	total = sum(list(mets.values()))
	if best/total < arg.met: continue	
	
	# some temporary output
	print(filename, num, pct, mets)

print(orthologs)
