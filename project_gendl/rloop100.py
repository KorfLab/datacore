import gzip
import random
import sys

def randgc(n, gc):
	seq = ''
	for i in range(n):
		if random.random() < gc:
			if random.random() < 0.5: seq += 'C'
			else:                   seq += 'G'
		else:
			if random.random() < 0.5: seq += 'A'
			else:                   seq += 'T'
	return seq

def write_fasta(filename, name, seqs):
	with open(filename, 'w') as fp:
		n = 1
		for s in seqs:
			fp.write(f'>{name}-{n}\n')
			fp.write(f'{s}\n')
			n += 1

# positives
obs = []
gc = 0
total = 0
with gzip.open(sys.argv[1], 'rt') as fp:
	for line in fp.readlines():
		for i in range(0, len(line), 100):
			line = line.rstrip()
			seq = line[i:i+100]
			if len(seq) < 100: continue
			if 'N' in seq: continue
			obs.append(seq)
			gc += seq.count('G')
			gc += seq.count('C')
			total += 100
write_fasta('rloop.pos.fa', 'pos', obs)

# negative1 - random sequence
neg = []
for i in range(len(obs)):
	neg.append(randgc(100, 0.5))
write_fasta('rloop.neg1.fa', 'neg1', neg)

# negative2 - GC-biased random sequence
neg = []
for i in range(len(obs)):
	neg.append(randgc(100, gc/total))
write_fasta('rloop.neg2.fa', 'neg2', neg)

# negative3 - negative strand r-loops
comp = str.maketrans('ACGTRYMKWSBDHV', 'TGCAYRKMWSVHDB')
neg = []
for seq in obs:
	anti = seq.translate(comp)[::-1]
	neg.append(anti)
write_fasta('rloop.neg3.fa', 'neg3', neg)

# negative4 - shuffled r-loops
neg = []
for seq in obs:
	seq = list(seq)
	random.shuffle(seq)
	neg.append(''.join(seq))
write_fasta('rloop.neg4.fa', 'neg4', neg)
