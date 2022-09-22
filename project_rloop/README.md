README for RLOOP
================

## Original Data ##

Data files were acquired from Stella Hartono and Fred Chedin. The following are
a subset of what they sent. The DRIPc files should have rloops as peaks and the
RNaseH are the controls. These files are kept in a `build` directory.

```
HeLa_DRIPc_WT_LS61A_rep1_neg.bw.wig.gz
HeLa_DRIPc_WT_LS61A_rep1_pos.bw.wig.gz
HeLa_DRIPc_WT_LS61C_rep2_neg.bw.wig.gz
HeLa_DRIPc_WT_LS61C_rep2_pos.bw.wig.gz
HeLa_DRIPc_WT_LS61H_rep3_neg.bw.wig.gz
HeLa_DRIPc_WT_LS61H_rep3_pos.bw.wig.gz
HeLa_qDRIP_RNaseH_neg.bw.wig.gz
HeLa_qDRIP_RNaseH_pos.bw.wig.gz
```

## Test Files ##

The first step is to make smaller versions of each file for testing and also for
saving inside this repo (the original files are large).

	python3 minifier.py build/H*.gz

This creates the following files, which contain up to the first 3 megabases of
chromosome 1 (approximately 0.001 of the genome). The `.bg` file extension
shows that these are bedGraph file types (not the wig shown in the previous
file name).

```
LS61A.rep1.neg.bg
LS61A.rep1.pos.bg
LS61C.rep2.neg.bg
LS61C.rep2.pos.bg
LS61H.rep3.neg.bg
LS61H.rep3.pos.bg
RNaseH.neg.bg
RNaseH.pos.bg
```

These are in their compressed forms in the repo.

## Controls and the Blacklist ##

If you look in the RNAseH controls, you will see some loud signal in one part.
This corresponds to a blacklisted region of the genome, which you can see below.
The other regions listed aren't problematic in the controls, however they do
appear as high coverage in the DRIPc.

```
chr1    564449  570371  High_Mappability_island 1000    .
chr1    724136  727043  Satellite_repeat        1000    .
chr1    825006  825115  BSR/Beta        1000    .
```

The blacklist file is downloadable as `ENCFF000KJP.bigBed`, which is
inconveniently stored in bigBed format. I have converted this to bed and it's in
the repo as `blacklist.bed`.

It's not clear to me that we should use the blacklist file. The DRIPc
experiments may have their own specific confounding sequences. It may be best to
use the controls as negative counts. That is, subtract read counts in DRIPc
where there are counts in RNaseH. How many counts does one reduce though?

As controls go, the RNaseH is not perfect. Peaks that appear in DRIPc still
appear as peaks in RNaseH because digestion may be incomplete.

## bed2numbers.py ##

It is anticipated that we will be using the coverage values for finding rloops.
The `bed2numbers.py` takes in bed files and converts them to a stream of
numbers. The following is NOT RECOMMENDED.

	python3 python3 bed2numbers.py LS61A.rep1.neg.wig > whatever

This inflates the file size by over 100x. There are vast empty regions in the
bed file. Instead, segment the bed file into regions with and without data.
There is no point filling in the first 10k values with zeros, for example.

## Experiments with distancer ##

How different are positive and negative rloop regions from each other? The rloop
signal is supposed to be strand-specific. But is it? K-mers should be different
when compared to each other if you parse just the top strand. However, if you
count both strands, the k-mers should be similar. Also, the k-mers should be
similar from different replicates and cell types if the rloops are relatively
stable.

+ Find peaks using a simple windowing method
	+ window size: 100
	+ depth of reads: 10, 20, 30
+ Extract sequences under peaks
+ Create k-mer tables of subsequences
+ Compare k-mer tables of different cell replicates and cell types

You can run this on the test data as follows:

```
python3 distancer.py chr1.fa.gz L*gz --noisy
python3 distancer.py chr1.fa.gz L*gz --noisy --anti
```

To perform the experiment on the BIGWIG files provided by Stella/Fred, it takes
about 20 minutes to run.

```
python3 distancer.py hg19.fa.gz BIGWIG/*LS6* --blacklist blacklist.bed --noisy --depth 30 --kmer 5 > w100d30k5p

python3 distancer.py hg19.fa.gz BIGWIG/*LS6* --blacklist blacklist.bed --noisy --depth 30 --kmer 5 --anti > w100d30k5a
```

The `tabler.pl` script aggregates a pair of outputs to create a table for
pasting into a Google Sheet.

```
perl tabler.pl w100d30k5* | pbcopy
```

## Some small test data ##

Preparing data for various experiments

```
python3 extract_rloops.py --blacklist blacklist.bed chr1.fa.gz LS61A.rep1.neg.bg.gz > 300.fa
```

This produces a file of 300 R-loop sequences. They are converted so that they
are all on the same strand.

