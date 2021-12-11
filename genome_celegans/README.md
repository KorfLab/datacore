Notes
=====

Build process for C. elegans genome

## WS282 ##

WS282 is the release used by AlphaFold, so it makes sense to use this as our
standard for a while. Download the genome and gff3 files and move them to the build directory.

	mkdir genome_celegans/build

## 1 percent build ##

The 1% build is useful when you're developing software and don't want the overhead of working with the whole genome (which is about 99% of the time).

First, make a stripped down version of the gff that contains the WormBase genes along with RNA-seq data. This file will get used a few times.

	cd genome_celegans
	gunzip -c build/c_elegans.PRJNA13758.WS282.annotations.gff3.gz | grep -E "WormBase|RNASeq" > build/ws282.gff3

Now make the 1% build with `haman` (from grimoire).

	haman --fasta build/c_elegans.PRJNA13758.WS282.genomic.fa.gz --gff build/ws282.gff3 --out 1pct_elegans --segment percent --pct 1

## gene build ##

For gene-centric studies, it's useful to have just the sequence around a specific gene. Chromosomes are just too big to work with. The first step is to make a miniature gene build for testing purposes.

	haman --fasta 1pct_elegans.fa --gff 1pct_elegans.gff --out build/mini_gene --segment gene

Now the full build using the stripped down GFF from the 1% build. This takes about 2.5 hours and 3G RAM on a Linux VM running on a Lenovo Idea Pad 3.

	time haman --fasta build/c_elegans.PRJNA13758.WS282.genomic.fa.gz --gff build/ws282.gff3 --out build/genes --segment gene


## region build ##

A region contains several genes in close proximity. The gene build above may end up with some partial genes nearby, but the region build makes sure that all genes are complete. First, make a mini region build for testing and development purposes.

	haman --fasta 1pct_elegans.fa --gff 1pct_elegans.gff --out build/mini_region --segment region

Then make the full region build. This takes about 80 min and 4G RAM.

	time haman --fasta build/c_elegans.PRJNA13758.WS282.genomic.fa.gz --gff build/c_elegans.PRJNA13758.WS282.annotations.gff3.gz --out build/region --segment region

