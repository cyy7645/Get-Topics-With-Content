#-*- coding:utf-8 -*-
# author:cyy7645
# datetime:2019-02-09 10:47
# software: PyCharm

from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
import re
import nltk
import time
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer, sent_tokenize
import requests
from nltk.stem import PorterStemmer, WordNetLemmatizer
from langdetect import detect
import jieba
import ssl

# given a url, output cleaned tokens
# 获得指定
def cleanHTMLContent(url):
    html = opener.open(url)
    soup = BeautifulSoup(html, features='lxml')
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    # get text with lots of space (try to remove it later!)
    text = soup.get_text()

    # 对使用语言进行判断，根据lang 或者title的语言
    splitRequired = False
    html = soup.find('html')
    language = html['lang']
    print(language)
    if 'zh' in language:
        splitRequired = True
    title = soup.find('title')
    title = str(title)
    if len(title) > 14:
        title = title[7:-8]
        lang = detect(title)
        if 'zh' in lang:
            splitRequired = True
    if splitRequired == False:
        # break into lines and remove leading and trailing space on each (with multiple blank lines now)
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # remove blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # tokens = word_tokenize(text)

        # remove punctuation and other special character
        tokenizer = RegexpTokenizer(r'[0-9a-zA-Z\-]+')
        tokens = tokenizer.tokenize(text)
        print(tokens)

        # apply lemmatization (group together the inflected forms of a word)
        lemmatizer = WordNetLemmatizer()
        for i in range(len(tokens)):
            tokens[i] = lemmatizer.lemmatize(tokens[i])

        # 移除数字
        tokens = [x for x in tokens if not (x.isdigit()
                                                 or x[0] == '-' and x[1:].isdigit())]

        # remove stopwords
        clean_tokens = list()
        sr = stopwords.words('english')
        for token in tokens:
            if token not in sr:
                clean_tokens.append(token)
        return clean_tokens




# 获得2-grams 和 3-grams
def getBigramsTrigrams(tokens):
    my_bigrams = list(nltk.bigrams(tokens))
    my_trigrams = list(nltk.trigrams(tokens))
    bigrams = []
    for grams in my_bigrams:
        bigrams.append(grams[0] + ' ' + grams[1])
    trigrams = []
    for grams in my_trigrams:
        trigrams.append(grams[0] + ' ' + grams[1] + ' ' + grams[2])
    return bigrams, trigrams

def getMostFreqTokens(clean_tokens):
    freq = nltk.FreqDist(clean_tokens)
    # print(freq)
    mostCommon = freq.most_common(10)
    for k, v in mostCommon:
        print(k,': ', v)
    return mostCommon

def combineWords(mostCommon):
    dict = {}
    for token, count in mostCommon:
        if token.lower() not in dict:
            dict[token.lower()] = [(token, count)]
        else:
            dict[token.lower()].append((token, count))
    results = []
    for token, list in dict.items():
        if len(list) == 1:
            results.append(list[0][0])
        else:
            res = list[0][0]
            c = list[0][1]
            for pair in list[1:]:
                if pair[1] > c:
                    res = pair[0]
            results.append(res)
    return results

startTime = time.time()
# solve "SSL: CERTIFICATE_VERIFY_FAILED"
ssl._create_default_https_context = ssl._create_unverified_context

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
base_url = "https://blog.csdn.net/willib/article/details/52246086"
clean_tokens = cleanHTMLContent(base_url)
bigrams, trigrams = getBigramsTrigrams(clean_tokens)
clean_tokens += bigrams
clean_tokens += trigrams
mostCommon = getMostFreqTokens(clean_tokens)
results = combineWords(mostCommon)
print(results)

