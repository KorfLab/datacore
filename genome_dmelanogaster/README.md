Notes
=====

Build process for D.melanogaster genome. Templated off C. elegans build.

## R6.42 ##

Using release R6.42 from flybase. Create a build directory and download the files there. dmel-all-chromsome-r6.42.fasta.gz dmel-all-r6.42.gff.gz

	mkdir genome_dmelanogaster/build


## FASTA ##

The genome has a lot of scaffolds that aren't in chromosomes. The only chromosomes we're interested in are the complete arms: 2L, 2R, 3L, 3R, 4, X, Y

Creating a stripped-down FASTA

	gunzip -c build/dmel-all-chromosome-r6.42.fasta.gz | head -1719359 > build/r6.42.fa

## GFF ##

Let's have a look at what's inside the GFF...

	perl flycheck.pl build/dmel-all-r6.42.gff.gz > datatypes.txt

The gene information is in the following lines

+ source: FlyBase
+ type: CDS, exon, five_prime_UTR, gene, intron, mRNA, three_prime_UTR

RNA-seq splicing is in exon_junction. Not sure where bulk RNA-seq is. The browser shows an Olver lab SRA aggregate, but it's not in the GFF.

+ source: FlyBase
+ type: exon_junction

Creating a stripped-down GFF. This converts exon_junction to RNASeq_splice among other things.

	perl flymunge.pl build/dmel-all-r6.42.gff.gz > build/r6.42.gff3

## 1% builds ##

The mini build for testing purposes	

	haman --fasta build/r6.42.fa --gff build/r6.42.gff3 --out 1pct --segment percent --pct 1

The mini gene build

	haman --fasta 1pct.fa --gff 1pct.gff3 --out build/mini_gene --segment gene

The mini region build

	haman --fasta 1pct.fa --gff 1pct.gff3 --out build/mini_region --segment region

## Full builds ##

Gene build takes about 10.5 min and 2G RAM.

	time haman --fasta build/r6.42.fa --gff build/r6.42.gff3 --out build/genes --segment gene

Region build takes about 6.5 min and 2G RAM.

	time haman --fasta build/r6.42.fa --gff build/r6.42.gff3 --out build/regions --segment region
