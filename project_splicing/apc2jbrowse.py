import argparse
from grimoire.genome import Reader
from grimoire.feature import Feature

parser = argparse.ArgumentParser(description='create GFF for use with jbrowse')
parser.add_argument('fasta')
parser.add_argument('gff')
parser.add_argument('--emm')
parser.add_argument('--elen')
parser.add_argument('--imm')
parser.add_argument('--ilen')
parser.add_argument('--don')
parser.add_argument('--acc')

arg = parser.parse_args()

genome = Reader(gff=arg.gff, fasta=arg.fasta)
dna = next(genome)

# get original genomic location from fasta defline
loc, STR, gene = dna.desc.split()
chrom, coords = loc.split(':')
BEG, END = coords.split('-')
BEG = int(BEG)
END = int(END)

# create gff components
exos = []
ints = []
accs = []
dons = []
for f in dna.ftable.features:
	coor = (f.beg, f.end)
	if f.type == 'intron':
		if coor not in ints: ints.append(coor)
		if f.beg not in dons: dons.append(f.beg)
		if f.end not in accs: accs.append(f.end)
	elif f.type == 'exon':
		if coor not in exos: exos.append(coor)

gffs = []
for beg, end in exos:
	gffs.append(Feature(dna, beg, end, STR, 'exon', source='model',
		score=0))
for beg, end in ints:
	gffs.append(Feature(dna, beg, end, STR, 'intron', source='model',
		score=0))
for beg in dons:
	gffs.append(Feature(dna, beg, beg+1, STR, 'donor', source='model',
		score=0))
for beg in dons:
	gffs.append(Feature(dna, beg, beg+1, STR, 'acceptor', source='model',
		score=0))
for f in gffs:
	dna.ftable.add_feature(f)


# convert all features to negative strand as needed
if STR == '-': dna.revcomp()

# output all features upscaled to genome coordinates
for f in dna.ftable.features:
	col9 = ''
	if f.id: col9 = f'ID={f.id}'
	if f.pid:
		pids = ','.join(f.pid)
		if col9: col9 += f';Parent={pids}'
		else:    col9 = f'Parent={pids}'

	print('\t'.join((chrom, f.source, f.type,
		str(f.beg + BEG), str(f.end + BEG), # this is probably off by 1
		str(f.score), f.strand, '.', col9)))

