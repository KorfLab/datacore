import sys
import gzip
import fnmatch

count = 0
with gzip.open(sys.argv[1], 'rt') as fp:
	while True:
		line = fp.readline()
		if line == '': break
		f = line.split()
		if f[1] != 'RNASeq_splice': continue
		count += float(f[5])
print('RNASeq_splice:', count)

# count all RNASeq
count = 0
with gzip.open(sys.argv[1], 'rt') as fp:
	while True:
		line = fp.readline()
		if line == '': break
		f = line.split()
		if fnmatch.fnmatch(f[1], 'RNASeq_*') != True: continue
		if isinstance(float(f[5]), float) != True: continue
		count += float(f[5])
print('All RNASeq_:', count)


