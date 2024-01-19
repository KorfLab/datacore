import glob
import os
import sys

from grimoire.genome import Reader

genome = Reader(fasta=sys.argv[1], gff=sys.argv[2])
for chrom in genome:
	xd = {} # expression data
	for f in chrom.ftable.features:
		if f.source == 'RNASeq_splice': xd[f'{f.beg}-{f.end}'] = f.score
	
	for gene in chrom.ftable.build_genes():
		if len(gene.transcripts()) == 0: continue # skip ncRNAs
		if gene.issues: continue # skip genes with obvious oddities
		for tx in gene.transcripts():
			if len(tx.introns) == 0: continue # skip intronless genes
			for intron in tx.introns:
				isig = f'{intron.beg}-{intron.end}'
				if isig in xd: xs = xd[isig]
				else:          xs = 0
				print(tx.id, intron.beg, intron.end, tx.strand, xs, sep='\t')
