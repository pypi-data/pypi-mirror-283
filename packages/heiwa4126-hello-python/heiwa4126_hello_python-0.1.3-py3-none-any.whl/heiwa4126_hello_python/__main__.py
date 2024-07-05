#!/usr/bin/env python3

from heiwa4126_hello_python.cli import parse_args
from heiwa4126_hello_python.hello import hello


def main():
    args = parse_args()
    hello(args.message)


if __name__ == "__main__":
    main()
