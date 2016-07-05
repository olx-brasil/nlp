#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

from nlp.tag_cleaner import TagCleaner
import pkg_resources
import os, sys
import pickle

tag_cleaner = TagCleaner()

tag_cleaner.loadModel('tagger')

body_raw = sys.stdin.read()

body_final = tag_cleaner.cleanBody(body_raw)

print body_final
