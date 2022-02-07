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

The file `440.tar.gz` contains a directory `440` with 440 fasta and gff files
that pass all of the current filters.

The `grapher.py` is a draft of an idea whose output is in `example.svg`.
