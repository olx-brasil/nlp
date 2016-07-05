# -*- coding: utf-8 -*-

import sys
sys.path.append('.')

import unittest
from unittest import TestCase
from nlp.tag_cleaner import TagCleaner

import re

class TestTagCleaner(TestCase):
    tc = None
    model = 'tagger'

    def setUp(self):
        self.tc = TagCleaner()

    def tearDown(self):
        self.tc = None

    def testLoadModel(self):
        self.tc.loadModel(self.model)
        self.assertIsNotNone(self.tc.getModel())

    def testCleanNoWords(self):
        result = self.tc.cleanNoWords('abc 123 abc123 123abc 123abc456 def')
        result = re.sub(r'\s+', ' ', result)
        self.assertEqual(result, 'abc def')

    def testTokenize(self):
        sentence = 'Eu vou fazer um ovo mexido. Quer 1 ou 2 ovos ?'
        tokens = self.tc.tokenize(sentence)
        self.assertEqual(tokens, ['eu', 'vou', 'fazer', 'um', 'ovo', 'mexido', 'quer', 'ou', 'ovos'])

    def testTag(self):
        sentence = u'o abacaxi está maduro'
        words = re.split(r'\s+', sentence, re.U)
        self.tc.loadModel(self.model)
        tokens = self.tc.tag(words)
        entities = map(lambda token: token[-1], tokens)
        self.assertEqual(entities, [u'ART', u'N', u'V', u'ADJ'])

    def testMarkWindowed(self):
        sentence = u'o abacaxi está maduro e ainda tem laranja, mandioca, banana, carro, caminhão, loja e aipim'
        words = re.split(r'\s+', sentence, re.U)
        self.tc.loadModel(self.model)
        tags_marked = self.tc.markWindowed(self.tc.tag(words))
        flags = map(lambda x: x[-1], tags_marked)
        self.assertEqual(flags, ['0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '0', '0'])

    def testFilterBodyDel(self):
        marks = [('', '', '0'), ('', '', '1'), ('', '', '2'), ('', '', '3')]
        self.assertEqual([('', '', '0')], self.tc.filterBodyDel(marks))

    def testFilterBodyMorf(self):
        marks = [('a', 'ADJ', ''), ('b', 'N', ''), ('x', 'XXX', ''), ('c', 'PCP', ''), ('d', 'V', '')]
        self.assertEqual('abcd', ''.join(self.tc.filterBodyMorf(marks)))


if __name__ == '__main__':
    unittest.main()
