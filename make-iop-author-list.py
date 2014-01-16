#!/usr/bin/env python

"""make-iop-author-list.py: Generates LaTeX code for the author list of an IOP paper."""

__author__      = "Leo C. Stein"
__copyright__   = "Copyright 2014"

import sys, string

def readAffilMap(filename):
    """ Reads from filename a map of {affiliation-key: affiliation-address}. """
    
    f = open(filename, 'r')
    affilMap = dict([tuple(l.rstrip().split(None,1)) for l in f.readlines()])
    f.close()
    
    return affilMap

def readAuthorList(filename):
    """ Reads from filename a list of lists [author-name, [affiliation-keys]]. """
    
    f = open(filename, 'r')
    authorList = map( lambda x: [ x[0], x[1].split(',') ],
                      [l.rstrip().split(None,1) for l in f.readlines()] )
    f.close()
    
    return authorList

def makeAffilOrder(authorList, affilMap):
    """ Returns an ordered list of the affiliation-keys according to the author order. """
    
    # This is probably slow. Fix it if you want.
    affilOrder = []
    for auth in authorList:
        for affil in auth[1]:
            if affil not in affilOrder:
                affilOrder.append(affil)
    
    return affilOrder

def authorSuperscripts(authorList, affilKeyOrder):
    """ Make the ordered list of [author, [superscripts]]. """
    
    # Add one because superscripts are 1-indexed
    superscriptNumber = lambda affilKey: affilKeyOrder.index(affilKey)+1
    
    return [ [auth[0], map(superscriptNumber, auth[1])] for auth in authorList]

def authorsString(authorList, affilKeyOrder):
    """ Make a string of LaTeX for the authors with superscripts for affiliations. """
    
    authSScripts = authorSuperscripts(authorList, affilKeyOrder)
    # this is the string format for one line, with no trailing comma
    authLine = lambda auth: auth[0] + "$^{" + (",".join([str(i) for i in auth[1]])) + "}$"
    
    authLines = map( authLine, authSScripts )
    return "\\author{%\n" + ( ",\n".join(authLines[:-1]) ) + "\nand\n" + authLines[-1] + "\n}"

def affilsString(affilKeyOrder, affilMap):
    """ Make a string of LaTeX for the affiliations with superscripts. """
    
    affilLine = lambda (affilKey, number): "\\address{$^{" + str(number) + "}$~" + affilMap[affilKey] + "}"
    return "\n".join(map(affilLine, zip(affilKeyOrder, range(1, 1+len(affilKeyOrder)))))

# The following could be improved with defaults, command line parsing, output to a named file, etc.
def main(authorsFilename, affilsFilename):
    """ Entry point for the script. """

    authorList = readAuthorList(authorsFilename)
    affilMap   = readAffilMap(affilsFilename)
    
    affilKeyOrder = makeAffilOrder(authorList, affilMap)
    
    print "% AUTO-GENERATED WITH make-iop-author-list.py"
    print "% FROM " + authorsFilename + " AND " + affilsFilename
    print authorsString(authorList, affilKeyOrder)
    print
    print affilsString(affilKeyOrder, affilMap)

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])
