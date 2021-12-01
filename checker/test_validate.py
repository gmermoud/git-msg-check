import pytest
from typing import Any
from collections import namedtuple

from checker.validate import validate_msg

Namespace = namedtuple(
    "Namespace", ["max_line_length", "max_summary_length", "verbose"]
)


@pytest.fixture
def args() -> Namespace:
    return Namespace(72, 50, True)


def test_valid1(args: Any) -> None:
    msg = """Component: fix a serious bug with this component

Here are some details, and then some more stuff.
# Some stuff
# as comments""".split(
        "\n"
    )

    validate_msg(msg, args)


def test_valid2(args: Any) -> None:
    msg = """Component: fix a serious bug with this component
    """.split(
        "\n"
    )

    validate_msg(msg, args)


def test_valid3(args: Any) -> None:
    msg = """Component: fix a serious bug with this component

- A list of details
- Another bullet point

# Some stuff
# as comments""".split(
        "\n"
    )

    validate_msg(msg, args)


def test_valid4(args: Any) -> None:
    msg = """[BREAKING CHANGE] Component: fix a serious bug with this component

- A list of details
- Another bullet point

# Some stuff
# as comments""".split(
        "\n"
    )

    validate_msg(msg, args)


def test_invalid_lowercase_tag(args: Any) -> None:
    msg = """[Test] Component: Fix a serious bug""".split("\n")

    with pytest.raises(AssertionError, match="Tag must in upper case"):
        validate_msg(msg, args)


def test_invalid_capitalize_summary(args: Any) -> None:
    msg = """Component: Fix a serious bug with this component

# Some stuff
# as comments""".split(
        "\n"
    )

    with pytest.raises(AssertionError, match="Summary must start with a lower case"):
        validate_msg(msg, args)


def test_invalid_nospace_summary(args: Any) -> None:
    msg = """Component: fix a serious bug with this component
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
    msg = """Component: fix a serious bug with this component but is too long
    """.split(
        "\n"
    )

    with pytest.raises(AssertionError, match="Summary exceeds character limit"):
        validate_msg(msg, args)


def test_invalid_long_details(args: Any) -> None:
    msg = """Component: fix a serious bug with this component

This sentence is too long, although it is part of the details of the description.
    """.split(
        "\n"
    )

    with pytest.raises(AssertionError, match="exceeds character limit"):
        validate_msg(msg, args)


def test_invalid_trivial_summary(args: Any) -> None:
    msg = """Component: fix bug
    """.split(
        "\n"
    )

    with pytest.raises(AssertionError, match="Summary is trivial"):
        validate_msg(msg, args)


def test_invalid_lowercase_details(args: Any) -> None:
    msg = """Component: fix a serious bug with this component

details without capital letter
    """.split(
        "\n"
    )

    with pytest.raises(AssertionError, match="Details must start with an upper case"):
        validate_msg(msg, args)
