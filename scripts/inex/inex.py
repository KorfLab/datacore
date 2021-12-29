#!/usr/bin/env python3

import argparse
import os

from collections import namedtuple

# setup
parser = argparse.ArgumentParser(description='Program returns all introns and exons of a given gene')
# required arguments
parser.add_argument('--fa', required=True, type=str,
	metavar='<path>', help='path to input fasta file containing one gene')
parser.add_argument('--gff', required=True, type=str,
	metavar='<path>', help='path to input gff file')
parser.add_argument('--out', required=True, type=str,
	metavar='<str>', help='output name (file or dir)')
# finalizing
arg = parser.parse_args()

# Obtain sequence
seq = ''
with open(f'{arg.fa}', 'r') as ffh:
	for line in ffh:
		if '>' in line:
			next
		else: seq+=line.strip()

# Locate the gene and its direction
gene_beg = -1
gene_end = -1
ingene = False
counter = 0
direction = '+'
with open(f'{arg.gff}', 'r') as gffh:
	for line in gffh:
		counter+=1
		if ingene == False and line.split()[2] == 'gene':
			ingene = True
			gene_beg = int(line.split()[3]) - 1
			gene_end = int(line.split()[4]) - 1
			if line.split()[6] == '+': direction = '+'
			elif line.split()[6] == '-': direction = '-'
			break

assert direction == '+' or direction == '-', 'gene direction not found'


# Get introns and exons		
Intron = namedtuple('Intron', ['seq','begin','end','reads'])
Exon   = namedtuple('Exon'  , ['seq','begin','end'])
introns = []
exons   = []
with open(f'{arg.gff}', 'r') as gffh:
	for line in gffh:
		#introns
		if line.split()[1] == 'RNASeq_splice':
			ibeg = int(line.split()[3]) - 1
			iend = int(line.split()[4]) - 1
			reads = float(line.split()[5])
			if ibeg >= gene_beg and iend <= gene_end:
				introns.append(Intron(seq[ibeg:iend+1], ibeg+1, iend+1, reads))
		#exons
		if line.split()[1] == 'WormBase' and line.split()[2] == 'exon':
			ebeg = int(line.split()[3]) - 1
			eend = int(line.split()[4]) - 1
			if ebeg >= gene_beg and eend <= gene_end:
				exons.append(Exon(seq[ebeg:eend+1], ebeg+1, eend+1))
				
# Write out 

if os.path.exists(arg.out):
	raise OSError('output dir exists, will not overwrite')
os.mkdir(arg.out)
	
counter = 0
with open(f'{arg.out}/intron.fa', 'w') as fp:
	for intron in introns:
		counter += 1
		fp.write(f'>intron{counter} beg:{intron[1]} end:{intron[2]} reads:{intron[3]} {direction}\n')
		for i in range(0,len(intron[0]),80):
			fp.write(f'{intron[0][i:i+80]}\n')
	
counter = 0		
with open(f'{arg.out}/canonical.intron.fa', 'w') as fp:
	for intron in introns:
		if (direction == '+' and intron[0][0:2] == 'GT' and intron[0][-2:] == 'AG') or (direction == '-' and intron[0][0:2]=='CT' and intron[0][-2:] == 'AC'):
			counter += 1
			fp.write(f'>intron{counter} beg:{intron[1]} end:{intron[2]} reads:{intron[3]} {direction}\n')
			for i in range(0,len(intron[0]),80):
				fp.write(f'{intron[0][i:i+80]}\n')

counter = 0
with open(f'{arg.out}/exon.fa', 'w') as fp:
	for exon in exons:
		counter += 1
		fp.write(f'>exon{counter} beg:{exon[1]} end:{exon[2]} {direction}\n')
		for i in range(0,len(exon[0]),80):
			fp.write(f'{exon[0][i:i+80]}\n')

		
		
		
		
		
		
		
		
		
		
