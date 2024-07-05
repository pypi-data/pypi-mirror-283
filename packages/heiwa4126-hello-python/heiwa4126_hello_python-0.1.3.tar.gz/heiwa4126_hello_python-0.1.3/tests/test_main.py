from heiwa4126_hello_python.hello import hello


def test_hello_custom_msg(capsys):
    hello("Dolly")
    captured = capsys.readouterr()
    assert captured.out == "Hello Dolly\n"


def test_hello_default_msg(capsys):
    hello()
    captured = capsys.readouterr()
    assert captured.out == "Hello Python\n"
