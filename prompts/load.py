import os


def get_instruction():
    with open(
        os.path.join(os.path.dirname(__file__), "sketchy.md"), "r", encoding="utf-8"
    ) as f:
        return f.read()
