import re
from typing import List
from argparse import Namespace


def validate_msg(msg: List[str], args: Namespace) -> None:
    assert len(msg) > 0, "Commit message must not be empty"

    # this counter is incremented for every non-commented line
    line_num = 0

    for line_idx, line in enumerate(msg):
        if args.verbose:
            print(f"DEBUG: process line {line_idx}\t{line}")

        # skip comments
        if line.strip().startswith("#"):
            continue

        assert (
            len(line) <= args.max_line_length
        ), f"Line {line_num} exceeds character limit ({len(line)} > {args.max_line_length})"

        # check header
        if line_num == 0:
            match = re.match(r"(\[[\w ]+\] )?([\w ]+): (.*)", line)
            assert match is not None, f"Header '{line.strip()}' has no component"

            # check optional tag
            tag = match.group(1)
            if tag is not None:
                assert tag.upper() == tag, f"Tag must in upper case (found: '{tag}')"

            # check component
            component = match.group(2)
            max_component_length = args.max_line_length - args.max_summary_length
            assert (
                len(component) <= max_component_length
            ), f"Summary exceeds character limit ({len(component)} > {max_component_length})"
            assert component[
                0
            ].isupper(), f"Component '{component}' must be capitalized"

            # check summary
            summary = match.group(3)

            assert (
                len(summary) <= args.max_summary_length
            ), f"Summary exceeds character limit ({len(summary)} > {args.max_summary_length})"
            assert summary[0].islower(), "Summary must start with a lower case"
            assert re.match(
                r"\w", summary[-1]
            ), "Summary must end with a regular character (no punctuation)"
            assert (
                len(summary.split(" ")) > 2
            ), "Summary is trivial, please provide a meaningful summary"
        elif line_num == 1:
            assert (
                len(line.strip()) == 0
            ), "Details must be separated from header by an empty line"
        elif line_num == 2:
            assert (
                line[0] in ["*", "-"] or line[0].isupper()
            ), "Details must start with an upper case or a Markdown list"

        line_num += 1
