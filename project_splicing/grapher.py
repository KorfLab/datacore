
import argparse
import svgwrite
from svgwrite import cm, mm

from grimoire.genome import Reader

def draw_gene(img, scale, off, gene):
	x = gene.beg * scale
	w = (gene.end - gene.beg + 1) * scale
	img.add(img.rect(insert=(x*cm, off*cm), size=(w*cm, 5*mm),
		fill='blue', stroke='blue', stroke_width=1))
	return 1

def draw_tx(img, scale, off, tx):
	for exon in tx.exons:
		draw_exon(img, scale, off, exon)
	for intron in tx.introns:
		draw_intron(img, scale, off, intron)
	return 1

def draw_exon(img, scale, off, exon):
	x = exon.beg * scale
	w = (exon.end - exon.beg + 1) * scale
	img.add(img.rect(insert=(x*cm, off*cm), size=(w*cm, 5*mm),
		fill='white', stroke='blue', stroke_width=1))
	return 0

def draw_intron(img, scale, off, f):
	x1 = f.beg * scale
	w = (f.end - f.beg + 1) * scale
	x2 = x1 + w
	m = x1 + w / 2
	img.add(img.line(start=(x1*cm, (off+0.25)*cm), end=(m*cm, off*cm),
		stroke='blue', stroke_width=1))
	img.add(img.line(start=(m*cm, (off)*cm), end=(x2*cm, (off+.25)*cm),
		stroke='blue', stroke_width=1))
	return 0

def draw_rnaseq(img, scale, off, f):
	x = f.beg * scale
	w = (f.end - f.beg + 1) * scale
	img.add(img.rect(insert=(x*cm, off*cm), size=(w*cm, 5*mm),
		fill='white', stroke='red', stroke_width=1))
	return 0.5

#######
# CLI #
#######

parser = argparse.ArgumentParser(
	description='isoform graphing thing')
parser.add_argument('fasta', type=str, metavar='<fasta>',
	help='path to fasta file')
parser.add_argument('gff', type=str, metavar='<gff>',
	help='path to gff file')
parser.add_argument('--width', type=int, metavar='<int>', default=20,
	required=False, help='width of image [%(default)i]')
arg = parser.parse_args()


#########
# Image #
#########

chrom = next(Reader(fasta=arg.fasta, gff=arg.gff))
scale = arg.width / len(chrom.seq)
img = svgwrite.Drawing(filename='example.svg')


off = 0
chrom = next(Reader(fasta=arg.fasta, gff=arg.gff))
for gene in chrom.ftable.build_genes():
	off += draw_gene(img, scale, off, gene)
	for tx in gene.transcripts():
		off += draw_tx(img, scale, off, tx)
for f in chrom.ftable.features:
	if f.source == 'RNASeq_splice':
		off += draw_rnaseq(img, scale, off, f)

img.save()

