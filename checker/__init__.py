import sys
import re

import argparse
import logging

from typing import List
from typing import Optional

DEFAULT_MAX_SUMMARY_LENGTH = 50
DEFAULT_MAX_LINE_LENGTH = 72


ACTION_VERBS = [
    "fix",
    "enhance",
    "improve",
    "increase",
    "decrease",
    "include",
    "exclude",
    "add",
    "insert",
    "remove",
    "create",
    "delete",
    "deprecate",
    "make",
    "change",
    "adapt"
]

def validate_msg(msg: List[str], args: argparse.Namespace) -> None:
    assert len(msg) > 0, f"Commit message must "

    for line_num, line in enumerate(msg):
        assert len(line) <= args.max_line_length, f"Line {line_num} exceeds character limit ({len(line)} > {args.max_line_length})"

        # check header
        if line_num == 0:
            match = re.match("(\w+): (.*)", line)

            assert match is not None, f"Header '{line.strip()}' has no component"
            
            # check component
            component = match.group(1)
            max_component_length = args.max_line_length - args.max_summary_length
            assert len(component) <= max_component_length, f"Summary exceeds character limit ({len(component)} > {max_component_length})"
            assert component[0].isupper(), f"Component '{component}' must be capitalized"

            # check summary
            summary = match.group(2)

            assert len(summary) <= args.max_summary_length, f"Summary exceeds character limit ({len(summary)} > {args.max_summary_length})"
            assert summary[0].islower(), "Summary must start with a lower case"
            assert re.match("\w", summary[-1]), "Summary must end with a regular character (no punctuation)"

            assert summary.split(" ")[0] in ACTION_VERBS, f"Summary must start with an action verb (i.e. {', '.join(ACTION_VERBS)})"
            assert len(summary.split(" ")) > 2, "Summary is trivial, please provide a meaningful summary"
        elif line_num == 1:
            assert len(line) == 1 and line[0] == "\n", f"Commit details must be separated from header by an empty line"



def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Validate a commit message file")

    parser.add_argument("filename", type=str, help="the file to be validated")
    parser.add_argument(
        "--max-summary-length", 
        type=int, 
        default=50, 
        help="maximum summary length"
    )
    parser.add_argument(
        "--max-line-length", 
        type=int, 
        default=72, 
        help="maximum line length"
    )
    parser.add_argument(
        "--guidelines-url", 
        type=str, 
        help="URL to commit message guidelines"
    )

    args = parser.parse_args()
    
    with open(args.filename, "r") as f:
        commit_msg = f.readlines()

        try:
            validate_msg(commit_msg, args)
            
            logging.info("Commit message has been successfully validated.")
        except AssertionError as err:
            sys.exit(f"Error: {err}\n\nPlease see our commit guidelines at {args.guidelines_url}.")