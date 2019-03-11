#-*- coding:utf-8 -*-
# author:cyy7645
# datetime:2019-02-10 11:59
# software: PyCharm
import jieba
from bs4 import BeautifulSoup
from textblob import TextBlob
from Classes import Connection
import re

class Split:
    def __init__(self):
        self.splitRequired = False

    # # connect to the given url
    # def connectURL(self, url, opener):
    #     html = opener.open(url)
    #     soup = BeautifulSoup(html, features='lxml')
    #     return soup

    # check whether the context is needed to be split according to the languagge
    def checkSplit(self, text):


        regex_str = "<[^>]+>"
        matchObj = re.sub(regex_str, '', text)
        return True, matchObj



        # # kill all script and style elements
        # for script in soup(["script", "style"]):
        #     script.extract()
        # # get text with lots of space (try to remove it later!)
        # text = soup.get_text()
        # html = soup.find('html')
        # try:
        #     language = html['lang']
        #     # Chinese is needed to be split
        #     if 'zh' in language:
        #         self.splitRequired = True
        # except KeyError:
        #     print("HTML doesn't contain lang tag. The program continues to execute..")
        # title = soup.find('title')
        # title = str(title)
        # if len(title) > 14:
        #     title = title[7:-8]
        #     b = TextBlob(title)
        #     lang = b.detect_language()
        #     # Chinese is needed to be split
        #     if 'zh' in lang:
        #         self.splitRequired = True
        # return self.splitRequired, text

    def splitChinese(self, text):
        splitedContent = list(jieba.cut(text))
        return splitedContent