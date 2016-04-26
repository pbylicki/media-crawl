import scrapy
import re
from media_crawl.items import ArticleItem


class GazetaSpider(scrapy.Spider):

    name = "GazetaPl"
    allowed_domains = ["gazeta.pl"]
    start_urls = [
        "http://wiadomosci.gazeta.pl/wiadomosci/0,114883.html#TRNavSST",  # Polska
        "http://wiadomosci.gazeta.pl/wiadomosci/0,114884.html#TRNavSST",  # Polityka
        "http://wiadomosci.gazeta.pl/wiadomosci/0,114881.html#TRNavSST"   # Swiat
    ]

    def parse(self, response):
        for href in response.xpath('//div[@class="pagination"]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse)

        for href in response.xpath('//article/header/h3/a/@href'):
            yield scrapy.Request(href.extract(), callback=self.parse_article_contents)

    def parse_article_contents(self, response):
        item = ArticleItem()
        item["title"] = response.xpath('//div[@class="holder_top"]/h1/text()').extract()[0]
        item["date"] = self.extract_date(response.xpath('//div[@id="gazeta_article_date"]/text()').extract()[0])
        item["link"] = response.url
        lead = self.extract_text("".join(response.xpath('//div[@id="gazeta_article_lead"]/.').extract()))
        text = self.extract_text("".join(response.xpath('//div[@id="artykul"]/.').extract()))
        item["text"] = lead + " " + text
        yield item

    def extract_date(self, date_string):
        date = re.findall(r"[0-9]{1,2}\.[0-9]{2}\.[0-9]{4}", date_string)
        return date[0] if date else ""

    def extract_text(self, raw_text):
        return re.sub(r'<[^>]*?>', ' ', raw_text).strip()