import glob
import os
import sys


from grimoire.genome import Reader

# sys.argv[1] should be of the form below
# ../genome_celegans/build/genes


for ff in glob.glob(f'{sys.argv[1]}/*.fa'):
	gf = ff[:-2] + 'gff3'
	genome = Reader(gff=gf, fasta=ff)
	chrom = next(genome) # there is only one in a gene build
	xd = {} # expression data
	for f in chrom.ftable.features:
		if f.source == 'RNASeq_splice': xd[f'{f.beg}-{f.end}'] = f.score
	
	for gene in chrom.ftable.build_genes():
		if len(gene.transcripts()) == 0: continue # skip ncRNAs
		if gene.issues: continue # skip genes with obvious oddities
		for tx in gene.transcripts():
			if len(tx.introns) == 0: continue # skip intronless genes
			for intron in tx.introns:
				iseq = intron.seq_str()
				isig = f'{intron.beg}-{intron.end}'
				if isig in xd: xs = xd[isig]
				else:
					xs = 0
					sys.stderr.write(f'{isig} not found\n')
					
				if intron.strand == '+':
					ib = intron.beg - gene.beg
					ie = intron.end - gene.beg
				else:
					ib = gene.end - intron.end
					ie = gene.end - intron.beg
				print(tx.id, ib, ie, tx.strand, xs, iseq, sep='\t')
				