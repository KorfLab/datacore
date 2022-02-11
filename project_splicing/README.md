Splicing
========

## APC Build ##

+ Short genes < 1200 bp for the chromosomal region (<1000 bp transcript)
+ Highly expressed region: RNASeq_splice > 100,000
+ Contain at least 1 intron in transcript
+ Protein-coding and no weird issues
+ Not too many isoforms (1M max)

Requires `../genome_celegans/build` directory

	./apc_build ../genome_celegans/build/genes | sort -nk5 > 772.txt
	perl gather.pl



The `grapher.py` is a draft of an idea whose output is in `example.svg`.
