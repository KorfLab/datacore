Splicing
========

APC Build
---------

+ Short genes < 1200 bp for the chromosomal region (<1000 bp transcript)
+ Have a single annotated isoform (no argument about which one is canonical)
+ Contain at least 1 intron in transcript
+ Moderately expressed region: RNASeq_splice > 100,000
+ No short introns (<35)
+ No short exons (<25)
+ No non-coding RNA genes
+ Not too many possible isoforms (1e6)

These criteria above are the defaults in `apc_build`

Requires doing a C.elegans gene build

	./apc_build ../genome_celegans/build/genes
	
This creates 2 files: `apc.genes.txt` and `apc.log.json`
	
	mkdir apc
	perl gather.pl apc.genes.txt
	tar -zcf apc.tar.gz apc
	rm -rf apc

Stuff
-----

The `grapher.py` is a draft of an idea whose output is in `example.svg`.
