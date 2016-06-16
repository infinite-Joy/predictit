from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from bs4 import BeautifulSoup
import re

# modules changed in python 3
try:
    import urllib.request as ur
    from urllib.parse import urljoin
except ImportError:
    import urllib as ur
    from urlparse import urljoin

from ignore_words import ignore_words
from ignore_words import ignore_patters


html = ur.urlopen('file:page_source/afg-vs-hk-5th-t20i-afghanistan-and-hong-kong-and-oman-in-uae-2015-score-card').read()
url = "http://www.cricbuzz.com"

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

def get_player_info(texts, player_name):
    for i,item in enumerate(texts):
        if item == player_name:
            get_player_statss = [texts[x] for x in range(i, i+9)]
            return get_player_statss

def not_match_any_pattern(string, ignore_pattern):
    pattern = re.compile(ignore_pattern)
    if pattern.match(string):
        return False
    return True

def is_player_name(tag):
    if len(tag.text.split()) > 3:
        return False
    elif tag.text in ignore_words:
        return False
    else:
        return True

def relevant_tags(tag):
    tag['href'] = urljoin(url, tag['href'])
    if is_player_name(tag) and \
        all(not_match_any_pattern(tag.text, ignore_pattern) for ignore_pattern in ignore_patters):
        return True

def get_all_player_names():
    all_players = []
    relevant_tag_list = filter(relevant_tags, soup.findAll('a', href=True))
    for tag in relevant_tag_list:
        all_players.append(tag.text)
    return list(set(all_players))

def get_player_info(texts, player_name):
    for i,item in enumerate(texts):
        if item == player_name:
            get_player_statss = [texts[x] for x in range(i, i+9)]
            return get_player_statss

def get_all_player_stats():
    all_player_stats = []
    for player in get_all_player_names():
        all_player_stats.append({player: get_player_info(texts, player)})
    return all_player_stats

def validate_stats(all_player_stats):
    player_match_stats = {}
    num_pattern = "\d+"
    pattern = re.compile(num_pattern)
    for player_stat in all_player_stats:
        for player_name, player_stats in player_stat.items(): # dict.items() is py3 code. need to make py2 compat
            if all(map(pattern.match, player_stats[4:])):
                player_match_stats[player_name] = player_stats
    return player_match_stats

def filter_invalid_match_stat():
    all_player_stats = get_all_player_stats()
    valid_stats = validate_stats(all_player_stats)
    return valid_stats

