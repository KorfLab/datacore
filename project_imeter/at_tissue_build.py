import glob
import os
import sys


from grimoire.genome import Reader

def expression(intron, ftable):
	count = {'aer':0, 'car':0, 'dgs':0, 'lgs':0, 'lea':0, 'pol':0, 'rec':0,
		'ram':0, 'roo':0, 'sam':0, 's12':0}
	for f in ftable.features:	
		if f.beg == intron.beg and f.end == intron.end:
			count[f.id] += f.score
	strings = []
	for k in count:
		strings.append(str(int(count[k])))
	return '\t'.join(strings)

root = '../genome_athaliana/build/genes' # change to full build
for ff in glob.glob(f'{root}/*.fa'):
	gf = ff[:-2] + 'gff3'
	genome = Reader(gff=gf, fasta=ff)
	chrom = next(genome) # there is only one in a gene build
	for gene in chrom.ftable.build_genes():
		if len(gene.transcripts()) == 0: continue # skip ncRNAs
		if gene.issues: continue # skip genes with obvious oddities
		for tx in gene.transcripts():
			if len(tx.introns) == 0: continue # skip intronless genes
			for intron in tx.introns:
				iseq = intron.seq_str()
				xs = expression(intron, chrom.ftable)
				if intron.strand == '+':
					ib = intron.beg - gene.beg
					ie = intron.end - gene.beg
				else:
					ib = gene.end - intron.end
					ie = gene.end - intron.beg
				print(tx.id, ib, ie, tx.strand, xs, iseq, sep='\t')
				
