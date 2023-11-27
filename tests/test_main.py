from eggi.main import say_something


def test_say_something():
    something = "Hello World!"
    assert say_something(something) == "Something: Hello World!"
