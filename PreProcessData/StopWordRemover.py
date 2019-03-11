# -*- coding:utf-8 -*-
# author:cyy7645
# datetime:2019-02-10 12:08
# software: PyCharm

from Classes.Constants import ChineseStopwordPath
from nltk.corpus import stopwords

class StopWordRemover:
    def __init__(self):
        self.stop_filepath = ChineseStopwordPath
        self.stopwords = [line.strip() for line in
                 open(self.stop_filepath, 'r', encoding='utf-8').readlines()]

    # clean stopwords for Chinese context
    def clearChineseStopwords(self, splitedContent):
        article = ' '.join(word for word in splitedContent if word not in self.stopwords)
        return article

    # # clean stopwords for English context
    def clearStopwords(self, tokens):
        # remove stopwords
        clean_tokens = list()
        sr = stopwords.words('english')
        for token in tokens:
            if token not in sr:
                clean_tokens.append(token)
        return clean_tokens

