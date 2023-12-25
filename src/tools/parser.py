"""Module for parser"""

import argparse


def arg_parser() -> argparse.ArgumentParser:
    """
    Parse the arguments

    Returns:
        Any: The arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--channel",
        type=str,
        help="Channel id",
        required=True,
    )
    parser.add_argument(
        "-i",
        "--interface",
        type=str,
        help="Interface name",
        required=True,
    )
    return parser.parse_args()
