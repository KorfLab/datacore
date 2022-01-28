#!/usr/bin/env python3

import sys
import os

from grimoire.genome import Reader

# APC requires
# short genes
# highly expressed
# introns
# protein-coding
# not weird


root = '../genome_celegans/build/genes'
MINX = 100000 # minimum RNASeq_splice value

fa  = open('apc.fa', 'w')
gff = open('apc.gff', 'w')

for d in os.listdir(root):
	n = d[4:]
	ff = f'{root}/{d}/{n}.fa'
	gf = f'{root}/{d}/{n}.gff'
	
	genome = Reader(gff=gf, fasta=ff)
	chrom = next(genome) # there is only one in a gene build
	if len(chrom.seq) > 1200: continue # short genes only
	
	for gene in chrom.ftable.build_genes():
		if len(gene.transcripts()) == 0: continue # skip ncRNAs
		if gene.issues: continue # skip genes with obvious oddities
		
		# expression
		maxexp = 0
		for f in chrom.ftable.features:
			if f.source == 'RNASeq_splice' and f.score > maxexp:
				maxexp = f.score
		if maxexp < MINX: continue
		
		# intron counts
		max_introns = 0
		for tx in gene.transcripts():
			if len(tx.introns) > max_introns: max_introns = len(tx.introns)
		if max_introns == 0: continue

		# write
		fa.write(f'{chrom}')
		gff.write(f'{gene}')

fa.close()
gff.close()
