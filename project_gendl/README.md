Generating Data for gendl
=========================

Exon-intron-exon
----------------

The main data source is an exon-intron-exon file with the following
space-delimited line structure:

+ 50 nt of exon preceding an intron
+ The entire sequence of the intron (40-150 bp)
+ 50 nt of exon after the intron
+ RNA splice count
+ Source gene

If either exon is below 50, the exon-intron-exon is not reported. If the intron
is short (<40) or long-ish (>150) the exon-intron-exon is not reported.

Duplicate exon-intron-exons from alternative isoforms or closely related genes
are reported only once. In such a case, only one source gene name is given.


Build
-----

Building exon-intron-exon files for 3 genomes.

```
./gendl_build ../genome_athaliana/build/genes > eie.at.txt
./gendl_build ../genome_celegans/build/genes > eie.ce.txt
./gendl_build ../genome_dmelanogaster/build/genes > eie.dm.txt
gzip *.txt
```

The number of exon-intron-exon lines:

+ 62804 A. thaliana
+ 53515 C. elegans
+ 19886 D. melanogaster


## Demo ##

In order to create test/training sets, you have to sample the various
exon-intron-exon files The `donors.py` program is an example of how to write
those scripts.

## setbuilder ##

This currently re-creates the 42 bp set.

```
mkdir data
python3 setbuilder.py
gzip data/*
```

Still need to make the negatives and add them to data...
