#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
import re
from media_crawl.items import ArticleItem


class SuperExpressSpider(scrapy.Spider):

    name = "SE"
    allowed_domains = ["se.pl"]
    start_urls = [
        "http://www.se.pl/wiadomosci/polityka/",
        "http://www.se.pl/wiadomosci/polska/",
        "http://www.se.pl/wiadomosci/swiat/"
                  ]

    def parse(self, response):
        for href in response.xpath(u'//a[@title="Następna strona"]/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse)

        for href in response.xpath('//div[@class="title "]/h2/a/@href'):
            yield scrapy.Request(href.extract(), callback=self.parse_article_contents)

    def parse_article_contents(self, response):
        item = ArticleItem()
        item["title"] = response.xpath('//article/div[@class="title "]/h1/text()').extract()[0]
        item["date"] = response.xpath('//meta[@itemprop="datePublished"]/@content').extract()[0]
        item["link"] = response.url
        lead = self.extract_text(" ".join(response.xpath('//div[@class="lead"]/p/text()').extract()))
        text = self.extract_text(" ".join(response.xpath('//div[@itemprop="articleBody"]/p/text()').extract()))
        item["text"] = lead + " " + text
        if item["text"]:
            yield item

    def extract_text(self, raw_text):
        return re.sub(r'<[^>]*?>', ' ', raw_text).strip()