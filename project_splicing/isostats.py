import argparse
import os
import seqlib
import sys
import time

parser = argparse.ArgumentParser(description='Get stats on isoforms')
parser.add_argument('apc', type=str,
	metavar='<apc>', help='path to apc program')
parser.add_argument('fasta', type=str,
	metavar='<fasta>', help='path to fasta file')
arg = parser.parse_args()

for name, seq in seqlib.read_fasta(arg.fasta):
	with open('temp.fa', 'w') as fp:
		fp.write(f'>{name}\n{seq}\n')
	t0 = time.time()
	os.system(f'{arg.apc} temp.fa | head -7 > temp.out')	
	t1 = time.time()
	t = t1 - t0
	
	with open('temp.out') as fp:
		lines = fp.readlines()
		name = lines[0].split()[2]
		nts  = lines[1].split()[2]
		dons = lines[2].split()[2]
		accs = lines[3].split()[2]
		isos = lines[5].split()[2]
	
	print(f'{name}\t{nts}\t{dons}\t{accs}\t{isos}\t{t:.2f}')
