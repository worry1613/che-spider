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

# import HTMLParser
import execjs
from bs4 import BeautifulSoup
from scrapy.spiders import Spider
from lxml import etree

import scrapy_redis_bloomfilter

# from csdn_spider.settings import BLOGKEY, USERKEY, BLOGKEYOK, REDIS_HOST, REDIS_PORT, REDIS_DB, BLOGFILE_DIR
# from csdn_spider.items import CsdnSpiderItem
from scrapy_redis_bloomfilter.spiders import RedisSpider

from che.items import CheArticleItem
from che.settings import ARTICLES

CATE='汽车'

class ArticleSpider(Spider):
# class ArticleSpider(RedisSpider):
    name = "arts"
    # allowed_domains = ["blog.csdn.net"]
    redis_key = ARTICLES
    f = open('che/spiders/articles.txt')
    start_urls= [l.strip() for l in f.readlines()]
    f.close()
    # start_urls = [
    #     'https://www.toutiao.com/i6624831806317264903/',

        # 'https://www.toutiao.com/i6650811291646558724/',
    # 'https://www.toutiao.com/i6651154848983092493/',

                  # 'https://www.toutiao.com/i6650812054758228494/',
                  # 'https://www.toutiao.com/i6651170050243822087/',
                  # 'https://www.toutiao.com/i6651346628642917635/',
                  # 'https://www.toutiao.com/i6651469913749717515/',

                  # 'https://www.toutiao.com/i6651519634379899399/',
    #               'https://www.toutiao.com/item/6694322397580886532/',
    #               'https://www.toutiao.com/item/6695830023934312963/',
    #               'https://www.toutiao.com/item/6696902078956044811/',
    #               'https://www.toutiao.com/item/6701582615205380107/',
    #               'https://www.toutiao.com/item/6703103984862756876/',
    #               'https://www.toutiao.com/item/6705089602669003277/',
    #               'https://www.toutiao.com/item/6712845808070296078/',
    #               'https://www.toutiao.com/item/6716099962297385484/',
    #               'https://www.toutiao.com/item/6726173343126389256/',
    #               'https://www.toutiao.com/item/6729076107489837575/',
    #               ]

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(ArticleSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # 处理博客内容
        logging.info(response.url)
        if 'toutiao.com' not in response.url: return

        data = response.body
        soup = BeautifulSoup(data, "html5lib")

        text = soup.text
        # chineseTag: '汽车',
        # con = re.compile(r'articleInfo:((?:.|\n)*?)\,\n\s+commentInfo')
        con = re.compile(r'chineseTag:\s\'([\u4e00-\u9fa5]+)\'\,')
        # self.log(text,level=logging.DEBUG)
        try:
            cate = con.findall(text)[0]
        except Exception as e :
            f = open('bad.txt','a')
            f.write(response.url+'\n')
            f.close()
            self.log('%s ---- [[%s]]' %(response.url,text),level=logging.ERROR)
            return
        if '404' in soup.title.text or cate not in CATE:
            return

        # art = CheArticleItem()
        # if not soup.h1: return
        # art['_title'] = soup.h1.text
        # art['_content'] =soup.find(class_="article-content").div
        # art['_text'] =art['_content'].text
        # art['_id']= response.url.split('/')[-2][1:]
        # art['_datetime'] = soup.findAll(class_='article-sub')[0].contents[-1].text
        # art['_keywords'] = '|+|'.join([tag.text for tag in  soup.findAll('li',{'class':['tag-item']})])
        # yield art


        con = re.compile(r'articleInfo:((?:.|\n)*?)\,\n\s+commentInfo')
        text = html.unescape(con.findall(text)[0])\
            .replace('\'"','"').replace('"\'','"').replace('\'','"')\
            .replace('.slice(6, -6)','') \
            .replace('\n', '')
            # .replace('  ',' ')



        art = CheArticleItem()
        con = re.compile(r'\s+title:\s\"(.*)\"\,\s+content:\s\"(.*)\"\,\s+groupId')
        art['_title'],art['_content'] =con.findall(text)[0]
        con = re.compile(r'(\\u[0-9a-fA-F]{4})')
        art["_content"] = re.sub(r'(\\u[0-9a-fA-F]{4})',
                                  lambda matched: matched.group(1).encode('utf-8').decode('unicode_escape'),
                          art["_content"])
        con = re.compile(r'\sitemId:\s\"(\d+)\"\,')
        art['_id']= con.findall(text)[0]
        con = re.compile(r'\s+time:\s\"(.*)\"\s+\}\,\s+tagInfo:')
        art['_datetime'] = con.findall(text)[0]
        con = re.compile(r'\"name\":\"([\u4e00-\u9fa5]+)\"')
        art['_keywords'] = con.findall(text)
        art['_text'] = BeautifulSoup(art['_content'], 'html5lib').text.strip()
        yield art
