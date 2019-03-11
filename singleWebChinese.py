#-*- coding:utf-8 -*-
# author:cyy7645
# datetime:2019-02-09 23:06
# software: PyCharm

from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
import jieba
import jieba.analyse
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
base_url = "http://www.runoob.com/python/python-exceptions.html"
html = opener.open(base_url)
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

# print(text)
def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

def format_str(content):
    content_str = ''
    for i in content:
        if is_chinese(i):
            content_str = content_str + i
    return content_str

# chinese_list = []
# for line in text:
#     chinese_list.append(format_str(line))
# print(chinese_list)

content_str = format_str(text)
# print(content_str)

splitedContent = list(jieba.cut(content_str))


def load_stopwords(stop_filepath):
    stopwords = [line.strip() for line in
                 open(stop_filepath, 'r', encoding='utf-8').readlines()]

    return stopwords

stop_filepath = "/Users/cyy7645/Documents/intern/article_recommendation_system/chinese_stop_words.txt"
stopwords = load_stopwords(stop_filepath)


def clear_stopwords(splitedContent, stopwords):
    article = ' '.join(word for word in splitedContent if word not in stopwords)
    return article

article = clear_stopwords(splitedContent, stopwords)


def extract_keywords(article, topK=20, withWeight=True, allowPOS=()):
    keywords = jieba.analyse.extract_tags(article, topK=20, withWeight=True, allowPOS=())
    items = []
    weights = []
    for item in keywords:
        # 分别为关键词和相应的权重
        items.append(item[0])
        weights.append(item[1])

    return items, weights

items, weights = extract_keywords(article)

print(items)

# text=nltk.text.Text(jieba.lcut(text))
#
# print(text)