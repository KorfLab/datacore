import gzip
import math
import subprocess
import sys

# draft, hard-coded version of something...


def distance(P, Q):
	d = 0
	for kmer in P:
		#d += P[kmer] * math.log2(P[kmer]/Q[kmer])
		d += abs(P[kmer] - Q[kmer])
	return d


W = 100 # window size
D = 10  # depth
K = 3   # k-mer size


seq = ''
with gzip.open('chr1.fa.gz', 'rt') as fp:
	for line in fp.readlines():
		seq += line.rstrip().upper()

count = {}
for file in sys.argv[1:]:
	cli = f'python3 wtf.py --window {W} --depth {D} {file}'
	out = subprocess.run(cli, shell=True, capture_output=True).stdout
	for line in out.split(b'\n'):
		if len(line) == 0: continue
		chrom, beg, end, cov = line.decode().split()
		beg = int(beg)
		end = int(end)
		sseq = seq[beg-1:end]

		if file not in count: count[file] = {}
		for i in range(0, len(sseq) -K +1):
			kmer = sseq[i:i+K]
			if kmer not in count[file]: count[file][kmer] = 0
			count[file][kmer] += 1

freq = {}
for file in count:
	freq[file] = {}
	tot = 0
	for kmer in count[file]: tot += count[file][kmer]
	for kmer in count[file]: freq[file][kmer] = count[file][kmer] / tot

for f1 in freq:
	for f2 in freq:
		print(f1, f2, distance(freq[f1], freq[f2]))
