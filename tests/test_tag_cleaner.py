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
        self.assertEqual(result, 'abc abc123 123abc 123abc456 def')

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
        self.assertEqual(entities, [u'DET', u'NOUN', u'VERB', u'ADJ'])

    def testEvaluateClass(self):
        self.tc.addClass('fipe', ['ford', 'palio', 'kombi'])
        self.assertEqual(self.tc.evaluateClass('ford'), 'fipe')
        self.assertEqual(self.tc.evaluateClass('palio'), 'fipe')
        self.assertEqual(self.tc.evaluateClass('bicicleta'), None)
        self.assertEqual(self.tc.evaluateClass('kombi'), 'fipe')

    def testMapClass(self):
        self.tc.addClass('fipe', ['ford', 'palio', 'kombi'])
        mappedClasses = self.tc.mapClass([('ford', 'None'), ('kombi', 'None'), ('bicicleta', 'None'), ('palio', 'None')])
        self.assertEqual(mappedClasses, [('ford', 'fipe'), ('kombi', 'fipe'), ('bicicleta', 'None'), ('palio', 'fipe')])

    def testMarkWindowed(self):
        sentence = u'Amanha vai chover e eu vou trazer o guarda-chuva, mas vou acabar esquecendo no trabalho ' + ' '.join(['palavradesconhecida']*7)
        words = re.split(r'\W+', sentence, flags=re.U)
        self.tc.loadModel(self.model)
        tags_marked = self.tc.markWindowed(self.tc.tag(words))
        flags = map(lambda x: x[-1], tags_marked)
        self.assertEqual(flags, ['0']*16 + ['1']*7)

    def testFilterBodyDel(self):
        marks = [('abc', '', '0'), ('', '', '1'), ('', '', '2'), ('', '', '3')]
        self.assertEqual([('abc')], self.tc.filterBodyDel(marks))

    def testFilterBodyMorf(self):
        marks = [('a', 'ADJ', ''), ('b', 'N', ''), ('x', 'XXX', ''), ('c', 'PCP', ''), ('d', 'V', '')]
        self.assertEqual('abcd', ''.join(self.tc.filterBodyMorf(marks)))


if __name__ == '__main__':
    unittest.main()
