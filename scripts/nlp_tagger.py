#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

from nlp.tag_cleaner import TagCleaner
import pkg_resources
import os, sys
import pickle
from optparse import OptionParser
import codecs

parser = OptionParser()
parser.set_usage('Usage: nlp_tagger.py [FILE]')
parser.add_option('-e', '--encoding', help='Set the input encoding (Default to UTF-8)', dest='encoding', default='utf-8')
parser.set_description(
"""
FILE\tThe file with body content (If ommited use stdin instead)
"""
)

(options, args) = parser.parse_args()

if (len(args) > 0):
    file_input = open(args[0], 'r')
else:
    file_input = sys.stdin

with file_input as f:
    body_raw = codecs.getreader(options.encoding)(f).read()

tag_cleaner = TagCleaner()

tag_cleaner.loadModel('tagger')

body_final = tag_cleaner.cleanBody(body_raw)

print body_final
