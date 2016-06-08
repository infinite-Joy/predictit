import scrapy
import time
import os #for creating directory tree based on year, series name and match name
pref = ''

class cricbuz_spider(scrapy.Spider):
    """docstring for cricbuz_spide
    Start url given to the spider is the archive page with year list. Functioning of spider can be defined like this:
    It Fetches the link to all the years -->
    From there, it would fetch the link to each series -->
    Series page will have link to each match in that series -->
    Match page will have other 4 subpages with different details which is specifying below
    cricket-scores: Commentary
    cricket-scorecard: Score card
    live-cricket-match-blog: blogs which would probably have details about climate and temperature
    cricket-match-facts: Facts like man of the mathc, total score, ranking etc.
    I would suggest to remove this big doc string, once you understand the concept
    """
    name = 'cricbuz'
    allowed_domains = ['cricbuzz.com']
    start_urls = ['http://www.cricbuzz.com/cricket-scorecard-archives']


    def parse(self, response):
    #Fetching year link
        global pref
        years = response.xpath('//div[@class="cb-col-33 cb-col cb-col-rt"]/div/a/@href').extract()
        pref = '/'.join(response.url.split('/')[:-1])
        for year in years:
            time.sleep(5)
            num_year = year.split('/')[-1]
            request = scrapy.Request((pref + year), callback = self.series_parser)
            request.meta['num_year'] = num_year
            yield request

    def series_parser(self, response):
    #Fetching series link
        global pref
        series = response.xpath('//div[@class="cb-col-16 cb-col text-bold cb-srs-cat" and ./text()="International"]/following-sibling::div[1]/div/a/@href').extract()
        for each_series in series:
            time.sleep(5)
            str_each_series = each_series.split('/')[-2]
            request = scrapy.Request((pref + each_series), callback = self.match_parser)
            request.meta['num_year'] = response.meta['num_year']
            request.meta['str_each_series'] = str_each_series
            yield request

    def match_parser(self, response):
    #Fetching match link
        global pref
        matches = response.xpath('//div[@class="cb-col-60 cb-col cb-srs-mtchs-tm"]/a[1]/@href').extract()
        for match in matches:
            time.sleep(5)
            request = scrapy.Request((pref + match), callback = self.match_details)
            request.meta['num_year'] = response.meta['num_year']
            request.meta['str_each_series'] = response.meta['str_each_series']
            request.meta['match_name'] = match.split('/')[-1]
            yield request

    def match_details(self, response):
    #fetching link to all four subpages
        r = response.meta
        url = response.url
        default_val = 'cricket-scores' #default value in the url which we need to replace for getting different pages
        path = str(r['num_year']) + '/' + str(r['str_each_series']) + '/' + str(r['match_name']) + '/'
        for page in ['cricket-scores','cricket-scorecard','live-cricket-match-blog','cricket-match-facts']:
            current_url = url.replace(default_val, page)
            current_path = path + page + '.html'
            time.sleep(5)
            request = scrapy.Request(current_url, callback = self.writefile)
            request.meta['current_path'] = current_path
            yield request

    def writefile(self, response):
    #writing source code of those pages into directory tree
    #Directory tree syntax  - c:/year/series/match/one_among_the_4_catagory.html
        current_path = response.meta['current_path']
        os.makedirs(os.path.dirname(current_path), exist_ok = True)
        with open('current_path', 'w+') as f:
                f.write(response.body)