#-*- coding:utf-8 -*-
# author:cyy7645
# datetime:2019-02-10 12:09
# software: PyCharm
from nltk import RegexpTokenizer


class WordTokenizer:

    def __init__(self):
        # remove punctuation and other special character
        self.tokenizer = RegexpTokenizer(r'[0-9a-zA-Z\-]+')

    # remove extra spaces
    def removeSpace(self, text):
        # break into lines and remove leading and trailing space on each (with multiple blank lines now)
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # remove blank lines
        textNoSpace = '\n'.join(chunk for chunk in chunks if chunk)
        return textNoSpace

    # word Tokenization
    def wordTokenizer(self, text):
        # tokens = word_tokenize(text)

        tokens = self.tokenizer.tokenize(text)
        return tokens

    # whether is Chinese word
    def isChinese(self, uchar):
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True
        else:
            return False

    # extract Chinese content
    def extractChinese(self, content):
        contentOnlyChinese = ''
        for i in content:
            if self.isChinese(i):
                contentOnlyChinese = contentOnlyChinese + i
        return contentOnlyChinese