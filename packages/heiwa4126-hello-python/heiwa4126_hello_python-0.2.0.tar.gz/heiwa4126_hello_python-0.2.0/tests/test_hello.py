import unittest
from unittest.mock import patch

from heiwa4126_hello_python.hello import hello


class TestMain(unittest.TestCase):
    @patch("cowsay.cow")
    def test_hello_default_msg(self, mock_cow):
        hello()
        mock_cow.assert_called_with("Hello Python")

    @patch("cowsay.cow")
    def test_hello_custom_msg(self, mock_cow):
        hello("Dolly")
        mock_cow.assert_called_with("Hello Dolly")
