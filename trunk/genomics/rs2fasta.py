#!/usr/bin/python

import sys
import re
import string
import getopt
import unicodedata
    

import Bio.EUtils
from Bio.EUtils import HistoryClient
Bio.EUtils.Config._add_db(Bio.EUtils.Config.DatabaseInfo("snp", 1))




            
def standardize(fin):
    header = None
    body = ''
    message = None
    for line in fin.splitlines():
        if line:
            firstchar = line[0]
            if firstchar == '>':
                header = line
            elif firstchar in string.digits:
                message = line
            else:
                body += line.replace(' ','').strip()
    if header:
        return "%s\n%s" % (header, body)
    else:
        print >>sys.stderr, message
        return None



def showFasta(rsnums):
    client = HistoryClient.HistoryClient()

    for rsnum in rsnums:
        try:
            request = Bio.EUtils.DBIds("snp", rsnum)
            result = client.post(request)
            infile = result.efetch(retmode = "text", rettype = "fasta")
            fasta = infile.read()
            stdFasta = standardize(fasta)
            if stdFasta:
                print stdFasta
        except Exception, e:
            print >>sys.stderr, e





    
import sys

if __name__ == '__main__':
    showFasta(sys.argv[1:])
