import sys
import os
import argparse

parser = argparse.ArgumentParser(description='decluster sequence sets')
parser.add_argument('fasta', type=str, metavar='<file>',
	help='path to fasta file to de declustered')
parser.add_argument('--percent', required=False, type=float, default=70.0,
	metavar='<float>',	help='percent similarity [%(default).2f]')
parser.add_argument('--out', required=False, type=str, default='dclust.output',
	metavar='<path>',	help='output file name [dclust.output]')
arg = parser.parse_args()

ff = arg.fasta
limit = arg.percent
outfile = arg.out
tmpfile = f'tmp.{os.getpid()}.out'


os.system(f'makeblastdb -in {ff} -dbtype nucl')
os.system(f'blastn -query {ff} -db {ff} -outfmt 6 > {tmpfile}')

pair = {}
kill = {}
with open(tmpfile) as fp:
	for line in fp.readlines():
		f = line.split()
		q, s = f[0], f[1]
		if q == s: continue
		if float(f[2]) < limit: continue
		if q not in pair:
			pair[q] = {}
		pair[q][s] = True

with open(outfile, 'w') as fh:
	for q in pair:
		if q in kill: continue
		fh.write(f'{q}\n')
		kill[q] = True
		for s in pair[q]: kill[s] = True

os.system(f'rm {tmpfile} {ff}.*')
