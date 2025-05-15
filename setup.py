from setuptools import setup

setup(
    name="git-msg-check",
    version="0.2",
    packages=["checker"],
    entry_points={"console_scripts": ["git-msg-check = checker.validate"]},
)
