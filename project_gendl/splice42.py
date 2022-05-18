import gzip
import random
import subprocess
import sys

def get_acceptors(filename):
	accs = []
	with gzip.open(filename, 'rt') as fp:
		for line in fp.readlines():
			(exon1, intron, exon2, expression, gene) = line.split()
			s1 = intron[-22:-2]
			s2 = intron[-2:]
			s3 = exon2[0:20]
			accs.append((s1, s2, s3, expression))
	random.shuffle(accs)
	return accs


def get_donors(filename):
	dons = []
	with gzip.open(filename, 'rt') as fp:
		for line in fp.readlines():
			(exon1, intron, exon2, expression, gene) = line.split()
			s1 = exon1[-20:]
			s2 = intron[0:2]
			s3 = intron[2:22]
			dons.append((s1, s2, s3, expression))
	return dons

def write_fasta(filename, name, seqs):
	with open(filename, 'w') as fp:
		n = 1
		for s1, s2, s3, x in seqs:
			fp.write(f'>{name}-{n} {x}\n')
			fp.write(f'{s1}{s2}{s3}\n')
			n += 1

def randomseq(size, contents='ACGT'):
	seq = ''
	for i in range(size):
		seq += random.choice(contents)
	return seq

def make_negative1(seqs):
	neg = []
	for i in range(len(seqs)):
		s1 = randomseq(20)
		s2 = seqs[0][1] # either GT or AG
		s3 = randomseq(20)
		x = 0
		neg.append((s1, s2, s3, x))
	return neg

def make_negative2(seqs):
	s1seq = '' # composition of part 1
	s3seq = '' # composition of part 2
	for s1, s2, s3, x in seqs:
		s1seq += s1
		s3seq += s3

	neg = []
	for i in range(len(seqs)):
		s1 = randomseq(20, s1seq)
		s2 = seqs[0][1] # either GT or AG
		s3 = randomseq(20, s3seq)
		x = 0
		neg.append((s1, s2, s3, x))
	return neg

def make_negative3(seqs):
	col1 = [[] for i in range(20)]
	col3 = [[] for i in range(20)]
	for s1, s2, s3, x in seqs:
		for i in range(20):
			col1[i].append(s1[i])
			col3[i].append(s3[i])

	neg = []
	for i in range(len(seqs)):
		s1 = ''
		s3 = ''
		for j in range(20):
			s1 += random.choice(col1[j])
			s3 += random.choice(col3[j])
		s2 = seqs[0][1] # either GT or AG
		x = 0
		neg.append((s1, s2, s3, x))
	return neg


#############
# 42 nt set # 20 nt upstream and downstream of canonical GT|AG
#############

genomes = ('at', 'ce', 'dm')

for gen in genomes:
	# observed
	eie = f'eie.{gen}.txt.gz'
	dons = get_donors(eie)
	accs = get_acceptors(eie)
	write_fasta(f'splice42/{gen}.don.fa', 'don', dons)
	write_fasta(f'splice42/{gen}.acc.fa', 'acc', accs)

	# negative 1 - totally random
	nd = make_negative1(dons)
	na = make_negative1(accs)
	write_fasta(f'splice42/{gen}.n1don.fa', 'n1don', nd)
	write_fasta(f'splice42/{gen}.n1acc.fa', 'n1acc', na)

	# negative 2 - compositional but not positional
	nd = make_negative2(dons)
	na = make_negative2(accs)
	write_fasta(f'splice42/{gen}.n2don.fa', 'n2don', nd)
	write_fasta(f'splice42/{gen}.n2acc.fa', 'n2acc', na)

	# negative 3 - compositional and positional
	nd = make_negative3(dons)
	na = make_negative3(accs)
	write_fasta(f'splice42/{gen}.n3don.fa', 'n3don', nd)
	write_fasta(f'splice42/{gen}.n3acc.fa', 'n3acc', na)
