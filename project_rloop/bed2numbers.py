import argparse
import gzip

parser = argparse.ArgumentParser(
	description='Stream data from wig to coverage')
parser.add_argument('wig', type=str, metavar='<wig>',
	help='wig file, may be compressed')
arg = parser.parse_args()

if arg.wig.endswith('.gz'): fp = gzip.open(arg.wig, 'rt')
else:                       fp = open(arg.wig)

beg = 1
next = 1
while True:
	line = fp.readline()
	if line == '': break
	if line.startswith('#'): continue
	c, b, e, v = line.split()
	b = int(b)
	e = int(e)
	
	# fill in missing values with zero
	if b != beg: 
		for i in range(beg, b): print(i, '0')
		beg = b
	
	# fill in reported values
	for i in range(b, e):
		print(i, v)
	beg = e

