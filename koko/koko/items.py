# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KokoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # collection = 'amzon_1808'
    collection = 'amzon_1808'

    # name = scrapy.Field()
    # asin = scrapy.Field()
    # price = scrapy.Field()
    # star = scrapy.Field()
    # comment = scrapy.Field()
    # img = scrapy.Field()
    node = scrapy.Field()
    page = scrapy.Field()
    pages = scrapy.Field()
    state = scrapy.Field()
    bad_url = scrapy.Field()
    url = scrapy.Field()
    arr = scrapy.Field()
    product_url = scrapy.Field()