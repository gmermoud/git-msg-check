import sys

import argparse
import logging

from typing import List
from typing import Optional

from checker.validate import validate_msg

DEFAULT_MAX_SUMMARY_LENGTH = 50
DEFAULT_MAX_LINE_LENGTH = 72

ALLOWED_TAGS = ["BREAKING CHANGE"]


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Validate a commit message file")

    parser.add_argument("filename", type=str, help="the file to be validated")
    parser.add_argument(
        "--max-summary-length", type=int, default=50, help="maximum summary length"
    )
    parser.add_argument(
        "--max-line-length", type=int, default=72, help="maximum line length"
    )
    parser.add_argument(
        "--guidelines-url",
        type=str,
        default="https://github.com/gmermoud/git-msg-check#readme",
        help="URL to commit message guidelines",
    )
    parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    with open(args.filename, "r") as f:
        commit_msg = f.readlines()

        try:
            validate_msg(commit_msg, args)

            logging.info("SUCCESS: Commit message is valid")
        except AssertionError as err:
            sys.exit(
                f"FAIL: {err}\n\nPlease see our commit guidelines at {args.guidelines_url}."
            )
