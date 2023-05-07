import os, django
import sys
path = os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weibo.settings")  # project_name 项目名称
django.setup()

from django.db.models import Q
from keshihua import models
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random
import re
import traceback
import copy

wd = webdriver.Chrome(os.getcwd() + '\chromedriver.exe')
wd.maximize_window()
wd.implicitly_wait(20)
with open(os.path.dirname(os.path.abspath(__file__)) + r'\stealth.min.js') as f:
    js = f.read()

wd.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": js
})

def get_pageurl(url, count,name):
    wd.get(url)
    for i in range(count):
        time.sleep(random.uniform(3.5, 5.5))
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    soup = BeautifulSoup(wd.page_source,'html.parser')
    divs = soup.select('div.vue-recycle-scroller__item-view')
    for row in divs:
        try:
            content = row.select('div.detail_wbtext_4CRf9')[0].text.strip()
            shijian = row.select('a.head-info_time_6sFQg')[0].attrs.get('title')
            zhuanfa = row.select('span.toolbar_num_JXZul')[0].text.strip()
            if '万' in zhuanfa:
                zhuanfa = str(zhuanfa).replace('万','')
                try:
                    zhuanfa = float(zhuanfa.strip()) * 10000
                except:
                    zhuanfa = 10000
            else:
                try:
                    zhuanfa = float(zhuanfa.strip()) * 10000
                except:
                    zhuanfa = 10000
            pingluns = row.select('span.toolbar_num_JXZul')[1].text.strip()
            if '万' in pingluns:
                pingluns = str(pingluns).replace('万','')
                try:
                    pingluns = float(pingluns.strip()) * 10000
                except:
                    pingluns = 10000
            else:
                pingluns = str(pingluns).replace('万', '')
                try:
                    pingluns = float(pingluns.strip()) * 10000
                except:
                    pingluns = 10000
            dianzhan = row.select('span.woo-like-count')[0].text.strip()
            if '万' in dianzhan:
                dianzhan = str(dianzhan).replace('万','')
                try:
                    dianzhan = float(dianzhan.strip()) * 10000
                except:
                    dianzhan = 10000
            else:
                try:
                    dianzhan = float(dianzhan.strip()) * 10000
                except:
                    dianzhan = 10000
            url = row.select('a.head-info_time_6sFQg')[0].attrs.get('href')
            print(shijian,zhuanfa,pingluns,dianzhan,content,url)
        except:
            print(traceback.format_exc())
            continue
        if not models.Case_item.objects.filter(url=url).all():
            models.Case_item.objects.create(
                fabushijian = datetime.datetime.strptime(shijian, '%Y-%m-%d %H:%M'),
                fabu_name = name,
                content = content,
                zhuanfa = zhuanfa,
                pingluns = pingluns,
                dianzan = dianzhan,
                url=url
            )
    print(len(divs))
    time.sleep(100)

if __name__ == '__main__':
    try:
        topic_xinxis = [('新闻晨报','https://weibo.com/shmorningpost?refer_flag=1028035010_'),
                        ("四川日报",'https://weibo.com/u/3167104922?refer_flag=1028035010_')
                        ]

        wd.get('https://weibo.com/?topnav=1&mod=logo')
        time.sleep(2)
        input('手动登录然后点击开始爬取数据:')
        for datas1 in topic_xinxis:
            data = datas1[-1]
            name = datas1[0]
            get_pageurl(data, 3,name)
            # time.sleep(random.randint(0, 3))  # 暂停0~3秒的整数秒，时间区间：[0,3

    except Exception as e:
        print(traceback.format_exc())
        time.sleep(100)

    finally:
        wd.close()


