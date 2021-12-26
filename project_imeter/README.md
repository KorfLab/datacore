IMEter
======

Intron Mediated Enhancement was a project between the Rose and Korf labs for several years. This project is a reboot of that using the latest data and ideas.

## Data ##

Start by building the A. thalaia genome from `datacore/genome_athaliana`. The gene build is what's needed.

## Master File ##

The master file contains information for most of the introns in the genome. It takes about XXX to build.

	python3 intron_build.py > ime_master.txt

The file is tab-separated and has the following columns

+ Transcript ID
+ Intron begin relative to start of gene
+ Intron end relative to start of gene
+ Strand of the gene in the genome
+ 11 expression values for various tissues
	+ Aerial
	+ Carpel
	+ Dark Grown Seedling
	+ Light Grown Seedling
	+ Leaf
	+ Pollen
	+ Receptacle
	+ Root Apical Meristem
	+ Root
	+ Shoot Apical Meristem
	+ Stage 12 Flower
+ Sequence of the intron

The file looks like this:

	AT1G01080.1     1374    1459    -       407     130     442     4126    4083    0       541     14      46      38      104     GTTAAGTTCGTTATCCATAAAAAGAATCTTGCTTGAGGAAACTTCTTCTACTGCTCTCTGGCTTTATCACAATCTCTCTTTTGCAG
	AT1G01080.1     976     1064    -       654     191     383     4040    4371    0       410     16      48      47      202     GTAAGAGCCCGGGAAACCAAAAAACAAGTCTATCTTTCTTCTGGTTGAGTGTAAAGTTGAGTGCTTTGGTTTTGTTGCTATATATGAAG

## Notes ##

Some genes have alternative transcripts.


	
	
	
	
	
