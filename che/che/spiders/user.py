# -*- coding: utf-8 -*-
# @创建时间 : 10/12/2018 
# @作者    : worry1613(549145583@qq.com)
# GitHub  : https://github.com/worry1613
# @CSDN   : http://blog.csdn.net/worryabout/
from bs4 import BeautifulSoup
from scrapy_redis.spiders import RedisSpider
import json
import sys
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy_redis.spiders import RedisSpider
import logging



from che.util import getresponsejson,get_js,payload_for_get



# class BlogUserSpider(RedisSpider):
class UserSpider(Spider):
    name = "user"
    # allowed_domains = ["blog.csdn.net"]
    # redis_key = USERKEY

    Honey = payload_for_get('', 1, '0')
    _as = Honey['as']
    _cp = Honey['cp']
    _sign = Honey['_signature']
    url = 'https://www.toutiao.com/api/pc/feed/?category=news_car' \
          '&utm_source=toutiao&widen=1&max_behot_time=%d&max_behot_time_tmp=%d' \
          '&tadrequire=true&as=%s&cp=%s&_signature=%s' % (0, 0, _as, _cp, _sign)
    start_urls = [url]

    def __init__(self, *args, **kwargs):
        self.page=1
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(UserSpider, self).__init__(*args, **kwargs)

    def parse(self,response):
        """
        不做数据处理，只是找到博客url，写入redis
        :param response:
        :return:
        """
        # strjson = getresponsejson(response)
        bodyjson = json.loads(response._body)
        if not bodyjson:
            return
        # f = open('data/user_url.txt', 'a+')
        users = ['http://www.toutiao.com' + b['media_url'] for b in bodyjson['data'] if 'media_url' in b]

        max_behot_time = bodyjson['next']['max_behot_time']
        # for u in users:
        #     yield Request(url=u, callback=self.parse_user_id, dont_filter=True)


        Honey = payload_for_get('', 1, str(max_behot_time))
        _as = Honey['as']
        _cp = Honey['cp']
        _sign = Honey['_signature']
        url = 'https://www.toutiao.com/api/pc/feed/?category=news_car' \
              '&utm_source=toutiao&widen=1&max_behot_time=%d&max_behot_time_tmp=%d' \
              '&tadrequire=true&as=%s&cp=%s&_signature=%s' % (max_behot_time,max_behot_time,_as,_cp,_sign)
        yield Request(url=url, callback=self.parse, dont_filter=True)
        #     url = b['personalPage']
        #     # logging.info('%d,%s' % (u,url))
        #     f.write('%d,%s\n' % (u,url))
        # f.close()
        # self.page += 1
        # url = 'http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=18&page={}&size=20&' \
        #       'callback=jQuery11240332517150833070661_156870333332448051&_=156870333333333332448052'.format(str(self.page))
        # # self.log(url,level=logging.INFO)
        # yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse_user_id(self,response):
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        script = soup.find('script', {'type': 'text/javascript'}).get_text()
        start = script.find('id:')+3
        end = script[start:].find(',')
        userid = script[start:start+end].strip()
        fu = open('data/userids.txt', 'a+')
        fu.write(userid+'\n')
        fu.close()
        # url = 'https://www.toutiao.com/c/user/article/?page_type=1' \
        #       '&user_id=%d&max_behot_time=%d&count=20' \
        #       '&as=%s&cp=%s&_signature=%s' % (userid,max_behot_time,_as,_cp,_sign)
