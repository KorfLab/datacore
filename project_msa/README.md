Multiple Sequence Alignments
============================

MSAs are useful for a lot of things. Here's the start of _something_.

## DATA ##

eggnog 5.0 (2019) taxon 6231 (nematoda)

http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/6231

These files may be removed later.

## Demo ##

Assuming you unpacked ther raw alignments into a build directory, try this

	python3 ntermi.py build/6231 --key 6239

6239 is the numeric identifier for C. elegans. This guarantees that all of the
MSAs include C. elegans proteins.

This results in a file with 821 MSAs whose N-terminal alignments are suspect.
There are cases where 6239 is the outlier. For example, ZK1073.2 has a longer
N-terminus than the others in the family. It's probably the results of the
longest-ORF rule.
