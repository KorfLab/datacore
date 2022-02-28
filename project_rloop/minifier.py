import sys
import gzip

limit = 3000000

for file in sys.argv[1:]:
	with gzip.open(file, 'rt') as fp:
		words = file.split('_')
		if words[2] == 'WT':
			out = f'{words[3]}.{words[4]}.{words[5][:3]}.bg'
		else:
			out = f'{words[2]}.{words[3][:3]}.bg'
		ofp = open(out, 'w')
		while True:
			line = fp.readline()
			if line.startswith('#'): continue
			chrom, beg, end, level = line.split()
			beg = int(beg)
			end = int(end)
			if beg > limit: break
			if end > limit: end = limit
			ofp.write(f'{chrom} {beg} {end} {level}\n')
		ofp.write(f'{chrom} {limit} {limit+1} 0.0\n')
		ofp.close()


