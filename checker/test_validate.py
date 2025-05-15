import pytest
from typing import Any
from collections import namedtuple

from checker.validate import validate_msg

Namespace = namedtuple(
    "Namespace", ["max_line_length", "max_summary_length", "verbose", "allowed-prefixes"]
)


@pytest.fixture
def args() -> Namespace:
    return Namespace(72, 50, True, ["new", "fix", "refactor", "tests", "docs", "minor", "build", "misc"])


def test_valid1(args: Any) -> None:
    msg = """fix[component]: fix a serious bug with this component

Here are some details, and then some more stuff.
# Some stuff
# as comments""".split(
        "\n"
    )

    validate_msg(msg, args)


def test_valid2(args: Any) -> None:
    msg = """fix: serious bug with this component
    """.split(
        "\n"
    )

    validate_msg(msg, args)


def test_valid3(args: Any) -> None:
    msg = """fix: a serious bug with this component

- A list of details
- Another bullet point

# Some stuff
# as comments""".split(
        "\n"
    )

    validate_msg(msg, args)


def test_valid4(args: Any) -> None:
    msg = """new[optimizer]: add parameter for Adam scheme

- A list of details
- Another bullet point

# Some stuff
# as comments""".split(
        "\n"
    )

    validate_msg(msg, args)


def test_invalid_prefix(args: Any) -> None:
    msg = """New[optimizer]: add parameter for Adam scheme""".split("\n")

    with pytest.raises(AssertionError, match="Prefix 'New' is not in the list of allowed prefixes"):
        validate_msg(msg, args)


def test_invalid_capitalize_summary(args: Any) -> None:
    msg = """new[optimizer]: Add parameter for Adam scheme

# Some stuff
# as comments""".split(
        "\n"
    )

    with pytest.raises(AssertionError, match="Summary must start with a lower case"):
        validate_msg(msg, args)


def test_invalid_nospace_summary(args: Any) -> None:
    msg = """new[optimizer]: add parameter for Adam scheme
Here are some details.
# Some stuff
# as comments""".split(
        "\n"
    )

    with pytest.raises(
        AssertionError, match="Details must be separated from header by an empty line"
    ):
        validate_msg(msg, args)


def test_invalid_long_summary(args: Any) -> None:
    msg = """new[optimizer]: fix a serious bug with this component but is too long
    """.split(
        "\n"
    )

    with pytest.raises(AssertionError, match="Summary exceeds character limit"):
        validate_msg(msg, args)


def test_invalid_long_details(args: Any) -> None:
    msg = """new[optimizer]: add parameter for Adam scheme

This sentence is too long, although it is part of the details of the description.
    """.split(
        "\n"
    )

    with pytest.raises(AssertionError, match="exceeds character limit"):
        validate_msg(msg, args)


def test_invalid_trivial_summary(args: Any) -> None:
    msg = """new[optimizer]: tbd
    """.split(
        "\n"
    )

    with pytest.raises(AssertionError, match="Summary is trivial"):
        validate_msg(msg, args)


def test_invalid_lowercase_details(args: Any) -> None:
    msg = """new[optimizer]: add parameter for Adam scheme

details without capital letter
    """.split(
        "\n"
    )

    with pytest.raises(AssertionError, match="Details must start with an upper case"):
        validate_msg(msg, args)
