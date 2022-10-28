Quality Control with Multiple Sequence Alignments
=================================================

MSAs can be useful for genome annotation quality control because they give an 
evolutionary perspective on sequences. For example, in the following MSA, most 
of these highly conserved proteins have the exact same starting Methionine. 
However, one of them has a much longer N-terminal extension (6239.W08D2.6). 
What is more likely, that this one protein is an extreme outlier in this highly 
conserved family or that the N-terminal extension is the product of robotically 
following the "longest ORF" heuristic?

```
----------MQLSSATFVASSLSAI 31234.CRE03571
MGIFSEFLYRMQVSSVTFVASSLSAI 6239.W08D2.6
----------MQVSSATFVASSLSAI 6238.CBG03475
----------MQVSSATFVASSLSGI 281687.CJA07071
----------MQVSSATFVASSLSAI 135651.CBN16755
----------MQVSSATFVASSLSAI 135651.CBN14324
----------MQLSSATFVASSLSAI 31234.CRE29867
```

## DATA ##

The data here is from eggnog 5.0 (2019) within the taxon 6231 (nematoda). There 
are others sources of orthologous MSAs, but for the time being, this represents 
a useful set of proteins. The download URL at the time is this:

http://eggnog5.embl.de/download/eggnog_5.0/per_tax_level/6231

## ntermi.py ##

Assuming you unpacked ther raw alignments into a build directory, try this

python3 ntermi.py build/6231 --key 6239 > 6239all
python3 ntermi.py build/6231 --key 6239 --only > 6239only

6239 is the numeric identifier for C. elegans. `--key 6239` guarantees that all 
of the MSAs include C. elegans proteins. Including the `--only` flag limits the 
report to those MSAs where the key organism is in error. The program flags 472 
alignments for further investigation, and 45 where 6239 appears as an outlier 
compared to the rest. The `ntermi.py` script currently tries to identify unique 
cases of longest-ORF or gene fusion events. It skips over cases where there are 
multiple suspect sequences and also over problems that it doesn't understand. 
Ideally, we should be looking for these categories and more.

+ Longest-ORF rule
+ Gene fusions
+ Genomic sequence errors
+ Unitary pseudogenes
+ Alignment difficulties
+ Excessive UTR lengths may indicate problems

## Interpretations ##

The `interpretations.txt` file contains a manual analysis of some of the MSAs. 
This may be removed at some point.
