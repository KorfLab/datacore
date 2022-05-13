Notes
=====

Build process for A.thaliana genome.

## TAIR10 ##

Using release TAIR10 arabidopsis.org. Create a build directory and download the
files there. TAIR10_chr_all.fas TAIR10_GFF3_gene.gff

```
mkdir genome_athaliana/build
```

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

I have therefore made a copy of the fasta file `TAIR10_chr_all.fas` as
`build/genome.fa` and changed the chromosome names to the GFF versions.

## GFF ##

Let's have a look at what's inside the GFF...

```
perl gffcheck.pl build/TAIR10_GFF3_genes.gff
```

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

What about RNA-seq information? The genome's JBrowse shows that there is RNA-seq
"Splice Junctions" as well as "Mapping Coverage". I emailed TAIR curators to
find out how to get that and they said to use the 'Save track data' and choose
the whole reference. After saving 55 files (11 tissues * 5 chromosomes) in an
`RNA-seq` directory, I had all of the Splice Junctions in gff files. I decided
not to bother with the Mapping Coverage.

The `gffhack.pl` program merges all of the splice data into a single gff.

```
perl gffhack.pl > splice.gff3
cat build/TAIR10_GFF3_genes.gff splice.gff3 > build/genes.gff3
gzip splice.gff3	
```

## 1% builds ##

The mini build for testing purposes

```
haman build/genome.fa build/genes.gff3 pct 1pct --pct 1
```

The mini gene build

```
haman 1pct.fa 1pct.gff3 gene build/mini_gene
```

## Full builds ##

Gene build takes about an hour and 1.6G RAM. After this is done, clear out the
build directory except for the `genes` directory and then make a tar-ball.

```
haman build/genome.fa build/genes.gff3 pcg build/genes
#rm build/...
tar -zcf genes.tar.gz build
```