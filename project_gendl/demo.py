from grimoire.genome import Reader
import sys

genome = Reader(fasta=sys.argv[1], gff=sys.argv[2])

seqs = {}
for chrom in genome:
	for gene in chrom.ftable.build_genes():
		for tx in gene.transcripts():
			for exon in tx.cdss:
				seqs[exon.seq_str()] = True

uni = seqs.keys()

k = 51
for seq in uni:
	for i in range(0, len(seq) - k + 1):
		print(seq[i:i+k])
