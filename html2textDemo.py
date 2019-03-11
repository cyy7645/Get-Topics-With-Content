#-*- coding:utf-8 -*-
# author:cyy7645
# datetime:2019-02-09 10:40
# software: PyCharm

import html2text
import requests

def to_text(html, rehtml=False):
    parser = html2text.HTML2Text()
    parser.wrap_links = False
    parser.skip_internal_links = True
    parser.inline_links = True
    parser.ignore_anchors = True
    parser.ignore_images = True
    parser.ignore_emphasis = True
    parser.ignore_links = True
    text = parser.handle(html)
    text = text.strip(' \t\n\r')
    if rehtml:
        text = text.replace('\n', '<br/>')
        text = text.replace('\\', '')
    return text

text = to_text("https://www.rei.com/blog/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors#_blank")
print(text)