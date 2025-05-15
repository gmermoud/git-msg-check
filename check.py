from checker import validate_msg

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
