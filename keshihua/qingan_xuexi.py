import os, django
import sys

import pandas

path = os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weibo.settings")  # project_name 项目名称
django.setup()

from django.db.models import Q
from keshihua import models as mb

import nltk
# nltk.download()
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import jieba


# 定义一个用于提取特征的函数
# 输入一段文本返回形如：{'It': True, 'movie': True, 'amazing': True, 'is': True, 'an': True}
# 返回类型是一个dict
def extract_features(word_list):
    return dict([(word, True) for word in word_list])


def stopwordslist():
    stopwords = [line.strip() for line in open('stopwords.txt', 'r', encoding='utf-8').readlines()]
    return stopwords


if __name__ == '__main__':

    # 加载积极与消极和中性评论
    stopwords = stopwordslist()  # 这里加载停用词的路径

    datas = pandas.read_csv('nCoV_100k_train.labled.csv')
    results = datas.values.tolist()
    zhongxing = []
    positive = []
    negative = []
    for resu in results:
        try:
            segtmp = jieba.lcut(resu[3], cut_all=False)  # 把句子进行分词，以列表的形式返回
            outstr = []
            for word in segtmp:
                if word not in stopwords:
                    if word != '\t':
                        if word != ' ' and word != '\n':
                            if resu[-1] == '0':
                                zhongxing.append(word.strip())
                            elif resu[-1] == '1':
                                positive.append(word.strip())
                            elif resu[-1] == '-1':
                                negative.append(word.strip())
        except:
            continue
    zhongxing = list(set(zhongxing))
    positive = list(set(positive))
    negative = list(set(negative))


    # 将这些评论数据分成积极评论和消极评论和中性
    features_positive = []
    for f in positive:
        # print(({f.strip():True}, 'Positive'))
        features_positive.append(({f.strip():True}, 'Positive'))
    features_negative = []
    for f in negative:
        features_negative.append(({f.strip():True}, 'Negative'))
    features_neutral = []
    for f in zhongxing:
        features_neutral.append(({f.strip(): True}, 'Neutral'))



    # 分成训练数据集（80%）和测试数据集（20%）
    threshold_factor = 0.8
    threshold_positive = int(threshold_factor * len(features_positive))  # 800
    threshold_negative = int(threshold_factor * len(features_negative))  # 800
    threshold_neutral = int(threshold_factor * len(features_neutral))  # 800
    # 提取特征 积极文本  消极文本构成训练集
    features_train = features_positive[:threshold_positive] + features_negative[:threshold_negative] + features_neutral[:threshold_neutral]
    features_test = features_positive[threshold_positive:] + features_negative[threshold_negative:] + features_neutral[threshold_neutral:]
    print("\n训练数据点的数量:", len(features_train))
    print("测试数据点的数量:", len(features_test))

    # 训练朴素贝叶斯分类器
    classifier = NaiveBayesClassifier.train(features_train)
    print("\n分类器的准确性:", nltk.classify.util.accuracy(classifier, features_test))


    # 输入一些简单的评论

    datas = mb.Case_item.objects.all()

    # 运行分类器，获得预测结果
    print("\n预测:")
    stopwords = stopwordslist()# 这里加载停用词的路径
    for review1 in datas:
        review = review1.content
        try:
            segtmp = jieba.lcut(review, cut_all=False)#把句子进行分词，以列表的形式返回
            outstr = []
            for word in segtmp:
                if word not in stopwords:
                    if word != '\t':
                        if word != ' ' and word != '\n':
                            outstr.append(word.strip())
            print("\n评论:", review)
            probdist = classifier.prob_classify(extract_features(outstr))
            pred_sentiment = probdist.max()
            # 打印输出
            print("预测情绪:", pred_sentiment)
            print("可能性:", round(probdist.prob(pred_sentiment), 2))
            review1.status = pred_sentiment
            review1.possibility = round(probdist.prob(pred_sentiment), 2)
            review1.save()
        except:
            continue





