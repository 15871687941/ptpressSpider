# -*- coding: utf-8 -*-
import scrapy


class PtpressSpider(scrapy.Spider):
    name = 'ptpress'
    allowed_domains = ['www.ptpress.com.cn']
    start_urls = ['http://www.ptpress.com.cn/']

    def parse(self, response):
        pass
