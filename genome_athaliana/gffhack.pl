#!/usr/bin/perl
use strict;
use warnings;


my %splice;
foreach my $file (`ls build/RNA-seq/*`) {
	chomp $file;
	print STDERR $file, "\n";
	my $stage;
	if    ($file =~ /Aerial/) {$stage = 'aer'}
	elsif ($file =~ /Carpel/) {$stage = 'car'}
	elsif ($file =~ /Dark/)   {$stage = 'dgs'}
	elsif ($file =~ /Light/)  {$stage = 'lgs'}
	elsif ($file =~ /Leaf/)   {$stage = 'lea'}
	elsif ($file =~ /Pollen/) {$stage = 'pol'}
	elsif ($file =~ /Recept/) {$stage = 'rec'}
	elsif ($file =~ /Root A/) {$stage = 'ram'}
	elsif ($file =~ /Root/)   {$stage = 'roo'}
	elsif ($file =~ /Shoot/)  {$stage = 'sam'}
	elsif ($file =~ /Stage/)  {$stage = 's12'}
	else {die "not possible"}
	
	open(my $fh, $file) or die "$file not found\n";
	while (<$fh>) {
		next if /^#/;
		my ($chr, $t, $s, $beg, $end, $n, $str, $p, $g) = split;
		$splice{$chr}{$beg}{$end}{$str}{$stage} += $n;
	}
	close $fh;
}

# the RNA-seq data appended
foreach my $chr (sort keys %splice) {
	foreach my $beg (sort {$a <=> $b} keys %{$splice{$chr}}) {
		foreach my $end (sort {$a <=> $b} keys %{$splice{$chr}{$beg}}) {
			foreach my $str (keys %{$splice{$chr}{$beg}{$end}}) {
				foreach my $stage (keys %{$splice{$chr}{$beg}{$end}{$str}}) {
					print join("\t", $chr, 'RNASeq_splice', 'intron',
						$beg, $end,
						$splice{$chr}{$beg}{$end}{$str}{$stage}, $str, '.',
						"ID=$stage"), "\n";
				}
			}
		}
	}
}
