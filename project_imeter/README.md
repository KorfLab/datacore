IMEter
======

Intron Mediated Enhancement was a project between the Rose and Korf labs for several years. This project is a reboot of that using the latest data and ideas.

## Data ##

Start by building the A. thalaia genome from `datacore/genome_athaliana`. The gene build is what's needed.

## Master File ##

The master file contains information for most of the introns in the genome. It takes about 30 sec and minimal memory to build.

	python3 intron_build.py > at_ime_master.txt

The file is tab-separated and has the following columns

+ Transcript ID
+ Intron begin relative to start of gene
+ Intron end relative to start of gene
+ Strand of the gene in the genome
+ 11 expression values (RNA-seq splice junctions) for various tissues
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

The file looks like this (4 lines shown of 142,779):

	AT3G02220.1     1057    1151    -       380     349     601     2717    3010    3       489     321     1010    49      499     GTAAGCTTCTCTAGTTACTTTGAAGAGTTTTTGAGATTTGTAAATGTGTATGTTTGTGTGATTTGGTCCTGAAGTTGCGTATTTGCTTGACATAG
	AT3G02220.1     914     1008    -       362     302     677     2889    3291    0       462     373     1170    9       655     GTTTGTCTTTTAATTATTCCGCTTTTGGCTTCTAATGTTCAATTTCATGCTTGTTTTTGGGAGGTTGTTGCTGATTTCTTATTGATGTGATGCAG
	AT3G02220.1     753     870     -       331     309     542     2861    2968    2       504     340     839     48      503     GTACTTGTACCTTGAAGACAGTCTTTCTTCTACTTATGCTAGATGCTGGTTTCCTTAAGAGTGGGTTTAGTAGACAAGATATTAAACTAATCTTGAGGTAATTATTCGTTTCTCGCAG
	AT3G02220.1     565     688     -       283     249     571     2568    2308    5       471     374     697     25      265     GTTAGTGTTTTCTTTCTTTGCTTTTGTTCTCGTACTTTCTTGGCTAATTAGAGTGTATAGATCAGTATCTTGTTTTATAAGTTGATGTGTTATGGTATTGAAATGGGTATGAAACTGATAACAG


## Notes ##

Some genes have alternative transcripts.
