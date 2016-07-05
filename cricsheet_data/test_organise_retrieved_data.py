from organise_retrieved_data import get_all_matches_yaml_list, \
                read_file_in_zip, get_all_cricket_cities

def test_get_all_matches_yaml_list():
    res = get_all_matches_yaml_list()
    assert len(res) == 3181

def test_read_file_in_zip():
    res = read_file_in_zip("913629.yaml")
    print(res)
    assert res["info"]["city"] == "London"

def test_read_file_in_zip_readme():
    res = read_file_in_zip("README.txt")
    print(res)
    assert len(res) == 198740

def test_read_file_in_zip2():
    res = read_file_in_zip("913629.yaml")
    print(res)
    assert res["info"]["city"] == "London"

@nottest
def test_get_all_cricket_cities():
    res = get_all_cricket_cities()
    print(res)
    assert res == 1
