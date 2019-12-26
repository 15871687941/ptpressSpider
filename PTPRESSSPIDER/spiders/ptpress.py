# -*- coding: utf-8 -*-
import scrapy
import json
from PTPRESSSPIDER.items import PtpressspiderItem
import math

class PtpressSpider(scrapy.Spider):
    name = 'ptpress'
    allowed_domains = ['www.ptpress.com.cn']
    start_urls = ['http://www.ptpress.com.cn/']

    def parse(self, response):
        parentCategoryUrl = "https://www.ptpress.com.cn/bookinfo/getFirstParent"
        return scrapy.Request(url=parentCategoryUrl, callback=self.parse_parent_cat)

    def parse_parent_cat(self, response):
        subCategoryUrl = "https://www.ptpress.com.cn/bookinfo/getBookTagByParentId"
        parentCatData = json.loads(response.text, encoding="utf-8")
        print(parentCatData)
        for parentTag in parentCatData["data"]:
            item = PtpressspiderItem()
            print(parentTag["tagId"], parentTag["tagName"])
            item["parentCat"] = parentTag["tagName"]
            data = {
                "parentId": parentTag["tagId"]
            }

            yield scrapy.FormRequest(
                url=subCategoryUrl,
                formdata=data,
                callback=self.parse_sub_cat,
                meta={"item": item}
            )

    def parse_sub_cat(self, response):
        bookListUrl = "https://www.ptpress.com.cn/bookinfo/getBookListForEBTag"
        item = response.meta["item"]
        subData = json.loads(response.text, encoding="utf-8")
        for subTag in subData["data"]:
            print(subTag["tagId"], subTag["tagName"])
            data = {
                "page": str(1),
                "rows": str(18),
                "bookTagId": subTag["tagId"],
                "orderStr": "hot"
            }
            item["subCat"] = subTag["tagName"]
            yield scrapy.FormRequest(
                url=bookListUrl,
                formdata=data,
                callback=self.parse_book_page,
                meta={"item": item, "bookListUrl": bookListUrl, "data": data}
                )

    def parse_book_page(self, response):
        bookListUrl = response.meta["bookListUrl"]
        data = response.meta["data"]
        print(data)
        bookListData = json.loads(response.text, encoding="utf-8")
        print(bookListData)
        bookItemCount = int(bookListData["data"]["total"])
        maxPage = math.ceil(bookItemCount / 18)
        for page in range(1, maxPage + 1):
            data["page"] = str(page)
            yield scrapy.FormRequest(
                url=bookListUrl,
                formdata=data,
                callback=self.parse_book_List,
                meta={"item": response.meta["item"]}
            )

    def parse_book_List(self, response):
        bookDetailUrl = "https://www.ptpress.com.cn/bookinfo/getBookDetailsById"
        bookListData = json.loads(response.text, encoding="utf-8")
        item = response.meta["item"]
        for bookData in bookListData["data"]["data"]:
            item["bookName"] = bookData.get("bookName", "")
            item["bookAuthor"] = bookData.get("author", "")
            item["bookPublishTime"] = bookData.get("publishDate", "")
            item["bookPrice"] = bookData.get("price", "")
            item["bookISBN"] = bookData.get("isbn", "")
            bookId = bookData["bookId"]
            data = {
                "bookId": bookId
            }
            yield scrapy.FormRequest(
                url=bookDetailUrl,
                formdata=data,
                callback=self.parse_book_detail,
                meta={"item": item}
            )

    def parse_book_detail(self, response):
        item = response.meta["item"]
        bookDetailData = json.loads(response.text, encoding="utf-8")
        bookDetail = bookDetailData.get("data", {})
        item["bookAuthorIntro"] = bookDetail.get("authorIntro", {}).get("data", "")
        item["bookIntro"] = bookDetail.get("specialWord", "")
        item["bookContentIntro"] = bookDetail.get("resume", {}).get("data", "")
        item["bookDir"] = bookDetail.get("bookDirectory", {}).get("data", "")
        item["bookDiscountPrice"] = bookDetail.get("discountPrice", item["bookPrice"])
        item["bookPageCount"] = bookDetail.get("bookDetail", {}).get("data", {}).get("data", "")
        return item






