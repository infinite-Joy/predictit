from __future__ import print_function

import pprint
from nose.plugins.skip import SkipTest

from parse_html import get_all_texts
from parse_html import get_player_info
from parse_html import get_all_player_names
from parse_html import not_match_any_pattern
from parse_html import get_all_player_stats
from parse_html import validate_stats
from parse_html import filter_invalid_match_stat

pp = pprint.PrettyPrinter(indent=4)

def test_get_all_texts():
    res = get_all_texts()
    assert "Chamu Chibhabha" in res

def test_get_player_info():
    texts = get_all_texts()
    res = get_player_info(texts, "Chamu Chibhabha")
    assert res == ['Chamu Chibhabha', 'b Bumrah', '\xa0\xa0', ' ', '13', '42', '0', '0', '30.95']

#@SkipTest
def test_get_all_player_names():
    res = get_all_player_names()
    assert "Graeme Cremer, " in res

def test_not_match_any_pattern():
    string = "abc vs def"
    ignore_pattern = ".*vs.*"
    res = not_match_any_pattern(string, ignore_pattern)
    assert res == False

def test_get_all_player_stats():
    res = get_all_player_stats()
    assert {'Dhawal Kulkarni': ['Dhawal Kulkarni', '10', '1', '42', '2', '0', '1', '4.20', 'Barinder Sran']} in res

def test_validate_stats_invalid():
    all_player_stats = [{'Dhawal Kulkarni': ['Dhawal Kulkarni', '10', '1', '42', '2', '0', '1', '4.20', 'Barinder Sran']}]
    res = validate_stats(all_player_stats)
    assert res == {}

def test_validate_stats_valid():
    all_player_stats = [{'Graeme Cremer': ['Graeme Cremer', 'b D Kulkarni', '\\xa0\\xa0', ' ', '8', '11', '1', '0', '72']}]
    res = validate_stats(all_player_stats)
    assert res == {'Graeme Cremer': ['Graeme Cremer', 'b D Kulkarni', '\\xa0\\xa0', ' ', '8', '11', '1', '0', '72']}

def test_filter_invalid_match_stat():
    valid_stats = filter_invalid_match_stat()
    assert valid_stats == {'Sikandar Raza': ['Sikandar Raza', 'b Barinder', '\xa0\xa0', ' ', '23', '54', '2', '0', '42.59'], 'Peter Moor': ['Peter Moor', 'lbw b Barinder', '\xa0\xa0', ' ', '3', '5', '0', '0', '60.00'], 'Hamilton Masakadza': ['Hamilton Masakadza', 'c Dhoni b D Kulkarni', '\xa0\xa0', ' ', '14', '21', '2', '0', '66.67'], 'Elton Chigumbura': ['Elton Chigumbura', 'b Bumrah', '\xa0\xa0', ' ', '41', '65', '1', '0', '63.08'], 'Graeme Cremer': ['Graeme Cremer', 'b D Kulkarni', '\xa0\xa0', ' ', '8', '11', '1', '0', '72.73'], 'Vusi Sibanda': ['Vusi Sibanda', 'c Dhoni b Bumrah', '\xa0\xa0', ' ', '5', '21', '0', '0', '23.81'], 'Chamu Chibhabha': ['Chamu Chibhabha', 'b Bumrah', '\xa0\xa0', ' ', '13', '42', '0', '0', '30.95'], 'Craig Ervine': ['Craig Ervine', 'c (sub)F Fazal b Axar', '\xa0\xa0', ' ', '21', '45', '1', '0', '46.67'], 'Richmond Mutumbami': ['Richmond Mutumbami', 'c Rahul b Chahal', '\xa0\xa0', ' ', '15', '27', '2', '0', '55.56'], 'Karun Nair': ['Karun Nair', 'c S Raza b Chatara', '\xa0\xa0', ' ', '7', '20', '1', '0', '35.00'], 'Tendai Chatara': ['Tendai Chatara', 'c Rayudu b Bumrah', '\xa0\xa0', ' ', '4', '10', '0', '0', '40.00']}
