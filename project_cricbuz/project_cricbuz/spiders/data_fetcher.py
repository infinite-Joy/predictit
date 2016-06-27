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

    def rm_spcl(self, string):
        assert isinstance(string, str)   
        out_string = ''
        for c in string:
            if not c.isalnum():
                out_string += ' '
            else:
                out_string += c
        return out_string.strip()

    def ground_name_fetcher(self, response, checking_res) :
        temp = response.xpath('//span[./text() = "Venue: "]/parent::div/text()').extract()
        varify = 0
        for val in temp:
            if not val.isspace() and val and not ':' in val:
                dicti[checking_res]['cricket-scores'].append(val)
                verify = 1
        if verify == 0:
            print('ground name fetching error: ', response.url)

    def time_fetcher(self, response, checking_res):
        date = response.xpath('.//*[@id="matchCenter"]/div[1]/div/span[4]/text()').extract()
        temp = response.xpath('//span[./text() = "Venue: "]/parent::div/text()').extract()
        varify = 0
        for time in temp:
            if ':' in time:
                try:
                    temp_date = self.rm_spcl(date[0])
                    print('date from special remove', temp_date)
                    dicti[checking_res]['cricket-scores'].append(temp_date + '==' + time)
                except IndexError:
                    print('date index error', response.url)
                    dicti[checking_res]['cricket-scores'].append('error')
                verify = 1
        if verify == 0:
            print('time & date fetching error', response.url)


    def team_name_fetcher(self, response, checking_res):
        temp = response.xpath('//title/text()').extract()
        temp = temp[0].upper().split(',')[0]
        temp = temp.split('VS')
        try:
            dicti[checking_res]['cricket-scores'] += temp
        except IndexError:
            print('team_name index error', response.url)
            dicti[checking_res]['cricket-scores'].append('error')
        
    def match_winner(self, response, checking_res):
        temp = response.xpath('//div[@class="cb-col cb-scrcrd-status cb-col-100 cb-text-complete"]/text()').extract()
        try:
            dicti[checking_res]['cricket-scorecard'].append(temp[0].split('won')[0])
        except IndexError:
            print('match_winner index error', response.url)
            dicti[checking_res]['cricket-scorecard'].append('error')

    def toss_winner(self, response, checking_res):
        temp = response.xpath('//div[./text()="Toss:"]/following-sibling::div[1]/text()').extract()
        try:
            dicti[checking_res]['match-facts'].append(temp[0].split('won')[0])
        except IndexError:
            print('match_facts index error', response.url)
            dicti[checking_res]['match-facts'].append('error')

    def html_parser(self, response):
        title = response.url
        #title = title[0]
        if not 'T20' in title.upper() and not 'TEST' in title.upper():
            checking_res = response.url
            checking_res = checking_res.split('/')[:-1]
            checking_res = '/'.join(checking_res)
            if not checking_res in dicti.keys():
                #creating dictionary of dictionaries to store the content from four files of cricubz
                dicti[checking_res] = {'cricket-scorecard':[], 'match-facts':[], 'cricket-scores':[], 'match-blog':[]}

            if 'cricket-scorecard' in response.url:#fetching match winner
                self.match_winner(response, checking_res)
                
                
            elif 'match-facts' in response.url:#fetching toss result
                self.toss_winner(response, checking_res)

            elif 'cricket-scores' in response.url:
                #pass

                #function to find ODI or TEST or T20
                temp = 0
                try:
                    temp1 = response.xpath(".//*[@id='matchCenter']/div[2]/div[1]/div/div[1]/div[1]/div[2]/text()").extract()
                    temp2 = response.xpath(".//*[@id='matchCenter']/div[2]/div[1]/div/div[1]/div[1]/div[1]/text()").extract()
                    if temp1:
                        temp1 = temp1[0].split('(')
                        temp1 = temp1[1].split()
                        temp1 = temp1[0]
                        temp1 = int(temp1.strip())
                    if temp2:
                        temp2 = temp2[0].split('(')
                        temp2 = temp2[1].split()
                        temp2 = temp2[0]
                        temp2 = int(temp2.strip())
                    temp = temp1 + temp2
                    if temp < 41 or temp > 100:
                        print(response.url)
                except Exception as e:
                    print('exception raised', e)
                self.team_name_fetcher(response, checking_res)
                self.ground_name_fetcher(response, checking_res)
                self.time_fetcher(response, checking_res)


            elif 'match-blog' in response.url:
                pass


            else:
                pass#print('unknown file name')
    
    def climate_from_commentary(self, response):
        for key, val in dicti.items():
            for value in val[0]:
                if any(word in value for word in self.climatic_words):
                    val[0] = 'climatic condition found'
                else:
                    val[0] = 'climatic condition not found'


    def parse(self, response):
        self.html_parser(response)
        


    def close(self, reason):
        with open('tabular.txt', 'w+') as f:
            for key, val in dicti.items():
                try:
                    temp_string = ''
                    delim = '=='
                    for value in val['cricket-scores']:
                        temp_string += value + delim
                    temp_string += val['match-facts'][0] + delim
                    temp_string += val['cricket-scorecard'][0]
                    temp_key = key.split('cricbuz_datav2/')[1]
                    temp_key = temp_key.split('/')
                    string = temp_key[0] + delim + temp_key[1] + delim + temp_key[2] + delim + temp_string
                    f.write(string + '\n')
                except Exception as e:
                    print('exception from close', e, key + str(val['cricket-scores']) + str(val['match-facts']) + str(val['cricket-scorecard']))