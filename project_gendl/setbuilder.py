import gzip
import random
import subprocess

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


genomes = ('at', 'ce', 'dm')


#############
# 42 nt set # 21 nt upstream and downstream of canonical GT|AG
#############

for gen in genomes:
	eie = f'eie.{gen}.txt.gz'
	dons = get_donors(eie)
	accs = get_acceptors(eie)
	write_fasta(f'data/{gen}.don.fa', 'don', dons)
	write_fasta(f'data/{gen}.acc.fa', 'acc', accs)

