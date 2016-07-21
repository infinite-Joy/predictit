from create_data import get_all_texts


def test_get_all_texts():
    res = get_all_texts()
    assert "Chamu Chibhabha" in res

