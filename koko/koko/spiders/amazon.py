# -*- coding: utf-8 -*-
import scrapy
import pymysql
from koko.items import KokoItem
import re

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    # start_urls = ['http://amazon.com/']
    # https://www.amazon.com/b?node=3741521&page=1
    # client = pymongo.MongoClient(host='192.168.0.116', port=27017)
    def start_requests(self):

        with open('/home/just_study/Desktop/url.txt', 'r+') as f:
            while 1:
                u = f.readline()
                if not u:
                    break
                # ur = u[0:-1]
                # for i in range(1, 28):
                #     url = ur + '%s'%i
                yield scrapy.Request(url=u,callback=self.parse, meta={'lianjie':u})
            # 'proxy':'112.84.51.232:4278', 


    def parse(self, response):
        # arr = []
        res = response.xpath('//*[@id="mainResults"]/ul/li')
        s = response.xpath('//*[@id="bottomBar"]/div/span[@class="pagnDisabled"]/text()').extract_first()
        if s==None:
            pages = 2
        else:
            pages = s
        me_2 = response.meta['lianjie']
        node = re.search('node=(\d+)', me_2).group(1)
        page_now_num = re.search('page=(\d+)', me_2).group(1)
        if len(res)>0:
            
            # pages_num = response.meta['page_max_num']
            # pages = int(pages_num)
            
            arr = []
            for f in res:
                
                # //*[@id="mainResults"]/ul/li//img/@src
                get_sth = {}
                get_sth['name'] = f.xpath('.//div//a/h2/text()').extract_first()
                get_sth['product_url'] = f.xpath('.//div//a/@href').extract_first()
                get_sth['asin'] = f.xpath('./@data-asin').extract_first()
                qw = f.xpath('.//span[contains(@class,"sx-price-large")]/span/text()').extract_first()
                e = f.xpath('.//span[contains(@class,"sx-price-large")]/sup[2]/text()').extract_first()
                # item['price'] = '.'.join(qw + e) # type=list 去掉列表元组外面的方括号
                get_sth['price'] = '{}.{}'.format(qw,e)
                c = f.xpath('.//div//span[contains(@class,"a-declarative")]//a//i/span/text()').extract_first()
                if c==None:
                    get_sth['star'] = 0
                else:
                    get_sth['star'] = c.rstrip('out of 5 stars')
                get_sth['comment'] = f.xpath('.//div//span[@name]/../a/text()').extract_first()
                get_sth['img'] = f.xpath('.//img/@src').extract_first()
                arr.append(get_sth)

        
            item = KokoItem()
            item['pages'] = pages
            item['node'] = node
            item['state'] = 1
            item['page'] = page_now_num
            item['url'] = me_2
            item['arr'] = arr
            yield item
        else:
            pass
        next_page_url_ = response.xpath('//*[@id="pagnNextLink"]/@href').extract_first()
        next_page_url = response.urljoin(next_page_url_)
        yield scrapy.Request(url=next_page_url, callback=self.next_page_parse, meta={'lianjie':next_page_url,'pages':pages, 'node':node})
    

    def next_page_parse(self, response):
        res = response.xpath('//*[@id="centerMinus"]//ul/li')
        me_2 = response.meta['lianjie']
        node = response.meta['node']
        pages = response.meta['pages']
        page_now_num = re.search('page=(\d+)', me_2).group(1)
        if len(res)>0 :
            # pages_num = response.meta['page_max_num']
            # pages = int(pages_num)
            arr = []
            for f in res:
                
                # //*[@id="mainResults"]/ul/li//img/@src
                get_sth = {}
                get_sth['name'] = f.xpath('.//div[contains(@class,"a-spacing-none")]/a[contains(@class,"a-text-normal")]/h2/@title').extract_first()
                get_sth['product_url'] = f.xpath('.//div[contains(@class,"a-spacing-none")]/a[contains(@class,"a-text-normal")]/h2/../@href').extract_first()
                get_sth['asin'] = f.xpath('./@data-asin').extract_first()
                qw = f.xpath('.//span[contains(@class,"sx-price-large")]/span/text()').extract_first()
                e = f.xpath('.//span[contains(@class,"sx-price-large")]/sup[2]/text()').extract_first()
                # item['price'] = '.'.join(qw + e) # type=list 去掉列表元组外面的方括号
                get_sth['price'] = '{}.{}'.format(qw,e)
                c = f.xpath('.//div//span[contains(@class,"a-declarative")]//a//i/span/text()').extract_first()
                if c==None:
                    get_sth['star'] = 0
                else:
                    get_sth['star'] = c.rstrip('out of 5 stars')
                get_sth['comment'] = f.xpath('.//div//span[@name]/../a/text()').extract_first()

                get_sth['img'] = f.xpath('.//img[contains(@class,"cfMarker")]/@src').extract_first()
                if get_sth!=None:
                    arr.append(get_sth)

        
            item = KokoItem()
            pages = response.meta['pages']
            item['pages'] = pages
            item['node'] = node
            item['state'] = 1
            item['page'] = page_now_num
            item['url'] = me_2
            item['arr'] = arr
            yield item
        else:
            pass
        next_page_url_ = response.xpath('//*[@id="pagnNextLink"]/@href').extract_first()
        if next_page_url_!=None:
            next_page_url = response.urljoin(next_page_url_)
            yield scrapy.Request(url=next_page_url, callback=self.next_page_parse, meta={'lianjie':next_page_url,'pages':pages, 'node':node})
