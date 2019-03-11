#-*- coding:utf-8 -*-
# author:cyy7645
# datetime:2019-02-10 12:09
# software: PyCharm
from nltk import WordNetLemmatizer


class WordLemmatizer:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    # word Lemmatization
    def wordLemmatizer(self, tokens):
        for i in range(len(tokens)):
            tokens[i] = self.lemmatizer.lemmatize(tokens[i])
        tokensNoNumbers = self.removeNumbers(tokens)
        return tokensNoNumbers

    def removeNumbers(self, tokens):
        # remove numbers
        tokensNoNumbers = [x for x in tokens if not (x.isdigit()
                                            or x[0] == '-' and x[1:].isdigit())]
        return tokensNoNumbers