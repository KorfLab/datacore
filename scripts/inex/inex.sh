#!/usr/bin/env bash

GENEPATH=~/datacore/genome_celegans/build/mini_gene

for gene_dir in ${GENEPATH}/*; do
	python3 inex.py --fa ${gene_dir}/*.fa --gff ${gene_dir}/*.gff --out ${gene_dir}/inex
done
