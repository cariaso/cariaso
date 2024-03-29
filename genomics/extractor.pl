#!/usr/bin/perl

use strict;
use warnings;

use Data::Dumper;
use FileHandle;
use Bio::SeqIO;


usage() unless $ARGV[0];

my $fnin = $ARGV[0];


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






use File::Basename;

my $file = $ARGV[1];

my $tis = {};
if ($file =~ /\.idx$/) {
    my $dir = dirname($file);
    my $idxfh = FileHandle->new($file);
    foreach my $line (<$idxfh>) {
	print $line;
	my ($fastagz, $ti) = $line =~ /^(\S+)\s+:\s+>gnl\|ti\|(\d+)\s+/;
	$tis->{$ti} = "$dir/$fastagz";
    }
}

print Dumper $tis;
exit;



my $fasta = FileHandle->new("gzip -dc $file |");









my $seq_in = Bio::SeqIO->new('-fh' => $fasta,
			     '-format' => 'fasta');

$count = 0;
my $resultsdir = 'results';
`mkdir -p $resultsdir`;
my $seq_out;
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


sub usage {

    print "$0 blasttable fasta.gz\n\n";
    print "or\n";
    print "$0 blasttable filename.idx\n\n";
    exit;
}
