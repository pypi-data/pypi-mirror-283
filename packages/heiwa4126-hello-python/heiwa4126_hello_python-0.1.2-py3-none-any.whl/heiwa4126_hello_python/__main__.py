#!/usr/bin/env python3

import argparse

from heiwa4126_hello_python.hello import hello


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "message",
        nargs="?",
        default="Python",
        help="Your custom message (default: Python)",
    )
    args = parser.parse_args()
    hello(args.message)


if __name__ == "__main__":
    main()
