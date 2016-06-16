from __future__ import print_function

import pprint
from nose.plugins.skip import SkipTest

from create_data import get_all_texts
from create_data import get_player_info
from create_data import get_all_player_names
from create_data import not_match_any_pattern
from create_data import get_all_player_stats
from create_data import get_match_stats_for_player

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

def test_get_match_stats_for_player_invalid():
    all_player_stats = [{'Dhawal Kulkarni': ['Dhawal Kulkarni', '10', '1', '42', '2', '0', '1', '4.20', 'Barinder Sran']}]
    res = get_match_stats_for_player(all_player_stats)
    assert res == {}

def test_get_match_stats_for_player_valid():
    all_player_stats = [{'Graeme Cremer': ['Graeme Cremer', 'b D Kulkarni', '\\xa0\\xa0', ' ', '8', '11', '1', '0', '72']}]
    res = get_match_stats_for_player(all_player_stats)
    print(res)
    assert res == {'Graeme Cremer': ['Graeme Cremer', 'b D Kulkarni', '\\xa0\\xa0', ' ', '8', '11', '1', '0', '72']}
