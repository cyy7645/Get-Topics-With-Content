#-*- coding:utf-8 -*-
# author:cyy7645
# datetime:2019-02-10 12:49
# software: PyCharm
import jieba
import nltk
import jieba.analyse

class GetTopics:

    # Get the 5 most frequent words
    def getMostFreqTokens(self,clean_tokens):
        freq = nltk.FreqDist(clean_tokens)
        mostCommon = freq.most_common(5)
        # for k, v in mostCommon:
        #     print(k, ': ', v)
        return mostCommon

    # same words may have different forms, we only keep the most appropriate one,
    # e.g. toaster:30 Toaster:45, we keep Toaster, discard toaster
    def combineWords(self, mostCommon):
        dict = {}
        for token, count in mostCommon:
            if token.lower() not in dict:
                dict[token.lower()] = [(token, count)]
            else:
                dict[token.lower()].append((token, count))
        topics = []
        for token, list in dict.items():
            if len(list) == 1:
                topics.append(list[0][0])
            else:
                res = list[0][0]
                c = list[0][1]
                for pair in list[1:]:
                    if pair[1] > c:
                        res = pair[0]
                topics.append(res)
        return topics

    def extract_keywords(self, clean_tokens, topK=5, withWeight=True, allowPOS=()):
        keywords = jieba.analyse.extract_tags(clean_tokens, topK=5, withWeight=True, allowPOS=())
        items = []
        weights = []
        for item in keywords:
            # Get the 5 most frequent words with weights
            items.append(item[0])
            weights.append(item[1])

        return items, weights