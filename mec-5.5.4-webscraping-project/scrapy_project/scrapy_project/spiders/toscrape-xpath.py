import scrapy


class ToScrapeXPathSpider(scrapy.Spider):
    name = "toscrape-xpath"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('//span[@class="text"]/text()').get(),
                'author': quote.xpath('//span//small[@class="author"]//text()').get(),
                'tags': quote.xpath('//div[@class="tags"]//a[@class="tag"]//text()').getall(),
            }

        next_page = response.xpath('//ul[@class="pager"]//a//@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)