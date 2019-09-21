# -*- coding: utf-8 -*-
# @创建时间 : 10/12/2018 
# @作者    : worry1613(549145583@qq.com)
# GitHub  : https://github.com/worry1613
# @CSDN   : http://blog.csdn.net/worryabout/
from bs4 import BeautifulSoup
from scrapy_redis_bloomfilter import bloomfilter
from scrapy_redis_bloomfilter.spiders import RedisSpider
import json
# from scrapy.spiders import Spider
from scrapy.http import Request
import redis
from che.util import get_js,payload_for_get
from settings import USERS,REDIS_HOST,REDIS_PORT,REDIS_DB,ARTICLES

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
rserver = redis.StrictRedis(connection_pool=pool)
p = rserver.pipeline()

bf = bloomfilter.BloomFilter(rserver,key='articles:bloomfilter')


class ArticlesSpider(RedisSpider):
# class ArticlesSpider(Spider):
    name = "userarts"
    redis_key = USERS
    # start_urls = ['http://www.toutiao.com/c/user/token/MS4wLjABAAAAz2T7HE2F-fbTc8WdKw_XLKnMdmzhfEGwuNkwbjluXdI/']

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(ArticlesSpider, self).__init__(*args, **kwargs)

    def parse(self,response):
        """
        不做数据处理，只是找到url，写入redis
        :param response:
        :return:
        """
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        script = soup.find('script', {'type': 'text/javascript'}).get_text()
        start = script.find('id:') + 3
        end = script[start:].find(',')
        userid = script[start:start + end].strip()
        fi = open('data/userids.txt','a')
        fi.write(str(userid)+'\n')
        fi.close()
        Honey = payload_for_get(userid,1,'0')
        _as = Honey['as']
        _cp = Honey['cp']
        _sign = Honey['_signature']
        url = 'https://www.toutiao.com/c/user/article/?page_type=1' \
              '&user_id=%s&max_behot_time=%d&count=20' \
              '&as=%s&cp=%s&_signature=%s' % (userid, 0, _as, _cp,_sign)
        yield Request(url=url, callback=self.parse_artlist, dont_filter=True,meta={'userid':userid})

    def parse_artlist(self, response):
        bodyjson = json.loads(response._body)
        if not bodyjson['data']:
            return
        articles = ['https://www.toutiao.com' + b['source_url'] for b in bodyjson['data']]
        for a in articles:
            if not bf.exists(a):
                bf.insert(a)
                p.lpush(ARTICLES, a)
        p.execute()
        max_behot_time = bodyjson['next']['max_behot_time']
        userid = response.meta['userid']
        Honey = payload_for_get(userid, 1, str(max_behot_time))
        _as = Honey['as']
        _cp = Honey['cp']
        _sign = Honey['_signature']
        url = 'https://www.toutiao.com/c/user/article/?page_type=1' \
              '&user_id=%s&max_behot_time=%d&count=20' \
              '&as=%s&cp=%s&_signature=%s' % (userid, max_behot_time, _as, _cp, _sign)
        yield Request(url=url, callback=self.parse_artlist, dont_filter=True, meta={'userid': userid})