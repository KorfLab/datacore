import sys

count = 0
with open(sys.argv[1]) as fp:
	while True:
		line = fp.readline()
		if line == '': break
		f = line.split()
		if f[1] != 'RNASeq_splice': continue
		count += float(f[5])
print(count)
