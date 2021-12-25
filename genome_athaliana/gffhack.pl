#!/usr/bin/perl
use strict;
use warnings;

my %splice;
foreach my $file (`ls build/RNA-seq/*`) {
	chomp $file;
	print STDERR $file, "\n";
	open(my $fh, $file) or die "$file not found\n";
	while (<$fh>) {
		next if /^#/;
		my ($chr, $t, $s, $beg, $end, $n, $str, $p, $g) = split;
		$splice{$chr}{$beg}{$end}{$str} += $n;
	}
	close $fh;
}

# the original GFF kept as is
system("cat build/TAIR10_GFF3_genes.gff");

# the RNA-seq data appended
my $jct = 1;
foreach my $chr (sort keys %splice) {
	foreach my $beg (sort {$a <=> $b} keys %{$splice{$chr}}) {
		foreach my $end (sort {$a <=> $b} keys %{$splice{$chr}{$beg}}) {
			foreach my $str (keys %{$splice{$chr}{$beg}{$end}}) {
				print join("\t", $chr, 'RNASeq_splice', 'intron', $beg, $end,
					$splice{$chr}{$beg}{$end}{$str}, $str, '.',
					"Name=jct$jct"), "\n";
				$jct++;
			}
		}
	}
}
