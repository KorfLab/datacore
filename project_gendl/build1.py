import argparse
import os

from grimoire.genome import Reader

## CLI
parser = argparse.ArgumentParser(description="exon-intron data builder")
parser.add_argument("build_dir", type=str, metavar='<dir>',
	help="build")
arg = parser.parse_args()

efp = open('exons1.fa', 'w')
ifp = open('introns1.fa', 'w')

for d in os.listdir(arg.build_dir):
	n = d[4:]
	base = f'{arg.build_dir}/{d}/{n}'

	genome = Reader(fasta=f'{base}.fa', gff=f'{base}.gff')
	chrom = next(genome) # there is one

	genes = chrom.ftable.build_genes()
	if len(genes) != 1: continue
	gene = chrom.ftable.build_genes()[0] # there is one
	tx = gene.transcripts()
	if len(tx) == 0: continue

	tx = tx[0] # use first transcript
	if tx.strand == '-': continue # half the data is enough

	# expression data
	exp = 0
	for f in chrom.ftable.features:
		if f.source == 'RNASeq_splice':
			if f.score > exp: exp = f.score
	exp = int(exp)

	# exons
	for cds in tx.cdss:
		efp.write(f'>{tx.id} {exp}\n{cds.seq_str()}\n')

	# introns
	for intron in tx.introns:
		ifp.write(f'{tx.id} {exp}\n{intron.seq_str()}\n')

