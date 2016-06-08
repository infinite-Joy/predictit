import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class cricbuz_spider(CrawlSpider):
    """docstring for cricbuz_spider"""
    name = 'cricbuz'
    allowed_domains = ['cricbuzz.com']
    start_urls = ['http://www.cricbuzz.com/cricket-scorecard-archives']

    rules = (
        Rule(LinkExtractor(restrict_xpaths = ('//div[@class="cb-col-33 cb-col cb-col-rt"]/div')), callback = 'year_parser'),
        )


    def year_parser(self, response):
        fname = response.url.split('/')[-1] + '.html'
        with open(fname, 'wb') as f:
                f.write(response.body)
#response.xpath('//div[@class="cb-col-16 cb-col text-bold cb-srs-cat" and ./text()="International"]/following-sibling::div[1]/div/a/span/text()').extract()
#'//div[@class="cb-col-33 cb-col cb-col-rt"]/div
