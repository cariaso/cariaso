#!/usr/bin/perl

use strict;
use warnings;

use Data::Dumper;
use FileHandle;
use Bio::SeqIO;



use strict;
use Bio::SearchIO; 


my $infn = '-';
$infn = $ARGV[0] if $ARGV[0];

my $in = new Bio::SearchIO(-format => 'blast', 
                           -file   => $infn);

while( my $result = $in->next_result ) {
    while( my $hit = $result->next_hit ) {
	

	print $result->query_name," ",$hit->name,"\n";

    }
}

