import argparse
import random

random.seed(1)

from grimoire.genome import Reader

## CLI
parser = argparse.ArgumentParser(description="exon trainer")
parser.add_argument("fasta", type=str, metavar='<file>',
	help="Enter name of fasta file")
parser.add_argument("gff", type=str, metavar='<file>',
	help="Enter name of gff file")
parser.add_argument("--size", required=False, type=int, metavar='<int>',
	default=51, help="sequence length")
parser.add_argument("--samples", required=False, type=int, metavar='<int>',
	default=0, help="number of samples, 0 = all (default)")
arg = parser.parse_args()


genome = Reader(fasta=arg.fasta, gff=arg.gff)

seqs = {}
for chrom in genome:
	for gene in chrom.ftable.build_genes():
		for tx in gene.transcripts():
			cds = tx.cds_str()
			if len(cds) == 0: continue
			if arg.samples != 0:
				for i in range(arg.samples):
					p = random.randint(0, len(cds) - arg.size + 1)
					print(cds[p:p+arg.size])
			else:
				for i in range(0, len(cds) - arg.size + 1):
					print(cds[i:i+arg.size])



uni = seqs.keys()

k = arg.size
for seq in uni:
	for i in range(0, len(seq) - k + 1):
		print(seq[i:i+k])
