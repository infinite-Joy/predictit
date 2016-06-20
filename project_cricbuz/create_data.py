from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from bs4 import BeautifulSoup
import re

try:
    import urllib.request as ur
except ImportError:
    import urllib as ur

html = ur.urlopen('page_source/zim-vs-ind-1st-odi-india-tour-of-zimbabwe-2016').read()

soup = BeautifulSoup(html, 'html.parser')
texts = soup.findAll(text=True)

try:
    str = unicode
except NameError:
    pass # Forward compatibility with Py3k

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

def get_all_texts():
    visible_texts = []
    for text in texts:
        try:
            if visible(text):
                visible_texts.append(text)
        except UnicodeEncodeError as e:
            pass
    return visible_texts

if __name__ == '__main__':
    prin("".join(get_all_texts()))

