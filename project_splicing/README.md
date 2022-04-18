Splicing
========

The build procedure needs a slight re-write with the criteria below. There 
should also be a file that reports how many pass and fail at each point.

## APC Build ##

+ Short genes < 1200 bp for the chromosomal region (<1000 bp transcript)
+ Contain at least 1 intron in transcript
+ No non-canonical features
	+ Splice sites
	+ Intron lengths
	+ Exon lengths
	+ Other issues
+ Highly expressed region: RNASeq_splice > 100,000
+ Have a single annotated isoform (no argument about which one is canonical)
+ Have no non-coding genes embedded inside

+ These criteria are the defaults in `apc_build`

Requires doing a C.elegans gene build

	./apc_build ../genome_celegans/build/genes | sort -nk5 > apc_set.txt
	mkdir apc
	perl gather.pl apc_set.txt
	tar -zcf apc.tar.gz apc
	rm -rf apc

The `grapher.py` is a draft of an idea whose output is in `example.svg`.
