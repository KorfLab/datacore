import gzip
import random

pseq = {}
dseq = {}
prox = 400
dist = 2000
size = 50

with gzip.open('../project_imeter/at_ime_master.txt.gz', 'rt') as fp:
	for line in fp.readlines():
		f = line.split()
		beg = int(f[1])
		end = f[2]
		strand = f[3]
		intron = f[-1]
		seq = intron[5:-10]
		if beg < prox:
			for i in range(0, size*3, size):
				sseq = seq[i:i+size]
				if len(sseq) == size:
					pseq[sseq] = True
		if beg > dist:
			for i in range(0, size*3, size):
				sseq = seq[i:i+size]
				if len(sseq) == size:
					dseq[sseq] = True

pseqs = list(pseq.keys())
random.shuffle(pseqs)
dseqs = list(dseq.keys())
random.shuffle(dseqs)

with open('ime50/prox.fa', 'w') as fp:
	i = 0
	for p, d in zip(pseqs, dseqs):
		fp.write(f'>prox-{i}\n{p}\n')
		i += 1

with open('ime50/dist.fa', 'w') as fp:
	i = 0
	for p, d in zip(pseqs, dseqs):
		fp.write(f'>dist-{i}\n{d}\n')
		i += 1


#################
# Negative Sets #
#################

ppool = ''
dpool = ''
apool = ''
for p, d in zip(pseqs, dseqs):
	ppool += p
	dpool += d
	apool += d
	apool += p

# set 1: shuffled prox
with open('ime50/rndp.fa', 'w') as fp:
	for i in range(len(pseqs)):
		s = ''
		for j in range(size):
			s += random.choice(ppool)
		fp.write(f'>rndp-{i}\n{s}\n')
	
# set 2: shuffled dist
with open('ime50/rndd.fa', 'w') as fp:
	for i in range(len(pseqs)):
		s = ''
		for j in range(size):
			s += random.choice(dpool)
		fp.write(f'>rndd-{i}\n{s}\n')

# set 3: shuffled prox + dist (all)
with open('ime50/rnda.fa', 'w') as fp:
	for i in range(len(pseqs)):
		s = ''
		for j in range(size):
			s += random.choice(dpool)
		fp.write(f'>rnda-{i}\n{s}\n')
