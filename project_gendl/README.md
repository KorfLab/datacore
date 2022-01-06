Generating Data for gendl
=========================

Considering exons

+ Size of sequences (e.g. 51 bp)
+ Sampling method
	+ Every window of sequence
	+ Some number of windows per sequence
+ What's the negative?
	+ Introns?
	+ Shuffled?
	+ The other strand?
+ Alternative isoforms
	+ Include
	+ Exclude
	+ Weighting them by occurance?
+ Misc
	+ Genes that are poorly expressed, might not even be real
	+ Genes that are really long or really short
	+ Exons that are shorter than 51 (or whatever)
	+ Genes that are highly conserved vs. poorly conserved
	+ Exon (includes UTRs) vs. CDS (only the protein-coding part)
