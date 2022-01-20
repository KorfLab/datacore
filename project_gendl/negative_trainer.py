import argparse
import gzip
import random
import sys

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
#parser.add_argument("--source", required=False, type='str', metavar='<int>',
#	default=0, help="source of negative sequence")
parser.add_argument("--samples", required=False, type=int, metavar='<int>',
	default=0, help="number of samples, 0 = all (default)")
arg = parser.parse_args()




"""
	1	genome base composition randomly generated
	2	CDS base composition random
	3	intron base composition
	4	CDS shuffled as 1-mer
	5	kmers?
"""

genome_at = 0 # Neg 1
genome_gc = 0 # Neg 1
cds_a = 0
cds_c = 0
cds_g = 0
cds_t = 0
int_a = 0
int_c = 0
int_g = 0
int_t = 0

genome = Reader(fasta=arg.fasta, gff=arg.gff)

for chrom in genome:
	genome_at += chrom.seq.count('A')
	genome_at += chrom.seq.count('T')
	genome_gc += chrom.seq.count('C')
	genome_gc += chrom.seq.count('G')

	for gene in chrom.ftable.build_genes():
		for tx in gene.transcripts():
			cds = tx.cds_str()
			cds_a += cds.count('A')
			cds_c += cds.count('C')
			cds_g += cds.count('G')
			cds_t += cds.count('T')
			for intron in tx.introns:
				iseq = intron.seq_str()
				int_a += iseq.count('A')
				int_c += iseq.count('C')
				int_g += iseq.count('G')
				int_t += iseq.count('T')
			"""
			if len(cds) == 0: continue
			if arg.samples != 0:
				for i in range(arg.samples):
					p = random.randint(0, len(cds) - arg.size + 1)
					print(cds[p:p+arg.size])
			else:
				for i in range(0, len(cds) - arg.size + 1):
					print(cds[i:i+arg.size])
			"""

print(cds_a, cds_c, cds_g, cds_t, (cds_a + cds_t) / (cds_a + cds_c + cds_g + cds_t))
print(int_a, int_c, int_g, int_t, (int_a + int_t) / (int_a + int_c + int_g + int_t))
#print(at, gc, at/(at+gc))

