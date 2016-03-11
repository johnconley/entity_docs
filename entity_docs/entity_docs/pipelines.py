# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from boto.s3.connection import S3Connection
from boto.s3.key import Key

class EntityDocsPipeline(object):

    def open_spider(self, spider):
        access_key_id = "AKIAJW5SG3CRPIGYPETQ"
        secret_access_key = "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"
        conn = S3Connection(access_key_id, secret_access_key)
        self.bucket = conn.get_bucket('og-data-uploads')

    def process_item(self, item, spider):
        k = Key(self.bucket)
        k.key = '/'.join(['development', 'pdfs', 'test', item['filename']])
        k.set_contents_from_string(item['file'])
        return item
