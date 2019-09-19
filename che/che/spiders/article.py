# -*- coding: utf-8 -*-
# @创建时间 : 8/12/2018 
# @作者    : worry1613(549145583@qq.com)
# GitHub  : https://github.com/worry1613
# @CSDN   : http://blog.csdn.net/worryabout/

import datetime
import logging
import time
import re
import html
import json

from bs4 import BeautifulSoup
from scrapy.spiders import Spider


# from csdn_spider.settings import BLOGKEY, USERKEY, BLOGKEYOK, REDIS_HOST, REDIS_PORT, REDIS_DB, BLOGFILE_DIR
# from csdn_spider.items import CsdnSpiderItem
from che.items import CheArticleItem


class ArticleSpider(Spider):
    # class ArticleSpider(RedisSpider):
    name = "arts"
    # allowed_domains = ["blog.csdn.net"]
    # redis_key = BLOGKEY
    start_urls = [
    'https://www.toutiao.com/item/6690254170995294732/',
                  'https://www.toutiao.com/item/6690891251891307011/',
                  'https://www.toutiao.com/item/6692106673466638862/',
                  'https://www.toutiao.com/item/6693087483615248899/',
                  'https://www.toutiao.com/item/6693092734288265736/',
        'https://www.toutiao.com/item/6723146523133083652/','https://www.toutiao.com/item/6723146523133083652/','https://www.toutiao.com/item/6723146523133083652/','https://www.toutiao.com/item/6723146523133083652/','https://www.toutiao.com/item/6723146523133083652/','https://www.toutiao.com/item/6723146523133083652/','https://www.toutiao.com/item/6723146523133083652/','https://www.toutiao.com/item/6723146523133083652/',
                  'https://www.toutiao.com/item/6693566431528747534/',
                  'https://www.toutiao.com/item/6694322397580886532/',
                  'https://www.toutiao.com/item/6695830023934312963/',
                  'https://www.toutiao.com/item/6696902078956044811/',
                  'https://www.toutiao.com/item/6701582615205380107/',
                  'https://www.toutiao.com/item/6703103984862756876/',
                  'https://www.toutiao.com/item/6705089602669003277/',
                  'https://www.toutiao.com/item/6712845808070296078/',
                  'https://www.toutiao.com/item/6716099962297385484/',
                  'https://www.toutiao.com/item/6726173343126389256/',
                  'https://www.toutiao.com/item/6729076107489837575/',
        'https://www.toutiao.com/item/6723146523133083652/',
        'https://www.toutiao.com/item/6723146523133083652/','https://www.toutiao.com/item/6723146523133083652/',
        'https://www.toutiao.com/item/6723146523133083652/','https://www.toutiao.com/item/6723146523133083652/',
        'https://www.toutiao.com/item/6723146523133083652/','https://www.toutiao.com/item/6723146523133083652/',
        'https://www.toutiao.com/item/6723146523133083652/','https://www.toutiao.com/item/6723146523133083652/',

                  ]

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(ArticleSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # 处理博客内容
        logging.info(response.url)
        if 'toutiao.com' not in response.url :
            return
        data = response.body
        soup = BeautifulSoup(data, "html5lib")

        text = soup.text
        con = re.compile(r'articleInfo:((?:.|\n)*?)\,\n\s+commentInfo')
        text = html.unescape(con.findall(text)[0])\
            .replace('\'"','"').replace('"\'','"').replace('\'','"')\
            .replace('.slice(6, -6)','') \
            .replace('\n', '')
            # .replace('  ',' ')



        art = CheArticleItem()
        con = re.compile(r'\s+title:\s\"(.*)\"\,\s+content:\s\"(.*)\"\,')
        art['_title'],art['_content'] =con.findall(text)[0]
        con = re.compile(r'\sitemId:\s\"(\d+)\"\,')
        art['_id']= con.findall(text)[0]
        con = re.compile(r'\s+time:\s\"(.*)\"\s+\}\,\s+tagInfo:')
        art['_datetime'] = con.findall(text)[0]
        con = re.compile(r'\"name\":\"([\u4e00-\u9fa5]+)\"')
        art['_keywords'] = con.findall(text)
        art['_text'] = BeautifulSoup(art['_content'], 'html5lib').text.strip()
        yield art



        # text = BeautifulSoup(text,"html5lib").text
        # con = re.compile(r'\,\s+\}')
        # text = con.sub('}', text)
        # con = re.compile(r'\s+([a-zA-Z\_]*:)\s+')
        # for w in con.findall(text):
            # text = con.sub('"'+w[:-1]+'"'+w[-1:],text)
            # text = text.replace(w,'"'+w[:-1]+'"'+w[-1:])
        #
        # fi = open('t1.txt','w')
        # fi.write(text)
        # fi.close()
        # artinfo = json.loads(text)
        #
        # art = CheArticleItem()
        # art['_title'] = artinfo['title']
        # art['_content'] = artinfo['content']
        # art['_text'] = BeautifulSoup(art['_content'],'html5lib').text.strip()
        # art['_id'] = artinfo['itemId']
        # art['_keywords'] = [tag['name'] for tag in artinfo['tagInfo']['tags']]
        # art['_datetime'] = artinfo['subInfo']['time']
        # yield art

        # # 处理用户信息,加到userkey列表中，不做处理在user爬虫中再处理
        # ok = r.keys('csdn:user:%s' % (writer,))
        # if not len(ok):
        #     r.lpush(USERKEY, 'https://blog.csdn.net/%s' % (writer,))
        #     logging.info('user--%s ======' % (writer,))
        #
        # # 处理博客内容下面的推荐列表
        # users = []
        # for u in soup.find_all(class_="recommend-item-box"):  # 博客推荐
        #     if u.find_all('a'):
        #         url = u.find_all('a')[0].get('href')
        #         uid = url.split('/')[3]
        #         _id = url.split('/')[-1]
        #
        #         # 统一去重策略
        #         ok = r.sismember('csdn:user:%s' % (uid,), _id)
        #         uok = r.keys('csdn:user:%s' % (uid,))
        #         if not ok:
        #             p.sadd('csdn:user:%s' % (uid,), _id)
        #             if not len(uok):
        #                 p.lpush(USERKEY, 'https://blog.csdn.net/%s' % (uid,))
        #             p.lpush(BLOGKEY, url)
        #             logging.info('%s ==== %s ' % (url, _id))
        #         else:
        #             logging.info('*********%s ==== %s ********** is ok ' % (url, _id))
        #         p.execute()
