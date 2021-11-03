Notes
=====

Build process for C. elegans genome

## WS282 ##

WS282 is the release used by AlphaFold, so it makes sense to use this as our
standard for a while.

## 1 percent build ##

Make a stripped down version of the gff that contains the WormBase genes along
with RNA-seq data for 1% of the genome. Download ws282 files to the
`genome_celegans/build` directory first.

	cd genome_celegans
	gunzip -c build/c_elegans.PRJNA13758.WS282.annotations.gff3.gz | grep -E "WormBase|RNASeq" > build/ws282.gff3

	haman --fasta build/c_elegans.PRJNA13758.WS282.genomic.fa.gz --gff build/ws282.gff3 --out 1pct_elegans --segment percent --pct 1

## region build ##

The full region build is large because we want all of the GFF, not just the genes. First, make a mini region in case we need to do some testing.

	haman --fasta 1pct_elegans.fa --gff 1pct_elegans.gff3 --out build/mini --segment region

Then make the full region biuld. This takes about 4G RAM and some time...

	time haman --fasta build/c_elegans.PRJNA13758.WS282.genomic.fa.gz --gff build/c_elegans.PRJNA13758.WS282.annotations.gff3.gz --out build/region --segment region
	
