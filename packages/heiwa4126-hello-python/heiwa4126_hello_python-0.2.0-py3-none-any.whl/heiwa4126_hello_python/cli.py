import argparse


def parse_args(args=None):
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "message",
        nargs="?",
        default="Python",
        help="Your custom message (default: Python)",
    )
    return parser.parse_args(args)
