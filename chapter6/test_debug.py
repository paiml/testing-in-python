from hello_debug import add
import pytest

@pytest.fixture
def myobj():
    class Foo():pass
    return Foo()

def test_add():
    assert add(1,2) == 3

def test_add_object(myobj):
    assert add(1,myobj) == 3
    