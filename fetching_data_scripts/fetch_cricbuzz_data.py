#!/usr/bin/env python

"""
This gets data from the cricbuzz site
"""
import sys
from contextlib import closing

import lxml.html as html # pip install 'lxml>=2.3.1'
from lxml.html.clean        import Cleaner
from selenium.webdriver     import Firefox         # pip install selenium
from werkzeug.contrib.cache import FileSystemCache # pip install werkzeug

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

cache = FileSystemCache('.cachedir', threshold=100000)

url = "http://www.cricbuzz.com/cricket-scores/15770/hk-vs-zim-1st-match-group-b-icc-world-t20-2016"

def get_all_content():
    wait = WebDriverWait(browser, 10)
    while True:
        try:
            load_more = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Load More Commentary')))
        except TimeoutException:
            break

        load_more.click()

    while True:
        try:
            load_more = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Load Commentary')))
        except TimeoutException:
            break

    load_more.click()
    
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# get page
page_source = cache.get(url)
if page_source is None:
    # use firefox to get page with javascript generated content
    with closing(Firefox()) as browser:
        browser.get(url)
        page_source = browser.page_source
    cache.set(url, page_source, timeout=60*60*24*7) # week in seconds


# extract text
root = html.document_fromstring(page_source)
# remove flash, images, <script>,<style>, etc
Cleaner(kill_tags=['noscript'], style=True)(root) # lxml >= 2.3.1
print root.text_content() # extract text
