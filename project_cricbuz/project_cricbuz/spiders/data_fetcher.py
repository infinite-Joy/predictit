import scrapy, os
dicti = {}
def links():
    '''function to return the links to match fact spider'''
    data_links = []
    for root, dirs, files in os.walk('/home/hhsecond/cricbuz_datav2/'):
        if not dirs:
            temp_list = []
            for file in files:
                current_path = 'http://127.0.0.1:8000' + os.path.join(root, file)
                temp_list.append(current_path)
            if len(temp_list) == 4:
                data_links += temp_list
            else:
                with open('links_with_file_issues.txt', 'a+') as f:
                    f.write(str(temp_list))
    return data_links

class data_fetcher(scrapy.Spider):
    '''spider for fetching the toss'''
    allowed_domains = ['127.0.0.1:8000'] 
    name = 'data_fetcher'
    start_urls = links()
    climatic_words = [' hot ','hotter','hottest','climate','climatic','cool','cold','snow','breeze','wind','cloud','rain','rainy','cloudy','sunny','temperature','wet','dew','humid','humidity','water']

    def html_parser(self, response, dicti):
        title = response.url
        #title = title[0]
        if not 'T20' in title.upper() and not 'TEST' in title.upper():
            checking_res = response.url
            checking_res = checking_res.split('/')[:-1]
            checking_res = '/'.join(checking_res)
            if not checking_res in dicti.keys():
                #creating dictionary of dictionaries to store the content from four files of cricubz
                
                dicti[checking_res] = {'cricket-scorecard':[], 'match-facts':[], 'cricket-scores':[], 'match-blog':[]}
                #dicti[checking_res] = []
            if 'cricket-scorecard' in response.url:#fetching match winner
                temp = response.xpath('//div[@class="cb-col cb-scrcrd-status cb-col-100 cb-text-complete"]/text()').extract()
                try:
                    dicti[checking_res]['cricket-scorecard'].append(temp[0].split('won')[0])
                except IndexError:
                    pass
            if 'match-facts' in response.url:#fetching toss result
                temp = response.xpath('//div[./text()="Toss:"]/following-sibling::div[1]/text()').extract()
                try:
                    dicti[checking_res]['match-facts'].append(temp[0].split('won')[0])
                except IndexError:
                    pass
            if 'cricket-scores' in response.url:
                temp = response.xpath('//body//text()').extract()
                dicti[checking_res]['cricket-scores'].append(temp)

            if 'match-blog' in response.url:
                temp = response.xpath('//body//text()').extract()
                dicti[checking_res]['match-blog'].append(temp)
    
    def climate_from_commentary(self, response, dicti):
        for key, val in dicti.items():
            for value in val[0]:
                if any(word in value for word in self.climatic_words):
                    val[0] = 'climatic condition found'
                else:
                    val[0] = 'climatic condition not found'


    def parse(self, response):
        self.html_parser(response, dicti)
        #self.climate_from_commentary(response, dicti)
        


    def close(self, reason):
        for key, val in dicti.items():
                try:
                    with open('commentary.txt', 'a+') as f:
                        f.write('\n=======================================' + str(key) + '\n' + str(val['cricket-scores']))
                    with open('blog.txt', 'a+') as f:
                        f.write('\n=======================================' + str(key) + '\n' + str(val['match-blog']))
                except IndexError:
                    print('error with the dictionary index')