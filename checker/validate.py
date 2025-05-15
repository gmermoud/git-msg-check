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

        assert len(line) <= args.max_line_length, (
            f"Line {line_num} exceeds character limit ({len(line)} > {args.max_line_length})"
        )

        # check header
        if line_num == 0:
            match = re.match(r"([\w ]+)(\[[\w ]+\])?: (.*)", line)
            assert match is not None, f"Header '{line.strip()}' has no component"

            # check prefix
            allowed_prefixes = args.allowed_prefixes
            assert (prefix := match.group(1)) in allowed_prefixes, (
                f"Prefix '{prefix}' is not in the list of allowed prefixes"
            )

            # check component
            component = match.group(2)
            if component is not None:
                component = component[1:-1]  # remove brackets

                max_component_length = args.max_line_length - args.max_summary_length
                assert len(component) <= max_component_length, (
                    f"Summary exceeds character limit ({len(component)} > {max_component_length})"
                )
                assert component[0].islower(), (
                    f"Component '{component}' must be lower case"
                )
                # check that component name does not contain any space
                assert " " not in component, (
                    f"Component '{component}' must not contain any space"
                )

            # check summary
            summary = match.group(3)

            # check that the summary does not exceed the maximal length
            assert len(summary) <= args.max_summary_length, (
                f"Summary exceeds character limit ({len(summary)} > {args.max_summary_length})"
            )
            # check that the summary starts with a lower case
            assert summary[0].islower(), "Summary must start with a lower case"
            # check that the summary does not end with a punctuation
            assert re.match(r"\w", summary[-1]), (
                "Summary must end with a regular character (no punctuation)"
            )
            # check that the summary is not trivial
            assert len(summary.split(" ")) > 2, (
                "Summary is trivial, please provide a meaningful summary"
            )
        elif line_num == 1:
            assert len(line.strip()) == 0, (
                "Details must be separated from header by an empty line"
            )
        elif line_num == 2:
            assert line[0] in ["*", "-"] or line[0].isupper(), (
                "Details must start with an upper case or a Markdown list"
            )

        line_num += 1


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate commit messages")
    parser.add_argument("path", type=str, help="Commit message")
    parser.add_argument(
        "--max-line-length", type=int, default=80, help="Max line length"
    )
    parser.add_argument(
        "--max-summary-length", type=int, default=55, help="Max summary length"
    )
    parser.add_argument(
        "--allowed-prefixes",
        type=str,
        nargs="+",
        default=["new", "fix", "refactor", "docs", "minor", "build", "misc"],
        help="Allowed prefixes",
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    with open(args.path, "r") as f:
        msg = f.readlines()

    validate_msg([line.strip() for line in msg], args)
