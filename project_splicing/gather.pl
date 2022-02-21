
my $root = "../genome_celegans/build/genes";
while (<>) {
	next if /^#/;
	my ($id) = split;
	system("cp $root/$id.fa apc/$id.fa");
	system("cp $root/$id.gff3 apc/$id.gff");
}
