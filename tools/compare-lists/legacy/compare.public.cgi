#! /usr/local/bin/perl -w

use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser set_message);

# Copyright(c) 2011 Whitehead Institute for Biomedical Research.
#              All Rights Reserved
#
# Author: George Bell
#         Bioinformatics and Research Computing
#         wibr-bioinformatics@wi.mit.edu

$input = new CGI;
print $input->header('text/html');

BEGIN
{
	sub handle_errors
	{
		my $msg = shift;
		print "<h1>Uh oh</h1>";
		print "Got an error: <PRE>$msg";
	}
	set_message(\&handle_errors);
}

if (param())
{
	$list1 = param("list1");
	$list2 = param("list2");
	$name1 = param("name1");
	$name2 = param("name2");
	$case = param("case");
}

if (! $list1 || ! $list2)
{
	print "<FONT COLOR=\"red\"><B>There seems to be incomplete input data.  What's up with that?</B></FONT>\n";
	print $input->end_html;
	exit(0);
}

##################  first list  ##################

@list1 = split (/\n/, $list1);

# Drop whitespace entries
foreach $x (@list1)
{
	if ($x !~ /^\s*$/)
	{
		$x =~ s/^\s+//;
		$x =~ s/\s+$//;
		push (@a, $x);
	}
}

# Make non-redundant
%seen = ();
@a_nr = ();
foreach $item (@a)
{
	if ($case)
	{
		unless ($seen{lc($item)})
		{
			$seen{lc($item)}++;
			push(@a_nr, lc($item));
		}
	}
	else
	{
		unless ($seen{$item})
		{
			$seen{$item} = 1;
			push(@a_nr, $item);
		}
	}
}

@a = sort(@a_nr);

##################  second list  ##################


@list2 = split (/\n/, $list2);

# Drop whitespace entries
foreach $x (@list2)
{
	if ($x !~ /^\s*$/)
	{
		$x =~ s/^\s+//;
		$x =~ s/\s+$//;
		push (@b, $x);
	}
}

# Make non-redundant
%seen = ();
@b_nr = ();
foreach $item (@b)
{
	if ($case)
	{
		unless ($seen{lc($item)})
		{
			$seen{lc($item)}++;
			push(@b_nr, lc($item));
		}
	}
	else
	{
		unless ($seen{$item})
		{
			$seen{$item} = 1;
			push(@b_nr, $item);
		}
	}
}

@b = sort(@b_nr);

######################################################

# Initialize
@union = @isect = ();
%union = %isect = ();

foreach $e (@a)
	{ $union{$e} = 1; }

foreach $e (@b)
{
    if ( $union{$e} )
    { $isect{$e} = 1; }
    $union{$e} = 1;
}
@union = sort(keys %union);
@isect = sort(keys %isect);

foreach $e (@a)
	{ $inA{$e} = 1; }
foreach $e (@b)
	{ $inB{$e} = 1; }

foreach $a (@a)
{
	if (! $inB{$a})
	{ push (@aOnly, $a); }
}
foreach $b (@b)
{
	if (! $inA{$b})
	{ push (@bOnly, $b); }
}

print "<BODY LINK=\"FF0000\" VLINK=\"0000FF\" LEFTMARGIN=0 TOPMARGIN=0 BGCOLOR=\"#ffffff\"><CENTER>\n";

print "<FONT SIZE=+2><B>Comparison of two lists</B></FONT><BR><BR>\n";

$list1size = $#a + 1;

print "<TABLE WIDTH=800 BGCOLOR=#FFE4B5><TR ALIGN=CENTER>";
print "<TD>$name1 ($list1size):<BR>\n";
print "<TEXTAREA NAME=\"list1\" ROWS=10 COLS=20>\n";
foreach $x (@a)
{ print "$x\n"; }
print "</TEXTAREA></TD>\n";

$list1onlysize = $#aOnly + 1;

print "<TD>$name1 <FONT COLOR=\"red\">only</FONT> ($list1onlysize):<BR>\n";
print "<TEXTAREA NAME=\"aOnly\" ROWS=10 COLS=20>\n";
foreach $x (@aOnly)
{ print "$x\n"; }
print "</TEXTAREA></TD>\n";

$unionSize = $#union + 1;

print "<TD>$name1 <FONT COLOR=\"red\">or</FONT> $name2 ($unionSize):<BR>\n";
print "<TEXTAREA NAME=\"union\" ROWS=10 COLS=20>\n";
foreach $x (@union)
{ print "$x\n"; }
print "</TEXTAREA></TD></TR>\n";

$list2size = $#b + 1;

print "<TR ALIGN=CENTER><TD>$name2 ($list2size):<BR>\n";
print "<TEXTAREA NAME=\"list2\" ROWS=10 COLS=20>\n";
foreach $x (@b)
{ print "$x\n"; }
print "</TEXTAREA></TD>\n";

$list2onlysize = $#bOnly + 1;

print "<TD>$name2 <FONT COLOR=\"red\">only</FONT> ($list2onlysize):<BR>\n";
print "<TEXTAREA NAME=\"bOnly\" ROWS=10 COLS=20>\n";
foreach $x (@bOnly)
{ print "$x\n"; }
print "</TEXTAREA></TD>\n";

$isectSize = $#isect + 1;

print "<TD>$name1 <FONT COLOR=\"red\">and</FONT> $name2 ($isectSize):<BR>\n";
print "<TEXTAREA NAME=\"isect\" ROWS=10 COLS=20>\n";
foreach $x (@isect)
{ print "$x\n"; }
print "</TEXTAREA></TD></TR>\n";

print "</TABLE>\n";

print "<BR>Notes:<BR>";

if ($case)
{
	print "Comparisons are case-insensitive (by converting items to lowercase).<BR>\n";
}
else
{
	print "Comparisons are case-sensitive.<BR>\n";
}

print "Duplicate entries are removed from each list before processing<BR>
and all lists are alphabetically ordered.\n";

print "
<BR><BR>
<CENTER>
<A HREF=\"compare.public.php\">Compare two more lists</A><BR><BR>
</CENTER>\n";


print $input->end_html;

