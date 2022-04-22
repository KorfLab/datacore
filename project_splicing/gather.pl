
my $root = "build/genes";
while (<>) {
	next if /^#/;
	my ($id) = split;
	system("cp $root/$id.fa apc");
	system("cp $root/$id.gff3 apc");
}
