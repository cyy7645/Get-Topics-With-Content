#-*- coding:utf-8 -*-
# author:cyy7645
# datetime:2019-02-10 12:47
# software: PyCharm
import nltk

# Given cleared tokens, generate bigrams and trigrams
class BiTriGramsCombine:

    def getBigramsTrigrams(self,tokens):

        my_bigrams = list(nltk.bigrams(tokens))
        my_trigrams = list(nltk.trigrams(tokens))
        bigrams = []
        for grams in my_bigrams:
            bigrams.append(grams[0] + ' ' + grams[1])
        trigrams = []
        for grams in my_trigrams:
            trigrams.append(grams[0] + ' ' + grams[1] + ' ' + grams[2])

        return bigrams, trigrams