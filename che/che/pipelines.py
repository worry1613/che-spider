# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class ChePipeline(object):
    def process_item(self, item, spider):
        _id = item.get('_id')
        _title = item.get('_title')
        _writer = item.get('_user')
        _tags = item.get('_keywords')
        _time = item.get('_datetime')
        _content = item.get('_content')
        """
        数据写入文件
        """
        f = '%d.txt' % (_writer,)
        fin = open(f,'a+')

        fin.write('%d_|||_%s_|||_%s_|||_%s_|||_%s\n' % (_id,_title,_time,'|+|'.join(_tags),_content))
        fin.close()
        return ''
