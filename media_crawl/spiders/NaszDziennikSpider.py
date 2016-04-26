import scrapy
import re
from media_crawl.items import ArticleItem


class NaszDziennikSpider(scrapy.Spider):

    name = "NaszDziennik"
    allowed_domains = ["naszdziennik.pl"]
    start_urls = [
        "http://www.naszdziennik.pl/polska",
        "http://www.naszdziennik.pl/swiat",
        "http://www.naszdziennik.pl/ekonomia"
                  ]

    def parse(self, response):
        for href in response.xpath('//div[@class="pagination"]/a[@title="Starsze"]/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse)

        for href in response.xpath('//div[@class="article"]/h2/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_article_contents)

    def parse_article_contents(self, response):
        item = ArticleItem()
        item["title"] = response.xpath('//div[@id="article"]/h1/text()').extract()[0]
        item["date"] = response.xpath('//div[@id="article-date"]/text()').extract()[0].strip('\n').strip()
        item["link"] = response.url
        lead = self.extract_text(" ".join(response.xpath('//div[@id="article-subtitle"]/p/text()').extract()))
        text = self.extract_text(" ".join(response.xpath('//div[@id="article-content"]/p/text()').extract()))
        item["text"] = lead + " " + text
        if item["text"]:
            yield item

    def extract_text(self, raw_text):
        return re.sub(r'<[^>]*?>', ' ', raw_text).strip()