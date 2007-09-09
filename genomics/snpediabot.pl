#!/usr/bin/perl

use warnings;
use strict;

use Perlwikipedia;
use DirHandle;
use FileHandle;


my $dirname = "results";
my $d = DirHandle->new($dirname);
if (!defined $d) {
    print STDERR "undef $dirname\n";
    exit;
}


my $bot = Perlwikipedia->new();
$bot->set_wiki('www.snpedia.com','/');
$bot->login('SNPediaBot');

while (defined(my $entry = $d->read)) {
    next unless $entry =~ /-tight\.aln$/;
    my $fh = FileHandle->new("$dirname/$entry");
    my ($rsnum) = $entry =~ /(rs\d+)/;

    #next if $rsnum =~ /rs4420638$/i; # Watson asked not to know this one

    my @lines = grep {!/^\s*$/} grep {!/CLUSTAL/} <$fh>;
    

    my $text = $bot->get_text('User:Venter');
    $text .= "\n\n{{ venter alignment | snp=$rsnum | preformatted=\n<pre>";
    $text .= join('', @lines);
    $text .= "</pre>\n}}\n";
    #$text =~ s/(dbSNP\|)(rs\d+)/$1\[\[$2\]\]/;
    print "$rsnum\n";
    print $text;
    $bot->edit('User:Venter', $text, 'adding venter analysis');
}

