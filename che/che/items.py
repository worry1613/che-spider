# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CheArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    _user = scrapy.Field()
    _title = scrapy.Field()
    _keywords = scrapy.Field()
    _content = scrapy.Field()
    _datetime = scrapy.Field()
    _text = scrapy.Field()
