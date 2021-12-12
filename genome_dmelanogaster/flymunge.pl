#!/usr/bin/perl
use strict;
use warnings FATAL => 'all';

open(my $fh, "gunzip -c $ARGV[0] |") or die;
my %keep = (
	gene => 1,
	mRNA => 1,
	exon => 1,
	intron => 1,
	CDS => 1,
	five_prime_UTR => 1,
	three_prime_UTR => 1,
	exon_junction => 1,
);

while (my $line = <$fh>) {
	next if $line =~ /^#/;
	my @f = split(/\s+/, $line);
	next unless @f >= 7;
	next unless $f[0] eq '2L' or $f[0] eq '2R' or $f[0] eq '3L' or $f[0] eq '3R'
		or $f[0] eq '4' or $f[0] eq 'X' or $f[0] eq 'Y';
	next unless $f[1] eq 'FlyBase';
	next unless defined $keep{$f[2]};
	if ($f[2] eq 'exon_junction') {
		if ($line =~ /modENCODE_mRNA-Seq_U_junctions:(\d+)/) {
			$f[1] = 'RNASeq_splice'; # converting to WormBase terminology
			$f[2] = 'intron'; # also covnerting to WormBase
			$f[3] = $f[3] + 1; # FlyBase uses exon coordinates rather than intron
			$f[4] = $f[4] - 1;
			$f[5] = $1;
			$line = join("\t", @f);
			$line .= "\n";
		} else {
			next;
		}
	}
	print $line;
}

__END__


