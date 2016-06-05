import scrapy
import time
pref = ''

class cricbuz_spider(scrapy.Spider):
	"""docstring for cricbuz_spider"""
	name = 'cricbuz'
	allowed_domains = ['cricbuzz.com']
	start_urls = ['http://www.cricbuzz.com/cricket-scorecard-archives']


	def parse(self, response):
		global pref
		years = response.xpath('//div[@class="cb-col-33 cb-col cb-col-rt"]/div/a/@href').extract()
		pref = '/'.join(response.url.split('/')[:-1])
		for year in years:
			time.sleep(5)
			yield scrapy.Request((pref + year), callback = self.series_parser)

	def series_parser(self, response):
		global pref
		series = response.xpath('//div[@class="cb-col-16 cb-col text-bold cb-srs-cat" and ./text()="International"]/following-sibling::div[1]/div/a/@href').extract()
		for each_series in series:
			time.sleep(5)
			yield scrapy.Request((pref + each_series), callback = self.match_parser)

	def match_parser(self, response):
		global pref
		matches = response.xpath('//div[@class="cb-col-60 cb-col cb-srs-mtchs-tm"]/a[1]/@href').extract()
		for match in matches:
			#time.sleep(5)
			print(match)
			time.sleep(5)
			yield scrapy.Request((pref + match), callback = self.match_details)

	def match_details(self, response):
		print(response.body)


