#!/usr/bin/env python

"""This gets data from the cricbuzz site"""

# for python 2/3 compatible code
from __future__ import absolute_import, print_function

import sys
PYTHON3 = sys.version_info[0] == 3
if PYTHON3:
    xrange = range

from contextlib import closing

import lxml.html as html  # pip install 'lxml>=2.3.1'
from lxml.html.clean        import Cleaner
from selenium.webdriver     import Firefox         # pip install selenium
from werkzeug.contrib.cache import FileSystemCache  # pip install werkzeug

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

cache = FileSystemCache('.cachedir', threshold=100000)

url = "http://www.espncricinfo.com/ci/engine/series/index.html"

def get_all_content(url):
    """
    This handles all the javascript.
    also scrolls down to the bottom of the page
    this helps us in getting all the content later
    """
    browser.get(url)
    wait = WebDriverWait(browser, 10)
    while True:
        try:
            load_more = wait.until(EC.visibility_of_element_located(
                            (By.LINK_TEXT, 'Load More Commentary')))
        except TimeoutException:
            break

        load_more.click()

    while True:
        try:
            load_more = wait.until(EC.visibility_of_element_located(
                            (By.LINK_TEXT, 'Load Commentary')))
        except TimeoutException:
            break

    load_more.click()

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    return browser.page_source
    
def get_links(page_source):
    """This parses the page source for the links"""
    soup = BeautifulSoup(page_source, 'html.parser')
    texts = []
    links = []
    for link in soup.find_all('a'):
        texts.append(link.get_text())
        links.append(link.get('href'))

    link_data = dict(zip(texts,links))
    return link_data
    
def     
    
def iterate_through_century(link_data, century_prefix):
    for year_suff in xrange(00, 99):
        link = link_data.get("%s%s/%s" % ( century_prefix, year_suff-1, year_suff ))
        if link:
            return link
            page_source = get_all_content("http://www.espncricinfo.com%s" % link)
            link_data = get_links(page_source)
            

        if year_suff == 99:
            link = link_data.get("%s%s00" % ( century_prefix, year_suff ))
            if link:
                return link
                #page_source = get_all_content("http://www.espncricinfo.com%s" % link)
            
        link = link_data.get("%s%s" % (century_prefix, year_suff ))
        if link:
            return link
            #page_source = get_all_content("http://www.espncricinfo.com%s" % link)
    
    

if __name__ == '__main__':
    # get page
    page_source = cache.get(url)
    if page_source is None:
        # use firefox to get page with javascript generated content
        browser = Firefox()
        page_source = get_all_content(url)
        cache.set(url, page_source, timeout=60*60*24*7)  # week in seconds

    link_data = get_links(page_source)
    
    for century_prefix in (17, 18, 19, 20):
        iterate_through_century(link_data, century_prefix)
