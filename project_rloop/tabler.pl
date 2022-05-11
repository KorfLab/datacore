use strict;
use warnings FATAL => 'all';

die "usage: $0 <file1> <file2>\n" unless @ARGV == 2;


my $d0 = read_file($ARGV[0]);
my $d1 = read_file($ARGV[1]);

foreach my $k1 (sort keys %$d0) {
	foreach my $k2 (sort keys %{$d0->{$k1}}) {
		print join("\t",
			$k1,
			$k2,
			$d0->{$k1}{$k2},
			$d1->{$k1}{$k2},
			abs($d0->{$k1}{$k2} - $d1->{$k1}{$k2})), "\n";
	}	
}


sub read_file {
	my ($file) = @_;
	my %d;
	open(my $fh, $file) or die;
	while (<$fh>) {
		my ($f1, $f2, $v) = split;
		my $t1 = make_name($f1);
		my $t2 = make_name($f2);
		$d{$t1}{$t2} = $v;
	}
	return \%d;
}

sub make_name {
	my ($text) = @_;
	
	my $name = "";
	if ($text =~ /HeLa/) {$name .= "H"}
	else                 {$name .= "K"}
	
	my ($n) = $text =~ /_rep(\d)_/;
	$name .= $n;
	
	if ($text =~ /_neg/) {$name .= "-"}
	else                 {$name .= "+"}
	
	return $name;
}