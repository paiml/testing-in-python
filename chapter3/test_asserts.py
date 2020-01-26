
def test_long_strings():
    string = ("This is a very, very, long string that has some differences"
            "that are hard to catch")
    expected = ("This is a very, very long string that hes some differences"
            "that are hard to catch")
    assert string == expected


def test_nested_dictionaries():
    result = {'first': 12, 'second': 13,
            'others': {'success': True, 'msg': 'A success message!'}}
    expected = {'first': 12, 'second': 13,
            'others': {'success': True, 'msg': 'A sucess message!'}}
    assert result == expected

def test_missing_key():
    result = {'first': 12, 'second': 13,
            'others': {'success': True, 'msg': 'A success message!'}}
    expected = {'first': 12, 'second': 13,
            'others': {'msg': 'A success message!'}}
    assert result == expected

