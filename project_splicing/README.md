Splicing
========

## APC Build ##

+ Short genes < 1200 bp for the chromosomal region (<1000 bp transcript)
+ Highly expressed region: RNASeq_splice > 100,000
+ Contain at least 1 intron in transcript
+ Protein-coding and no weird issues

Requires `../datacore/genome_celegans/build` directory

	python3 apc_build.py

Creates output files `apc.fa` and `apc.gff` which were compressed before push.
There are 1102 genes.

## To Do ##

+ Make the `apc_build.py` program work for other genomes.
	+ Use argparse
	+ Name the output files with source genome
+ Build the other apc datasets
