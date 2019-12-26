# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PtpressspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    parentCat = scrapy.Field()
    subCat = scrapy.Field()
    bookName = scrapy.Field()
    bookISBN = scrapy.Field()
    bookAuthor = scrapy.Field()
    bookAuthorIntro = scrapy.Field()
    bookIntro = scrapy.Field()
    bookContentIntro = scrapy.Field()
    bookDir = scrapy.Field()
    bookPrice = scrapy.Field()
    bookDiscountPrice = scrapy.Field()
    bookPageCount = scrapy.Field()
    bookPublishTime = scrapy.Field()



