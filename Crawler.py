#-*- coding:utf-8 -*-
# author:cyy7645
# datetime:2019-02-09 00:59
# software: PyCharm

from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
html = opener.open("https://www.amazon.com/Cuisinart-CPT-122-Compact-2-SliceToaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster")
# html=urlopen("https://www.amazon.com/Cuisinart-CPT-122-Compact-2-SliceToaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster").read().decode('utf-8')

soup = BeautifulSoup(html, features='lxml')

# html = requests.get("https://www.amazon.com/Cuisinart-CPT-122-Compact-2-SliceToaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster")
# soup = BeautifulSoup(html, features='lxml')

# print(soup.h1)
# all_href = soup.find_all('a')
# all_href = [l['href'] for l in all_href]
# print('\n', all_href)

# content = soup.find_all('h1', {"class": "entry-title cb-entry-title cb-title"})
# print(content)

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

# text = soup.get_text(strip=True)
tokens = word_tokenize(text)
# tokens = text.split()
print (tokens)

clean_tokens = list()
sr = stopwords.words('english')
for token in tokens:
    if token not in sr:
        clean_tokens.append(token)

freq = nltk.FreqDist(clean_tokens)
for key,val in freq.items():
    print (str(key) + ':' + str(val))

freq.plot(20, cumulative=False)
