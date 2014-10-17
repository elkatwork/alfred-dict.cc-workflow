#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, urllib
import re
import sys
import string

# Edit here for default number of results
MAX_RESULTS = 20

class Dict:
    def __init__(self):
        self.Eng = []
        self.De = []

    def getResponse(self, word):
        # Trick to avoid dict.cc from denying the request: change User-agent to firefox's
        req = urllib2.Request("http://www.dict.cc/?s="+word, None, {'User-agent': 'Mozilla/6.0'})
        f = urllib2.urlopen(req)
        self.Response = f.read()

    # Find 'var c1Arr' and 'var c2Arr'
    def parseResponse(self):
        self.engWords = []
        self.deWords = []

        engLine = deLine = ""

        # Split lines
        lines = self.Response.split("\n")

        for l in lines:
            if l.find("var c1Arr") >= 0:
                engLine =  l
            elif l.find("var c2Arr") >= 0:
                deLine = l

        if not engLine or not deLine:
            return False

        pattern = "\"[^,]+\""

        # Return list of matching strings
        self.engWords = map(self.sanitizeWord, re.findall(pattern, engLine))
        self.deWords = map(self.sanitizeWord, re.findall(pattern, deLine))

    def getOutputLength(self):
        # Get minumum number of both eng and de
        minWords = len(self.engWords) if len(self.engWords) <= len(self.deWords) else len(self.deWords)

        # Is it more than MAX_RESULTS?
        minWords = minWords if minWords <= MAX_RESULTS else MAX_RESULTS

        # Find biggest word in first col
        length = 0
        for w in self.engWords[:minWords]:
            length = length if length > len(w) else len(w)

        return length, minWords

    def printXMLResults(self, expression):
        print "<?xml version=\"1.0\"?>"
        print "<items>"

        if not self.engWords or not self.deWords:
            print "<item valid=\"no\">"
            print "<title>'%s' not found</title>" % string.strip(expression)
            print "<icon>de_en.png</icon>"
            print "</item>"

        else:
            length, minWords = self.getOutputLength()

            for word_idx in range(minWords):
                if self.engWords[word_idx] == "\"\"": continue
                print "<item valid=\"yes\" arg=\"%s\">" % self.engWords[word_idx]
                print "<title>%s</title>" % self.engWords[word_idx]
                print "<subtitle>%s</subtitle>" % self.deWords[word_idx]
                print "<icon>de_en.png</icon>"
                print "</item>"

        print "</items>"

    def sanitizeWord(self, word):
        word = word.replace("\\", "")
        return word.strip("\" ")


if __name__ == "__main__":
    expression = ""
    for index in range(1, len(sys.argv)):
        expression += sys.argv[index] + " "

    myDict = Dict()
    myDict.getResponse(urllib.quote(expression))
    myDict.parseResponse()
    myDict.printXMLResults(expression)
