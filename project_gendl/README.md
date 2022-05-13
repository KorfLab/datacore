Generating Data for gendl
=========================

To begin, you need a typical `haman` gene build. Assuming that is in a build
directory called genes, do the following:

```
gendl_build build/genes > eie.txt
```

This outputs an exon-intron-exon file. By default, each line contains
space-separated values with the following information:

+ 50 nt of exon preceding an intron
+ The entire sequence of the intron (40-150 bp)
+ 50 nt of exon after the intron
+ RNA splice count
+ Source gene

If either exon is below 50, the exon-intron-exon is not reported. If the intron
is short (<40) or long-ish (>150) the exon-intron-exon is not reported.

Duplicate exon-intron-exons from alternative isoforms or closely related genes
are reported only once. In such a case, only one source gene name is given.

## Sampling ##

In order to create test/training sets, you have to sample the `eie.txt` file.
The `gendl_selector` program provides that functionality.



