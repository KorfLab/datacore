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

## Post-processing APC ##

Get some info aobut the genes of the APC set.

	isostats.py isoformer apc.fa | sort -nk5  > 1102.txt

+ 45 w/ less than 1000 isoforms
+ 145 w/ less than 10K isoforms
+ 351 w/ less than 100K isoforms
+ 722 w/ less than 1M isoforms
+ 1060 w/ less than 10M isoforms

## To Do ##

+ Make the `apc_build.py` program work for other genomes.
	+ Use argparse
	+ Name the output files with source genome
+ Build the other apc datasets
