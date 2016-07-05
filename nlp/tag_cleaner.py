# -*- coding: utf-8 -*-

import re
import pickle
from nlp.resource import Resource

class TagCleaner:
    model = None
    split_regex = re.compile('\W+', re.U)

    def __init__(self):
        pass

    def loadModel(self, modelName):
        resource_package = __name__
        with open(Resource.getResourcePath('data', "%s.dat" % modelName), 'r') as f:
            self.model = pickle.load(f)

    def getModel(self):
        return self.model

    def cleanNoWords(self, text):
        return re.sub(r'\w*\d+\w*', '', text)

    def tokenize(self, text):
      return [t for t in re.split(self.split_regex, text.lower()) if len(t) > 1 or t in ['a','e','o']]

    def tag(self, words):
      return self.model.tag(words)

    def markWindowed(self, x):
      aux = [0] * len(x)
      for idx in range(0,len(x)-4):
        if (x[idx][1]==None or x[idx][1]=='N' or x[idx][1]=='N|EST') and \
           (x[idx+1][1]==None or x[idx+1][1]=='N'  or x[idx+1][1]=='N|EST') and \
           (x[idx+2][1]==None or x[idx+2][1]=='N'  or x[idx+2][1]=='N|EST') and \
           (x[idx+3][1]==None or x[idx+3][1]=='N'  or x[idx+3][1]=='N|EST') and \
           (x[idx+4][1]==None or x[idx+4][1]=='N'  or x[idx+4][1]=='N|EST'):
          aux[idx]   = 1
          aux[idx+1] = 1
          aux[idx+2] = 1
          aux[idx+3] = 1
          aux[idx+4] = 1
      for idx, val in enumerate(x):
          x[idx] += (str(aux[idx]), )
      return x

    def filterBodyDel(self, marks):
      return [t for t in marks if t[2]=='0']

    def filterBodyMorf(self, marks):
      return [t[0] for t in marks if t[1] in [None, 'N', 'V', 'PCP', 'ADJ']]

    def countKeep(self, marks):
      count = 0
      for i in marks:
        if i[2] == '0':
          count+=1
      return count

    def countDel(self, marks):
      count = 0
      for i in marks:
        if i[2] == '1':
          count+=1
      return count

    def countN(self, marks):
      count = 0
      for i in marks:
        if i[1] == 'N':
          count+=1
      return count

    def filterMarks(self, marks):
        return self.filterBodyMorf(self.filterBodyDel(marks))

    def cleanBody(self, body):
        body_cleaned = self.cleanNoWords(body)
        tokens = self.tokenize(body_cleaned)

        tags = self.tag(tokens)
        marks = self.markWindowed(tags)
        tokens_cleaned = self.filterMarks(marks)

        return " ".join(tokens_cleaned)
