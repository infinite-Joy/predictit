import scrapy, os
dicti = {}
def links():
    '''function to return the links to match fact spider'''
    data_links = []
    for root, dirs, files in os.walk('/home/hhsecond/cricbuz_datav2/'):
        if not dirs:
            temp_list = []
            for file in files:
                if 'match-facts' in file or 'cricket-scorecard' in file:
                    current_path = 'http://127.0.0.1:8000' + os.path.join(root, file)
                    temp_list.append(current_path)
            if len(temp_list) == 2:
                data_links += temp_list
            else:
                print('links has file issues', temp_list)
    return data_links

class data_fetcher(scrapy.Spider):
    '''spider for fetching the toss'''
    allowed_domains = ['127.0.0.1:8000'] 
    name = 'data_fetcher'
    start_urls = links()

    def parse(self, response):
        global dicti
        title = response.url
        #title = title[0]
        if not 'T20' in title.upper() and not 'TEST' in title.upper():
            checking_res = response.url
            checking_res = checking_res.split('/')[:-1]
            checking_res = '/'.join(checking_res)
            if not checking_res in dicti.keys():
                dicti[checking_res] = []
            if 'cricket-scorecard' in response.url:#fetching match winner
                temp = response.xpath('//div[@class="cb-col cb-scrcrd-status cb-col-100 cb-text-complete"]/text()').extract()
                try:
                    dicti[checking_res].append(temp[0].split('won')[0])
                except IndexError:
                    pass
            if 'match-facts' in response.url:#fetching toss result
                temp = response.xpath('//div[./text()="Toss:"]/following-sibling::div[1]/text()').extract()
                try:
                    dicti[checking_res].append(temp[0].split('won')[0])
                except IndexError:
                    pass


    def close(self, reason):
        global dicti
        key_without_val = 0
        total_count = 0
        c1 = 0
        c2 = 0
        for key, val in dicti.items():
            total_count += 1
            if len(val) < 2:
                key_without_val += 1
            else:
                if val[0].strip() == val[1].strip():
                    c1 += 1
                else:
                    c2 += 1
#        print('total count', total_count)
#        print('key without val', key_without_val)
#        print('both are equal', c1)
#        print('both are different', c2)

