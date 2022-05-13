Notes
=====

Build process for D.melanogaster genome. Templated off C. elegans build.

## R6.42 ##

Using release R6.42 from flybase. Create a build directory and download the
files there. dmel-all-chromsome-r6.42.fasta.gz dmel-all-r6.42.gff.gz

```
mkdir genome_dmelanogaster/build
```

## FASTA ##

The genome has a lot of scaffolds that aren't in chromosomes. The only chromosomes we're interested in are the complete arms: 2L, 2R, 3L, 3R, 4, X, Y

Creating a stripped-down FASTA

```
gunzip -c build/dmel-all-chromosome-r6.42.fasta.gz | head -1719359 > build/r6.42.fa
```

## GFF ##

Let's have a look at what's inside the GFF...

```
perl flycheck.pl build/dmel-all-r6.42.gff.gz > datatypes.txt
```

The gene information is in the following lines

+ source: FlyBase
+ type: CDS, exon, five_prime_UTR, gene, intron, mRNA, three_prime_UTR

RNA-seq splicing is in exon_junction. Not sure where bulk RNA-seq is. The browser shows an Olver lab SRA aggregate, but it's not in the GFF.

+ source: FlyBase
+ type: exon_junction

Create a stripped-down GFF. This converts exon_junction to RNASeq_splice among
other things. This takes about 2 min to run.

```
perl flymunge.pl build/dmel-all-r6.42.gff.gz > build/r6.42.gff3
```

## 1% builds ##

The mini build for testing purposes

```
haman build/r6.42.fa build/r6.42.gff3 pct 1pct --pct 1
```

The mini gene build

```
haman 1pct.fa 1pct.gff3 pcg build/mini_gene
```

## Full builds ##

Gene build takes about 6 min and 2G RAM. After that's done remove everything in
the build directory except the `genes` directory and then tar-ball it.

```
haman build/r6.42.fa build/r6.42.gff3 pcg build/genes
#rm build/...
tar -zcf genes.tar.gz build
```

