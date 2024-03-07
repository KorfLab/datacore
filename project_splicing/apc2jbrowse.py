import argparse
from grimoire.genome import Reader

parser = argparse.ArgumentParser(
	description='create GFF for use with jbrowse')
parser.add_argument('fasta', type=str, metavar='<fasta file>',
	help='path to fasta file')
parser.add_argument('gff', type=str, metavar='<gff file>',
	help='path to gff file')
arg = parser.parse_args()

genome = Reader(gff=arg.gff, fasta=arg.fasta)
dna = next(genome)

# get original genomic location from fasta defline
loc, strand, gene = dna.desc.split()
chrom, coords = loc.split(':')
beg, end = coords.split('-')
beg = int(beg)
end = int(end)
#print(chrom, beg, end, strand)

# create splice acceptor features
# create splice donor features
# create exon features
# create intron features

# convert all features to negative strand as needed
if strand == '-': dna.revcomp()

# output all features upscaled to genome coordinates
for f in dna.ftable.features:
	print('\t'.join((chrom, f.source, f.type,
		str(f.beg + beg), str(f.end + beg), # this is probably off by 1
		str(f.score), f.strand, '.')))

