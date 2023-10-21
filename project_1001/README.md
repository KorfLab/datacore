1001 Genomes
============

## Data ##

Use `wget` to retrieve all of the pseudogenomes. This is about 30G of
compressed files.

```
wget -r --no-parent -A 'pseudo*.fasta.gz'
https://1001genomes.org/data/GMI-MPI/releases/v3.1/pseudogenomes/fasta
```

## seqstream ##

This was a cool idea, but ultimately does not work. It remains here as a
reminder to think through the whole problem before coding. The idea was to do a
breadth-first pass through the 1001 genomes, getting the frequency of every
base at every position. The problem is that there are indels, so the genomes
aren't the same lengths. You must do multiple alignment in regions before
getting the probabilities at each position.