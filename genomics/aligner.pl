#!/usr/bin/perl

use strict;
#use warnings;

use Data::Dumper;
use FileHandle;
use Bio::SeqIO;
use lib '/mnt/bioperlhack/lib/perl5/';
use Bio::Tools::Run::Alignment::Sim4;


BEGIN { $ENV{CLUSTALDIR} = '/usr/local/runblast/' }
use Bio::Tools::Run::Alignment::Clustalw;

use Bio::PrimarySeq;

if (!@ARGV) {
    usage();
}


my $allsnps_fn = $ARGV[0];



my $countsfh = FileHandle->new(">/tmp/counts-venter.txt");
my $fasta = FileHandle->new($allsnps_fn);
my $seq_in = Bio::SeqIO->new('-fh' => $fasta,
			     '-format' => 'fasta');




my $sim4 = Bio::Tools::Run::Alignment::Sim4->new();
$sim4->executable('/usr/local/runblast/sim4');


my @params = ('ktuple' => 2, 'matrix' => 'BLOSUM');
my $factory = Bio::Tools::Run::Alignment::Clustalw->new(@params);

my $count = "seq000";

my $resultsdir = 'results';

while (my $inseq = $seq_in->next_seq) {
    my %seen = ();

    eval {
	my ($rsid) = $inseq->display_id() =~ /\|(rs\d+)/;
	
	#next unless $rsid =~ /rs(662799)/;
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

	    #my $www;
	    #map {$www->{$_}++} split(/\s+/,join(' ',`cat wanted.txt`));


	    my @exon_sets = $sim4->align(\@reads, $inseq);
	    #print Dumper $exon_sets[0];
	    my $reflen = $inseq->length;
	    my $snppos = $reflen / 2;
	    if ($inseq->display_id() =~ /allelePos=(\d+)/) {
		$snppos = $1;
	    }
	    if ($inseq->desc() =~ /allelePos=(\d+)/) {
		$snppos = $1;
	    }
	    if ($inseq->desc() =~ /\|pos=(\d+)/) {
		$snppos = $1;
	    }

	    foreach my $set (@exon_sets){
		foreach my $exon($set->sub_SeqFeature){


#		    my ($gi) = $exon->est_hit->seq_id =~ /(\d+)/;
#		    if ($www->{$gi}) {
# 			print "+";
# 		    } else {
# 			print "-";
# 		    }
# 		    print "\t";

		    print $exon->percentage_id,"\t",($exon->est_hit->end - $exon->est_hit->start),"\t";

		    print "hit of $reflen got ".$exon->start."\t".$exon->end."\t".$exon->strand;
		    print "\tMatched ".$exon->est_hit->seq_id." \t".$exon->est_hit->start." \t".$exon->est_hit->end;
		    

		    if (($exon->start > $snppos) || ($snppos > $exon->end)) {
			print "\tdoes not straddle snp at $snppos\n";
			next;
		    }

		    if ($exon->percentage_id < 80) {
			print "\trejected ",$exon->percentage_id,"% ident\n";
			next;
		    }
		    
		    my $length = $exon->est_hit->end - $exon->est_hit->start;
		    if ( $length < 50) {
			print "\trejected length=$length\n";
			next;
		    }



		    if ($seen{$exon->est_hit->seq_id}) {
			print "\trejected duplicate",$exon->est_hit->seq_id,"\n";
			next;
		    }



		    $seen{$exon->est_hit->seq_id}++;

		    if ($exon->strand == 1) {
			push @fwd, $lookup{$exon->est_hit->seq_id};
			print "\tfwd ",$exon->est_hit->seq_id;
		    } else {
			print "\trev ",$exon->est_hit->seq_id;
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
		    

		    print "\n";


		}

	    }     
	    if (($#fwd >= 0) || ($#rev >= 0)) {
		
		eval {


		    my $raln = $factory->align([@rev, @fwd, $inseq]);

		    my $rout = Bio::AlignIO->new(-file   => ">$resultsdir/$rsid.aln" ,
						 -format => 'clustalw');
		    $rout->write_aln($raln);


		    my $id = $inseq->display_id;
		    my $id2 = substr($id, 0, 30);
		    print "$id ->\n$id2\n";
		
		    my $pos = $raln->column_from_residue_number($id2, $snppos);
		    print "Adjusted $snppos -> $pos\n";


		    my $mini_aln = $raln->slice($pos-8,$pos+8);
		    my $tightfn = "$resultsdir/$rsid-tight.aln";
		    my $sout = Bio::AlignIO->new(-file   => ">$tightfn",
						 -format => 'clustalw');
		    $sout->write_aln($mini_aln);
		    print `cat $tightfn`;


		    my $rout = Bio::AlignIO->new(-file   => ">$resultsdir/$rsid.aln" ,
						 -format => 'clustalw');
		    $rout->write_aln($raln);

		    my %count = ();
                    foreach my $seq ($raln->each_seq) {
			my $res = $seq->subseq($pos, $pos);
			$count{uc $res}++;
		    }
		    print Dumper \%count;
		    print $countsfh join("\t", $inseq->display_id,$count{A}, $count{T}, $count{C}, $count{G}, $count{N}, $count{'.'}),"\n";
		    $countsfh->flush();



		};
		if ($@) {
		    print STDERR "error with $rsid $@\n";
		}
	    }
	    
	}

    };
    if ($@) {
	print STDERR "Error: $@\n";
    }
}



sub usage {
    print "$0 rssnps.fasta";
    exit;
}
