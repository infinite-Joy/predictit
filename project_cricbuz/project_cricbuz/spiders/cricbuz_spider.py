import scrapy
class cricbuz_spider(scrapy.Spider):
	"""docstring for cricbuz_spider"""
	name = 'cricbuz'
	allowed_domains = ['cricbuzz.com']
	start_urls = ['http://www.cricbuzz.com/cricket-scorecard-archives', 'http://www.cricbuzz.com/cricket-scorecard-archives/2011']
	def parse(self, response):
		fname = response.url.split('/')[-1] + '.html'
		with open(fname, 'wb') as f:
				f.write(response.body)
#response.xpath('//div[@class="cb-col-16 cb-col text-bold cb-srs-cat" and ./text()="International"]/following-sibling::div[1]/div/a/span/text()').extract()
				