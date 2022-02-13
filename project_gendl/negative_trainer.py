import argparse
import gzip
import random
import sys


from grimoire.toolbox import random_dna, read_fasta

## CLI
parser = argparse.ArgumentParser(description='negative sequence trainer')
parser.add_argument('fasta', type=str, metavar='<file>',
	help="name of fasta file of observations")
parser.add_argument('--size', required=False, type=int, metavar='<int>',
	default=100, help="sequence length")
parser.add_argument('--count', required=False, type=int, metavar='<int>',
	default=20, help="number of sequences")
parser.add_argument('--shuffle', required=False, action="store_true",
	help="shuffle instead of generate")
parser.add_argument('--seed', required=False, type=int, metavar='<int>',
	help="set random seed")
arg = parser.parse_args()

if arg.seed: random.seed(arg.seed)

a = 0
c = 0
g = 0
t = 0
for name, seq in read_fasta(arg.fasta):
	if arg.shuffle:
		shuff = list(seq)
		random.shuffle(shuff)
		print(f'>{name} shuffled')
		seq = ''.join(shuff)
		for i in range(0, len(seq), 80):
			print(seq[i:i+80])
	else:
		a += seq.count('A')
		c += seq.count('C')
		g += seq.count('G')
		t += seq.count('T')

total = a + c + g + t
a /= total
c /= total
g /= total
t /= total
if not arg.shuffle:
	for i in range(arg.count):
		seq = random_dna(arg.size, a=a, c=c, g=g, t=t)
		print(f'>seq{i}')
		for i in range(0, len(seq), 80):
			print(seq[i:i+80])
