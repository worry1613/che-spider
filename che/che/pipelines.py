# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



class ChePipeline(object):
    def process_item(self, item, spider):
        _id = item.get('_id')
        _title = item.get('_title')
        _writer = item.get('_user')
        _tags = item.get('_keywords')
        _time = item.get('_datetime')
        _content = item.get('_content')
        _text = item.get('_text')
        """
        数据写入文件
        """
        f = 'che/data/data.txt'
        fin = open(f,'a+')
        fin.write('%s_|||_%s_|||_%s_|||_%s_|||_%s_|||_%s\n' % (_id,_title,_time,'|++|'.join(_tags),_content,_text))
        fin.close()
        return ''
