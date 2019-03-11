#-*- coding:utf-8 -*-
# author:cyy7645
# datetime:2019-02-10 11:51
# software: PyCharm
from bs4 import BeautifulSoup

from Classes import Connection

class URLs:
    def __init__(self):
        # defalut test urls
        self.TestURL1 = "https://www.rei.com/blog/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors#_blank"
        self.TestURL2 = "https://www.cnn.com/2013/06/10/politics/edward-snowden-profile/#_blank"
        self.TestURL3 = "https://www.amazon.com/Cuisinart-CPT-122-Compact-2-SliceToaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster#_blank"
        self.TestURL4 = "http://www.runoob.com/python/python-exceptions.html"
        # self.connect = Connection.Connection()
        # self.opener = self.connect.fakeAgent()

    # get all valid urls in a given url
    def getUrls(self, baseUrl, opener):
        html = opener.open(baseUrl)
        soup = BeautifulSoup(html, features='lxml')
        # Extracting all the <a> tags into a list.
        tags = soup.find_all('a')

        urls = [baseUrl]
        # Extracting URLs from the attribute href in the <a> tags.
        for tag in tags:
            url = tag.get('href')
            if isinstance(url, str) and len(url) > 11 and (url[:11] == "https://www" or url[:11] == "http://www."):
                urls.append(url)
        return urls
