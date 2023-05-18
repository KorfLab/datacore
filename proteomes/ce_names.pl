use strict;
use warnings;

# use full wormbase.gff3 file

print "# name, pid, tid, gid\n";
my $token = '[\w\.\-]+';
while (<>) {
	my @f = split;
	next unless $f[1] eq 'WormBase' and $f[2] eq 'mRNA';
	my ($tid) = $f[8] =~ /ID=Transcript:($token)/;
	my ($gid) = $f[8] =~ /Parent=Gene:($token)/;
	my ($pid) = $f[8] =~ /wormpep=($token)/;
	my ($name) = $f[8] =~ /Name=($token)/;
	if ($name =~ /(\w+\.\w+)\.\w+/) {
		$name = $1;
	}
	print "$name\t$pid\t$tid\t$gid\n";
}