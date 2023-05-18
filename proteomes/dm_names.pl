use strict;
use warnings;

# use flybase protein fasta file

print "# name, pid, tid, gid\n";
my $token = '[\w\.\-\(\)]+';
while (<>) {
	next unless /^>/;
	my ($pid) = $_ =~ />($token)/;
	my ($gid, $tid) = $_ =~ /parent=($token),($token)/;
	my ($name) = $_ =~ /name=($token)/;
	print "$name\t$pid\t$tid\t$gid\n";
}