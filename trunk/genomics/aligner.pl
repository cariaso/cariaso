#!/usr/bin/perl

use strict;
use warnings;

use Data::Dumper;
use FileHandle;
use Bio::SeqIO;
use lib '/mnt/bioperlhack/lib/perl5/';
use Bio::Tools::Run::Alignment::Sim4;


BEGIN { $ENV{CLUSTALDIR} = '/usr/local/runblast/' }
use Bio::Tools::Run::Alignment::Clustalw;

use Bio::PrimarySeq;

my $fasta = FileHandle->new("/mnt/mnt/keepers/allsnps-20070802.fasta");
my $seq_in = Bio::SeqIO->new('-fh' => $fasta,
			     '-format' => 'fasta');


my $sim4 = Bio::Tools::Run::Alignment::Sim4->new();
$sim4->executable('/usr/local/runblast/sim4');


my @params = ('ktuple' => 2, 'matrix' => 'BLOSUM');
my $factory = Bio::Tools::Run::Alignment::Clustalw->new(@params);

my $count = "seq000";

my $resultsdir = 'results';

while (my $inseq = $seq_in->next_seq) {

    eval {
	my ($rsid) = $inseq->display_id() =~ /\|(rs\d+)/;
	
	#next unless $rsid =~ /rs(4420638)/;
	#next unless $rsid =~ /rs(6318|1800321|3788853|4420638)/;
	print "checking $rsid\n";
	
	if (!-e "$resultsdir/$rsid-hits.fasta") {
	    print "no $rsid-hits\n";

	} else {


	    $inseq->seq(uc $inseq->seq);

	    my $readsin = Bio::SeqIO->new('-file' => "$resultsdir/$rsid-hits.fasta",
					  '-format' => 'fasta');
	    my @reads = ();
	    while (my $readseq = $readsin->next_seq) {
		push @reads, $readseq;
	    }


	    my @fwd = ();
	    my @rev = ();
	    my %lookup = ();
	    foreach my $read (@reads) {
		$lookup{$read->id} = $read;
	    }

	    my @exon_sets = $sim4->align(\@reads, $inseq);
	    #print Dumper $exon_sets[0];
	    my $reflen = $inseq->length;
	    my $snppos = $reflen / 2;
	    foreach my $set (@exon_sets){
		foreach my $exon($set->sub_SeqFeature){


		    print "hit of $reflen got ".$exon->start."\t".$exon->end."\t".$exon->strand;
		    print "\tMatched ".$exon->est_hit->seq_id." \t".$exon->est_hit->start." \t".$exon->est_hit->end."\n";

		    if (($exon->start < $snppos) && ($exon->end > $snppos)) {



			if ($exon->strand == 1) {
			    push @fwd, $lookup{$exon->est_hit->seq_id};
			    print "fwd ",$exon->est_hit->seq_id,"\n";
			} else {
			    print "rev ",$exon->est_hit->seq_id,"\n";
			    my $fwd = $lookup{$exon->est_hit->seq_id};
			    if (!$fwd) {
				print STDERR "*****Failure on $rsid ",$exon->est_hit->seq_id,"\n";
			    } else {

				my $old = $fwd->seq;
				my $new = join('', reverse(split(//,$fwd->seq)));
				$new =~ tr/ATCG/TAGC/;
				my $rev = Bio::PrimarySeq->new(-id => "r_".$fwd->display_id, 
							       -seq => $new);
				push @rev, $rev;
			    }
			}


		    }


		}

	    }     
	    if (($#fwd >= 0) || ($#rev >= 0)) {
		
		eval {
		    my $raln = $factory->align([@rev, @fwd, $inseq]);
		    my $rout = Bio::AlignIO->new(-file   => ">$resultsdir/$rsid.aln" ,
						 -format => 'clustalw');
		    $rout->write_aln($raln);
		};
		if ($@) {
		    print STDERR "error with $rsid\n";
		}
	    }
	    
	}

    };
    if ($@) {
	print STDERR "Error: $@\n";
    }
}



