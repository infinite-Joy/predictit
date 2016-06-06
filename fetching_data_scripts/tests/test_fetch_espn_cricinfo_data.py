import pickle
page_source = pickle.load( open( "tests/page_source.p", "rb" ) )

from get_data import get_links
from get_data import iterate_through_century

def test_get_links():
    assert( get_links(page_source).get("1933") == "/db/ARCHIVE/1930S/1933/" )

def test_iterate_through_century():
    link_data = {"1933": "/db/ARCHIVE/1930S/1933/"}
    assert(iterate_through_century(link_data, 19) == "/db/ARCHIVE/1930S/1933/")

