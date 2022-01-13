import argparse
from grimoire.genome import Reader

## CLI
parser = argparse.ArgumentParser(description="exon trainer")
parser.add_argument("fasta", type=str, metavar='<file>',
                    help="Enter name of fasta file")
parser.add_argument("gff", type=str, metavar='<file>',
                    help="Enter name of gff file")
parser.add_argument("--size", required=False, type=int, metavar='<int>', default=51,
                    help="sequence length")
arg = parser.parse_args()


genome = Reader(fasta=arg.fasta, gff=arg.gff)

seqs = {}
for chrom in genome:
	for gene in chrom.ftable.build_genes():
		for tx in gene.transcripts():
			print(tx.cds_str())  # anchored at ATG
#			for exon in tx.cdss:  # coding sequence
#				seqs[exon.seq_str()] = True

uni = seqs.keys()

k = arg.size
for seq in uni:
	for i in range(0, len(seq) - k + 1):
		print(seq[i:i+k])
