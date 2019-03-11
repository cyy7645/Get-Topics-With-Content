#-*- coding:utf-8 -*-
# author:cyy7645
# datetime:2019-02-09 13:36
# software: PyCharm


from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, RegexpTokenizer
import requests
from nltk.stem import PorterStemmer, WordNetLemmatizer
import multiprocessing as mp
import time
import ssl

# 打开指定url，获取该网页下的所有url
def getUrls(url, opener):
    html = opener.open(url)
    soup = BeautifulSoup(html, features='lxml')
    # Extracting all the <a> tags into a list.
    tags = soup.find_all('a')

    urls = [base_url]
    # Extracting URLs from the attribute href in the <a> tags.
    for tag in tags:
        url = tag.get('href')
        if isinstance(url, str) and len(url) > 11 and (url[:11] == "https://www" or url[:11] == "http://www."):
            urls.append(url)
    return urls


# given a url, output cleaned tokens
# 获得指定
def cleanHTMLContent(url):
    print("start clean HTML ", url)
    html = opener.open(url)
    soup = BeautifulSoup(html, features='lxml')
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    # get text with lots of space (try to remove it later!)
    text = soup.get_text()

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
    # print (tokens)

    # print("start filtering numbers")
    # # 过滤数字
    # i = 0
    # while i < len(tokens):
    #     if tokens[i].isdigit():
    #         tokens.remove(tokens[i])
    #     else:
    #         i += 1
    # print("finish filtering numbers")

    # remove stopwords
    clean_tokens = list()
    sr = stopwords.words('english')
    for token in tokens:
        if token not in sr:
            clean_tokens.append(token)

    print("finish clean HTML ", url)
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
base_url = "https://www.google.com/"
urls = getUrls(base_url, opener)

# 使用多进程获得该url下所有二级url的token
pool = mp.Pool(8)
clean_tokens = []
crawl_jobs = [pool.apply_async(cleanHTMLContent, args=(url,)) for url in urls]
for j in crawl_jobs:
    clean_tokens += j.get()

print("start get bigrams....")
bigrams, trigrams = getBigramsTrigrams(clean_tokens)

# 连接 token bigrams trigrams
clean_tokens += bigrams + trigrams
# get frequency of words
# freq = nltk.FreqDist(clean_tokens)
mostCommon = getMostFreqTokens(clean_tokens)
results = combineWords(mostCommon)
print(results)

# freq.plot(20, cumulative=False)
endTime = time.time()
print(endTime - startTime,"s")




