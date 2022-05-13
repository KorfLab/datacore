#!/usr/bin/env python3

import argparse
import glob

from grimoire.genome import Reader

#######
# CLI #
#######

parser = argparse.ArgumentParser(
	description='dataset builder for gendl project')
parser.add_argument('genes', type=str, metavar='<genes dir>',
	help='path to gene build directory')
parser.add_argument('--minexon', type=int, metavar='<int>', default=50,
	required=False, help='minimum exon length [%(default)i]')
parser.add_argument('--minintron', type=int, metavar='<int>', default=40,
	required=False, help='maximum intron length [%(default)i]')
parser.add_argument('--maxintron', type=int, metavar='<int>', default=150,
	required=False, help='maximum intron length [%(default)i]')
arg = parser.parse_args()


########
# Main #
########
eie = {}
for ff in glob.glob(f'{arg.genes}/*.fa'):
	gf = ff[:-2] + 'gff3'

	genome = Reader(gff=gf, fasta=ff)
	chrom = next(genome)
	genes = len([None for f in chrom.ftable.features if f.type == 'gene'])
	gene = chrom.ftable.build_genes()[0]

	expression = {}
	for f in chrom.ftable.features:
		if f.source == 'RNASeq_splice':
			expression[(f.beg, f.end)] = str(int(f.score))

	# exon-intron-exon data set
	for tx in gene.transcripts():
		if tx.issues: break
		for i in range(1, len(tx.exons)):
			exon1 = tx.exons[i-1]
			exon2 = tx.exons[i]
			intron = tx.introns[i-1]
			exp = None
			sig = (intron.beg, intron.end)
			if sig in expression: exp = expression[sig]
			if exp is None: continue
			if exon1.length < arg.minexon: continue
			if exon2.length < arg.minexon: continue
			if intron.length < arg.minintron: continue
			if intron.length > arg.maxintron: continue
			stuff = (exon1.seq_str()[-50:], intron.seq_str(),
				exon2.seq_str()[0:50], exp)
			eie[stuff] = gene.id

for thing in eie:
	(e1, i, e2, s) = thing
	name = eie[thing]
	print(e1, i, e2, s, name)
