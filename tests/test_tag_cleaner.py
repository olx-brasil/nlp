# -*- coding: utf-8 -*-

import sys
sys.path.append('.')

import unittest
from unittest import TestCase
from nlp.tag_cleaner import TagCleaner

import re

class TestTagCleaner(TestCase):
    tc = None

    def setUp(self):
        self.tc = TagCleaner()

    def tearDown(self):
        self.tc = None

    def testLoadModel(self):
        self.tc.loadModel('tagger')
        self.assertIsNotNone(self.tc.getModel())

    def testCleanNoWords(self):
        result = self.tc.cleanNoWords('abc 123 abc123 123abc 123abc456 def')
        result = re.sub(r'\s+', ' ', result)
        self.assertEqual(result, 'abc def')

    def testTokenize(self):
        sentence = 'Eu vou fazer um ovo mexido. Quer 1 ou 2 ovos ?'
        tokens = self.tc.tokenize(sentence)
        self.assertEqual(tokens, ['eu', 'vou', 'fazer', 'um', 'ovo', 'mexido', 'quer', 'ou', 'ovos'])


if __name__ == '__main__':
    unittest.main()
