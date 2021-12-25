Notes
=====

Build process for A.thaliana genome.

## TAIR10 ##

Using release TAIR10 arabidopsis.org. Create a build directory and download the files there. TAIR10_chr_all.fas TAIR10_GFF3_gene.gff

	mkdir genome_athaliana/build

## FASTA ##

The genome has 5 numeric chromosomes plus mitochondria and chloroplast.

+ 1
+ 2
+ 3
+ 4
+ 5
+ mitochondria
+ chloroplast

These are different compared with the GFF...

+ Chr1
+ Chr2
+ Chr3
+ Chr4
+ Chr5
+ ChrC
+ ChrM

I have therefore made a copy of the fasta file `build/genome.fa` and changed the chromosome names to the GFF versions.

## GFF ##

Let's have a look at what's inside the GFF...

	perl gffcheck.pl build/TAIR10_GFF3_genes.gff

The following appear useful for gene purposes

+ CDS
+ exon
+ five_prime_UTR
+ gene
+ mRNA
+ three_prime_UTR

There are also the following which I'll leave in as they won't be intrusive.

- chromosome
- mRNA_TE_gene
- miRNA
- ncRNA
- protein
- pseudogene
- pseudogenic_exon
- pseudogenic_transcript
- rRNA
- snRNA
- snoRNA
- tRNA
- transposable_element_gene

What about RNA-seq information? The genome's JBrowse shows that there is RNA-seq "Splice Junctions" as well as "Mapping Coverage". I emailed TAIR curators to find out how to get that and they said to use the 'Save track data' and choose the whole reference. After saving 55 files (11 tissues * 5 chromosomes) in an `RNA-seq` directory, I had all of the Splice Junctions in gff files. I decided not to bother with the Mapping Coverage.

The `gffhack.pl` program merges all of the splice data into a single gff.

	perl gffhack.pl > splice.gff3

Now for the combined gff with gene and splice info.

	cat build/TAIR10_GFF3_genes.gff splice.gff3 > build/genes.gff3

The splice.gff3 file was compressed and saved in the repo because it isn't easily downloaded.

	gzip splice.gff3

## 1% builds ##

The mini build for testing purposes	

	haman --fasta build/genome.fa --gff build/genes.gff3 --out 1pct --segment percent --pct 1

The mini gene build

	haman --fasta 1pct.fa --gff 1pct.gff3 --out build/mini_gene --segment gene

The mini region build

	haman --fasta 1pct.fa --gff 1pct.gff3 --out build/mini_region --segment region

## Full builds ##

Gene build takes about 30 min and 0.8G RAM.

	time haman --fasta build/genome.fa --gff build/genes.gff3 --out build/genes --segment gene

Region build takes a little less time.

	time haman --fasta build/genome.fa --gff build/genes.gff3 --out build/regions --segment region

