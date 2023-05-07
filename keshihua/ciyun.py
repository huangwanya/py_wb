import os, django
import sys
path = os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(path)
# print(sys.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weibo.settings")  # project_name 项目名称
django.setup()

from django.db.models import Q
from keshihua import models

from wordcloud import WordCloud
import jieba,os
import PIL.Image as image
import numpy as np

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords
root_path = os.path.dirname(os.path.abspath(__file__))
stopwords = stopwordslist(root_path + os.sep + 'stopwords.txt')

def chinese_jieba(text):
    wordlist_jieba = jieba.cut(text)
    space_wordlist = ' '.join([i for i in wordlist_jieba if i not in stopwords])
    return space_wordlist



mask = np.array(image.open("11.jpg"))

datas1 = models.Case_item.objects.all()
strs = ' '
for data1 in datas1:
    strs += data1.content
text = chinese_jieba(strs)
font_path = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))) + os.sep + 'data' + os.sep + 'simfang.ttf'
wordcloud = WordCloud(font_path=font_path,mask=mask,
                      background_color=None, mode="RGBA", width=800,
                      height=400, max_words=50, min_font_size=8).generate(text)
image = wordcloud.to_image()
path = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))) + os.sep + 'static' + os.sep + 'ciyuntu' + os.sep + '{}.png'.format(1)
image.save(path)

