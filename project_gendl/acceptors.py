import argparse
import gzip

parser = argparse.ArgumentParser(
	description='acceptor extractor')
parser.add_argument('eie', type=str, metavar='<eie>',
	help='path to exon-intron-exon file')
parser.add_argument('--exon', type=int, metavar='<int>', default=0,
	required=False, help='number of bases of exon [%(default)i]')
parser.add_argument('--intron', type=int, metavar='<int>', default=5,
	required=False, help='number of bases of intron [%(default)i]')
arg = parser.parse_args()

with gzip.open(arg.eie, 'rt') as fp:
	for line in fp.readlines():
		(exon1, intron, exon2, expression, gene) = line.split()
		print(intron[-arg.intron:], end='')
		if arg.exon: print(exon2[0:arg.exon], end='')
		print()
