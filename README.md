Data Core
=========

Standardized data generation scripts and data sets supporting research efforts
in the Korf Lab.

## Organization ##

+ `genome_xyz` - data build for a specific genome
+ `project_xyz` - data build for specific project

Some raw data can be very large. For these reasons, we don't store the files in
github but download them from their original sources and add them to a specific
directory that is ignored by the repo. Each `genome` or `project` directory
should have a `build` directory for these large files.

## Genomes ##

+ C. elegans
+ D. melanogaster
+ A. thaliana
- D. rerio
- M. musculus
- O. sativa
- S. cereviseae
- S. pombe

## Projects ##

Started

- imeter
- gendl
- splicing

Not started

- qalpha
