from eggi.main import say_something


def test_say_something():
    assert say_something() == "Hello World!"
