#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, urllib
import re
import sys

# Edit here for default number of results
MAX_RESULTS = 20

class Dict:
    def __init__(self):
        self.Eng = []
        self.De = []

    def getResponse(self, word):
        # Trick to avoid dict.cc from denying the request: change User-agent to firefox's
        req = urllib2.Request("http://www.dict.cc/?s="+word, None, {'User-agent': 'Mozilla/5.0'})
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

        else:
            # Regex
            # pattern = "\"[A-Za-z \.()\-\?ßäöüÄÖÜéáíçÇâêî\']*\""
            pattern = "\"[^,]+\""

            # Return list of matching strings
            self.engWords = re.findall(pattern, engLine)
            self.deWords = re.findall(pattern, deLine)

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
            print "<title>%s not found</title>" % expression
            print "<icon>de_en.png</icon>"
            print "</item>"

        else:
            length, minWords = self.getOutputLength()

            for word_idx in range(minWords):
                if self.engWords[word_idx] == "\"\"": continue
                print "<item>"
                print "<title>%s</title>" % self.engWords[word_idx].strip("\"")
                print "<subtitle>%s</subtitle>" % self.deWords[word_idx].strip("\"")
                print "<icon>de_en.png</icon>"
                print "</item>"

        print "</items>"


if __name__ == "__main__":
    expression = ""
    for index in range(1, len(sys.argv)):
        expression += sys.argv[index] + " "
    expression = urllib.quote(expression)

    myDict = Dict()
    myDict.getResponse(expression)
    myDict.parseResponse()
    myDict.printXMLResults(expression)
