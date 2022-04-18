Splicing
========

## APC Build ##

+ Short genes < 1200 bp for the chromosomal region (<1000 bp transcript)
+ Highly expressed region: RNASeq_splice > 100,000
+ Contain at least 1 intron in transcript
+ Protein-coding and no weird issues
+ No really short introns or exon
+ Not too many isoforms (1M max)
+ These criteria are the defaults in `apc_build`

Requires doing a C.elegans gene build

	./apc_build ../genome_celegans/build/genes | sort -nk5 > apc_set.txt
	mkdir apc
	perl gather.pl apc_set.txt
	tar -zcf apc.tar.gz apc
	rm -rf apc

The `grapher.py` is a draft of an idea whose output is in `example.svg`.
