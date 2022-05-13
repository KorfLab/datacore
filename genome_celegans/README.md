Notes
=====

Build process for C. elegans genome

## WS282 ##

WS282 is the release used by AlphaFold, so it makes sense to use this as our
standard for a while. Download the genome and gff3 files and move them to the
build directory.

```
mkdir genome_celegans/build
```

## 1 percent build ##

The 1% build is useful when you're developing software and don't want the
overhead of working with the whole genome (which is about 99% of the time).

First, make a stripped down version of the gff that contains the WormBase genes
along with RNA-seq data. This file will get used a few times. This takes about 3
minutes.

```
cd genome_celegans
gunzip -c build/c_elegans.PRJNA13758.WS282.annotations.gff3.gz | grep -E "WormBase|RNASeq" > build/ws282.gff3
```

Now make the 1% build with `haman` (from grimoire).

```
haman build/c_elegans.PRJNA13758.WS282.genomic.fa.gz build/ws282.gff3 pct 1pct_elegans --pct 1
```

## Protein-coding gene build ##

For typical gene-centric studies, it's useful to have just the sequence around
a specific protein-coding gene. Chromosomes are too big to work with. The first
step is to make a miniature gene build for testing purposes. This uses the 1
percent files just created above.

```
haman 1pct_elegans.fa 1pct_elegans.gff3 pcg build/mini_gene
```

Now the full build (still using the stripped down GFF). This takes about an hour
and 3G RAM. Afterwards remove everything but the `genes` directory and make a
tar-ball.

```
haman build/c_elegans.PRJNA13758.WS282.genomic.fa.gz build/ws282.gff3 pcg build/genes
#rm build/...
tar -zcf genes.tar.gz build
```
