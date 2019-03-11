#-*- coding:utf-8 -*-
# author:cyy7645
# datetime:2019-02-10 14:52
# software: PyCharm
from Classes import Connection, URLs, GetTopics, BiTriGramsCombine
from PreProcessData import Split, WordTokenizer, WordLemmatizer, StopWordRemover
import multiprocessing as mp

# add muti-processess function for mutl-urls,
# not be used now
class Tokens:

    def __init__(self):
        self.URLsObj = URLs.URLs()
        self.splitRequired = False
        self.connectObj = Connection.Connection()
        # self.urlsObj = URLs.URLs()
        self.splitObj = Split.Split()
        self.WordTokenizerObj = WordTokenizer.WordTokenizer()
        self.StopWordRemoverObj = StopWordRemover.StopWordRemover()
        self.biTriGramsCombineObj = BiTriGramsCombine.BiTriGramsCombine()
        self.GetTopicsObj = GetTopics.GetTopics()

    # get cleaned tokens with the given url
    def getCleanedTokens(self, url):
        opener = self.connectObj.fakeAgent()

        # base_url = self.urlsObj.TestURL4
        # base_url = self.url

        soup = self.splitObj.connectURL(url, opener)

        self.splitRequired, text = self.splitObj.checkSplit(soup)
        # print("splitRequired: ",self.splitRequired)

        if self.splitRequired == False:
            print("sentences split isn't required.")
            text = self.WordTokenizerObj.removeSpace(text)
            tokens = self.WordTokenizerObj.wordTokenizer(text)
            WordLemmatizerObj = WordLemmatizer.WordLemmatizer()
            tokensNoNumbers = WordLemmatizerObj.wordLemmatizer(tokens)
            clean_tokens = self.StopWordRemoverObj.clearStopwords(tokensNoNumbers)

        else:
            textNoSpace = self.WordTokenizerObj.removeSpace(text)
            contentOnlyChinese = self.WordTokenizerObj.extractChinese(textNoSpace)
            splitedContent = self.splitObj.splitChinese(contentOnlyChinese)
            clean_tokens = self.StopWordRemoverObj.clearChineseStopwords(splitedContent)
        return clean_tokens, self.splitRequired

    # get cleaned tokens with the given url and the urls in the given url by muti-processes
    def getCleanedTokensMutiProcess(self, url):
        opener = self.connectObj.fakeAgent()
        urls = self.URLsObj.getUrls(url, opener)

        # create processes pool
        pool = mp.Pool(8)
        clean_tokens = []
        crawl_jobs = [pool.apply_async(self.getCleanedTokens, args=(url,)) for url in urls]
        for j in crawl_jobs:
            clean_tokens += j.get()
        return clean_tokens, self.splitRequired

