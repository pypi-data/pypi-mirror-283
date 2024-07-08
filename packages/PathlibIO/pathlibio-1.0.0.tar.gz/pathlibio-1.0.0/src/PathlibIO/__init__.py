"""PathlibIO"""

__version__ = "1.0.0"

import argparse
from pathlib import Path

from .exit_code_tests import handlers as exit_code_handlers
from .properties_etc import handlers as properties_handlers

all_handlers = exit_code_handlers + properties_handlers

cli_action_name_to_handler = {
    handler.path_attr_name: handler
    for handler in all_handlers
}

STDIN_PATH = Path("-")

def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description = "")

    parser_action = parser.add_subparsers(
        metavar = "ACTION",
        dest = "action",
        required = True,
    )

    for handler in all_handlers:
        handler.add_args(parser_action)

    args = parser.parse_args()

    return args

def main() -> None:
    args = get_cli_args()

    handler = cli_action_name_to_handler[args.action]

    if (path := getattr(args, "path", None)) is None:
        # `home` and `cwd`
        return handler(None, args)

    if path != STDIN_PATH:
        return handler(path, args)

    while True:
        try:
            path_str = input()
        except EOFError:
            break

        path = Path(path_str)

        handler(path, args)
