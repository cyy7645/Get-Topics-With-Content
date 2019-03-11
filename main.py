#-*- coding:utf-8 -*-
# author:cyy7645
# datetime:2019-02-10 12:50
# software: PyCharm
import time

from Classes import Connection, URLs, GetTopics, BiTriGramsCombine
from PreProcessData import Split, WordTokenizer, WordLemmatizer, StopWordRemover, Tokens
import sys

class GetTopicsMain:

    def __init__(self):
        #  for running on command, receive parameters from command
        # input = sys.argv
        # try:
        #     self.url = input[1]
        # except IndexError:
        #     print("You didn't given an url, use default url now...")
        #     self.urlsObj = URLs.URLs()
        #     self.url = self.urlsObj.TestURL3

        # get the data from database
        self.tokens = Tokens.Tokens()
        self.splitRequired = False
        self.connectObj = Connection.Connection()
        self.splitObj = Split.Split()
        self.WordTokenizerObj = WordTokenizer.WordTokenizer()
        self.StopWordRemoverObj = StopWordRemover.StopWordRemover()
        self.biTriGramsCombineObj = BiTriGramsCombine.BiTriGramsCombine()
        self.GetTopicsObj = GetTopics.GetTopics()

    # print result in following form
    def printTopics(self, topics):
        length = len(topics[0])
        print(length, " common topics that best describe the contents:")
        for i in range(length):
            print("topic ", topics[0][i], ": ", topics[1][i])

    def main(self):
        startTime = time.time()

        # opener = self.connectObj.fakeAgent()
        # base_url = self.url
        # soup = self.splitObj.connectURL(base_url, opener)

        # callback get_data to get the data dict
        self.connObj = Connection.Connection()
        self.data = self.connObj.get_data()

        # enumerate every record
        for key, value in self.data.items():
            # text: only content of articles
            self.splitRequired, text = self.splitObj.checkSplit(value['content'])
            # concatenate content with title and tags
            allContent = value['title'] + ' ' + value['tags'] + ' ' + text

            # if it's a English article, we don't need to split
            if self.splitRequired == False:
                text = self.WordTokenizerObj.removeSpace(allContent)
                tokens = self.WordTokenizerObj.wordTokenizer(text)
                WordLemmatizerObj = WordLemmatizer.WordLemmatizer()
                tokensNoNumbers = WordLemmatizerObj.wordLemmatizer(tokens)
                clean_tokens = self.StopWordRemoverObj.clearStopwords(tokensNoNumbers)
                bigrams, trigrams = self.biTriGramsCombineObj.getBigramsTrigrams(clean_tokens)
                clean_tokens += bigrams
                clean_tokens += trigrams
                mostCommon = self.GetTopicsObj.getMostFreqTokens(clean_tokens)
                topics = self.GetTopicsObj.combineWords(mostCommon)
                self.printTopics(topics)

                keywords = ','.join(topics[0])
                self.connectObj.insert_data(keywords, key)

            # otherwise, split is required
            else:
                textNoSpace = self.WordTokenizerObj.removeSpace(allContent)
                contentOnlyChinese = self.WordTokenizerObj.extractChinese(textNoSpace)
                splitedContent = self.splitObj.splitChinese(contentOnlyChinese)
                clean_tokens = self.StopWordRemoverObj.clearChineseStopwords(splitedContent)
                topics = self.GetTopicsObj.extract_keywords(clean_tokens)
                keywords = ','.join(topics[0])
                self.printTopics(topics)
                # callback insert sql method
                self.connectObj.insert_data(keywords, key)
        endTime = time.time()
        print("It takes a total of ", endTime - startTime, "s")

if __name__ == '__main__':
    test = GetTopicsMain()
    test.main()