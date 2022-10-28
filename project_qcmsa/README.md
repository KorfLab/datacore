Quality Control with Multiple Sequence Alignments
=================================================

MSAs can be useful for genome annotation quality control because they give an 
evolutionary perspective on sequences. For example, in the following MSA, most 
of these highly conserved proteins have the exact same starting Methionine. 
However, one of them has a much longer N-terminal extension (34506.g6644). What 
is more likely, that this one protein is an extreme outlier in this highly 
conserved family or that the N-terminal extension is the product of robotically 
following the "longest ORF" heuristic?

```
----------------------------MASRTTAGGIGFAVMS 6326.BUX.s01141.83
----------------------------MANRTTAGGIGFAVRQ 6239.F28H1.2
----------------------------MANRTTAGGIGFAVRQ 6238.CBG12084
MVIHCPMFVIQNFILFYILILKFIISYSMASRTTAGGIGFSVQA 34506.g6644
----------------------------MANRTTAGGIGFAVRQ 31234.CRE24012
----------------------------MSTRTTAGGIGFAVMQ 7209.EJD74170.1
----------------------------MASRTTPGGLGFAVLQ 6334.EFV52354
----------------------------MANRTTAGGIGFAVRQ 135651.CBN19153
----------------------------MANRTTAGGIGFAVRQ 135651.CBN14566
----------------------------MANRTTAGGIGFAVRQ 281687.CJA04130
```

## DATA ##

The data here is from eggnog 5.0 (2019) within the taxon 6231 (nematoda). There 
are others sources of orthologous MSAs, but for the time being, this represents 
a useful set of proteins. The download URL at the time is this:

http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/6231

## ntermi.py ##

Assuming you unpacked ther raw alignments into a build directory, try this

	python3 ntermi.py build/6231 --key 6239

6239 is the numeric identifier for C. elegans. This guarantees that all of the 
MSAs include C. elegans proteins. This results in a file with 821 MSAs whose 
N-terminal alignments are suspect for some reason or another. There are several 
likely categories of errors:

+ Following the longest-ORF rule
+ Gene fusions
+ Genomic sequence errors
+ Unitary pseudogenes
+ Alignment difficulties

## Interpretations ##

The `interpretations.txt` file contains an analysis of the 821 MSAs for further 
consideration.
