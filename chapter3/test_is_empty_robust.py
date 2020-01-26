def is_empty(value):
    try:
        return len(value) == 0
    except TypeError:
        return False

def test_empty_list():
    assert is_empty([]) is True

def test_empty_dict():
    assert is_empty({}) is True

def test_list_is_not_empty():
    assert is_empty([1,2,3]) is False

def test_dict_is_not_empty():
    assert is_empty({"item": 1}) is False

def test_integer_is_false():
    assert is_empty(1) is False
