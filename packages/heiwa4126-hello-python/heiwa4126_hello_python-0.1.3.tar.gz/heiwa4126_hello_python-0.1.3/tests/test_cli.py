from heiwa4126_hello_python.cli import parse_args


def test_parse_args_custom_msg():
    args = parse_args(["Hello"])
    assert args.message == "Hello"


def test_parse_args_default_msg():
    args = parse_args([])
    assert args.message == "Python"
