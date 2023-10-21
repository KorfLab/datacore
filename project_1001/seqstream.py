import argparse
import gzip
import os

class SeqLineReader():
	def __init__(self, filename):
		self.filename = filename
		self.uid = None
		self.off = 0
		self.fp = None
		if   filename.endswith('.gz'): self.fp = gzip.open(filename, 'rt')
		elif filename == '-':          self.fp = sys.stdin
		else:                          self.fp = open(filename)
	
	def __iter__(self):
		for line in self.fp:
			if line.startswith('>'):
				f = line.split()
				self.uid = f[0][1:]
			else:
				seq = line.rstrip()
				beg = self.off
				self.off += len(seq)
				end = self.off
				yield self.uid, beg, end, seq
				
parser = argparse.ArgumentParser(description='')
parser.add_argument('path', type=str, metavar='<directory>',
	help='directory of gzipped pseudogenome fasta files')
parser.add_argument('--test', action='store_true')
arg = parser.parse_args()


genomes = []
for (dirpath, dirnames, filenames) in os.walk(arg.path):
	for file in filenames:
		genomes.append(SeqLineReader(f'{dirpath}/{file}'))

if arg.test: files = files[:5]

while True:
	seqs = []
	length = None
	beg = None
	end = None
	for g in genomes:
		try:
			uid, beg, end, seq = next(iter(g))
			if length is None: length = len(seq)
			else:              assert(len(seq) == length)
			seqs.append(seq)
		except StopIteration:
			break

	if length is None: break

	counts = []
	for i in range(length):
		counts.append({'A':0, 'C': 0, 'G': 0, 'T': 0})
	
	for seq in seqs:
		for i in range(len(seq)):
			counts[i][seq[i]] += 1
	
	for i in range(len(counts)):
		out = [f'{beg+1+i}']
		t = sum(counts[i].values())
		for nt in counts[i]:
			counts[i][nt] /= t
			out.append(f'{counts[i][nt]:.3f}')
		print('\t'.join(out))
