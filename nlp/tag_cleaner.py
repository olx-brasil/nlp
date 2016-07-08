# -*- coding: utf-8 -*-

import re
import pickle
from nlp.resource import Resource

class TagCleaner:
    model = None
    split_regex = re.compile('\W+', re.U)
    classes = {}

    def __init__(self):
        pass

    def loadModel(self, model_name):
        resource_package = __name__
        with open(Resource.getResourcePath('data', "%s.dat" % model_name), 'r') as f:
            self.model = pickle.load(f)

    def getModel(self):
        return self.model

    def addClass(self, class_name, words):
        self.classes[class_name] = words

    def evaluateClass(self, word):
        for class_name in self.classes.keys():
            class_set = self.classes[class_name]
            if word in class_set:
                return class_name
        return None

    def mapClass(self, tokens):
        result = list(tokens)
        for idx in range(0, len(tokens)):
            token = result[idx]
            word = token[0]
            special_class = self.evaluateClass(word)
            if special_class:
                token_list = list(token)
                token_list[1] = special_class
                token_new = tuple(token_list)
                result[idx] = token_new
        return result

    def cleanNoWords(self, text):
        return re.sub(r'\b\d+\b', ' ', text)

    def tokenize(self, text):
      return [t for t in re.split(self.split_regex, text.lower()) if len(t) > 1 or t in ['a','e','o']]

    def tag(self, words):
      return self.model.tag(words)

    def markWindowed(self, x):
      aux = [0] * len(x)
      classes = self.classes.keys()
      if (len(x) > 6):
          r_init = 7
          aux[0] = 0
          aux[1] = 0
          aux[2] = 0
          aux[3] = 0
          aux[4] = 0
          aux[5] = 0
          aux[6] = 0
      else:
          r_init = 0
      for idx in range(r_init,len(x)-6):
        if (x[idx][1]=='None' or x[idx][1] in classes or x[idx][1]=='X') and \
           (x[idx+1][1]=='None' or x[idx+1][1] in classes or x[idx+1][1]=='X') and \
           (x[idx+2][1]=='None' or x[idx+2][1] in classes or x[idx+2][1]=='X') and \
           (x[idx+3][1]=='None' or x[idx+3][1] in classes or x[idx+3][1]=='X') and \
           (x[idx+4][1]=='None' or x[idx+4][1] in classes or x[idx+4][1]=='X') and \
           (x[idx+5][1]=='None' or x[idx+5][1] in classes or x[idx+5][1]=='X') and \
           (x[idx+6][1]=='None' or x[idx+6][1] in classes or x[idx+6][1]=='X'):
          aux[idx]   = 1
          aux[idx+1] = 1
          aux[idx+2] = 1
          aux[idx+3] = 1
          aux[idx+4] = 1
          aux[idx+5] = 1
          aux[idx+6] = 1
      for idx, val in enumerate(x):
          x[idx] += (str(aux[idx]), )
      return x

    def filterBodyDel(self, marks):
      return [t[0] for t in marks if t[2]=='0']

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
        return self.filterBodyDel(marks)

    def cleanBody(self, body):
        body_cleaned = self.cleanNoWords(body)
        tokens = self.tokenize(body_cleaned)

        tags = self.tag(tokens)
        tags_class_mapped = self.mapClass(tags)
        marks = self.markWindowed(tags)

        tokens_cleaned = self.filterMarks(marks)

        return " ".join(tokens_cleaned)
