inex
====

inex is a python script that picks out all the introns, canonical introns, and exons from a given gene. 

## Python script ##

To run the python script:

	python3 inex.py --fa ~/datacore/genome_celegans/build/mini_gene/gene10/10.fa --gff ~/datacore/genome_celegans/build/mini_gene/gene10/10.gff --out gene10
	
## Bash script ##

Can also use a bash script to automate inex for all genes in a directory:

Edit inex.sh and change the GENEPATH to the path of the genes
	
	GENEPATH=~/datacore/genome_celegans/build/mini_gene

Run the bash script:
	
	bash inex.sh
	
Every gene dirctory in the GENEPATH now has an inex folder that contains 3 fasta files for the gene's introns, canonical introns, and exons
	


