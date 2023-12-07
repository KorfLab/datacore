Splicing
========

APC Build
---------

+ Short genes < 1200 bp for the chromosomal region (<1000 bp transcript)
+ Have a single annotated isoform (no argument about which one is canonical)
+ Contain at least 1 intron in transcript
+ Have no more than 3 introns
+ Moderately expressed region: RNASeq_splice > 100,000
+ No short introns (<35)
+ No short exons (<25)
+ No non-coding RNA genes
+ Not too many possible isoforms (1e6)

These criteria above are the defaults in `apc_build`


Stuff you need

+ grimoire for `haman`
+ genomikon for `isocounter`
+ executables and libraries in proper paths...

Requires doing a C.elegans gene build with --issuesok

	mkdir build
	cd build
	ln -s $DATA/c_elegans.PRJNA13758.WS282.genomic.fa.gz genome.gz
	ln -s $DATA/c_elegans.PRJNA13758.WS282.annotations.gff3.gz gff3.gz 
	gunzip -c gff3.gz | grep -E "WormBase|RNASeq" > ws282.gff3
	cd ..
	haman build/genome.gz build/ws282.gff3 pcg genes --issuesok
	./apc_build build/genes

2 new files: `apc.genes.txt` and `apc.log.json`

	mkdir apc
	perl gather.pl apc.genes.txt
	tar -zcf apc.tar.gz apc
	mv apc build
