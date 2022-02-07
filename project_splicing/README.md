Splicing
========

## APC Build ##

+ Short genes < 1200 bp for the chromosomal region (<1000 bp transcript)
+ Highly expressed region: RNASeq_splice > 100,000
+ Contain at least 1 intron in transcript
+ Protein-coding and no weird issues
+ Not too many isoforms (1M max)

Requires `../datacore/genome_celegans/build` directory

	/apc_build ../genome_celegans/build/genes > celegans.apc.txt

## To Do ##

`apc_build` gives the names of the sequences to use, but does not create fasta
or gff files to process. This set should be sorted and examine before making
the mini test set.

There needs to be some kind of visualizer

+ exon-intron structure of the gene(s) in the region
+ expression levels of each splice site
+ probabilities of the top isoforms?
