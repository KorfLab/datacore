
my $root = "../genome_celegans/build/genes";
while (<>) {
	next if /^#/;
	my ($id) = split;
	system("cat $root/gene$id/$id.fa > apc/$id.fa");
	system("cat $root/gene$id/$id.gff > apc/$id.gff");
}
