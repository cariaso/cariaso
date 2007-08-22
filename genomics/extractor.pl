#!/usr/bin/perl

use strict;
use warnings;

use Data::Dumper;
use FileHandle;
use Bio::SeqIO;

my $fnin = $ARGV[0];
#my $fhin = FileHandle->new("gzip -dc /mnt/mnt/keepers/allsnps-20070802.blasttable.gz |");
my $fhin = FileHandle->new($fnin);

my $max = 1000;
my $count=0;
my $wanted = {};
while (my $line = <$fhin>) {
    my ($rs, $id) = $line =~ /\|(rs\d+).*? gnl\|ti\|(\d+)/;
    $wanted->{$id}->{$rs}++;

    $count++;
}
print "loaded $count blast rows\n";
#print Dumper \$wanted;



my $file = $ARGV[1];
my $fasta = FileHandle->new("gzip -dc $file |");




my $seq_in = Bio::SeqIO->new('-fh' => $fasta,
			     '-format' => 'fasta');

$count = 0;
my $resultsdir = 'results';
`mkdir -p $resultsdir`;
my $seq_out;
#my @wanted;
my $wanted2;
my $id;
my $inseq;
while ($inseq = $seq_in->next_seq) {
    ($id) = $inseq->display_id() =~ /\|(\d+)/;
    $count++;

     foreach my $rs (keys %{$wanted->{$id}}) {
	 $seq_out = Bio::SeqIO->new('-file' => ">>$resultsdir/$rs-hits.fasta",
				    '-format' => 'fasta');
	 $seq_out->write_seq($inseq);
	 $seq_out->close();
     }
}

print "scanned $count fasta records in $file\n";


