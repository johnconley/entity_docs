# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EntityDocsItem(scrapy.Item):
    entity_id = scrapy.Field()
    filename = scrapy.Field()
    file = scrapy.Field()
