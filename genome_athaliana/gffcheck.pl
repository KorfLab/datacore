#!/usr/bin/perl
use strict;
use warnings;

open(my $fh, $ARGV[0]) or die;
my %type;
my $i = 0;
while (<$fh>) {
#last if $i++ == 100000;
	next if /^#/;
	my @f = split;
	next unless @f >= 7;
	$type{$f[1]}{$f[2]}++;
}

display(\%type);


sub display {
	my ($d) = @_;
	foreach my $k (sort keys %$d) {
		print "$k\n";
		foreach my $k2 (sort keys %{$d->{$k}}) {
			print "\t$k2\t$d->{$k}{$k2}\n";
		}
	}
}

__END__

