import argparse
from pathlib import Path

class Handler:
    def __init__(self, path_attr_name: str, add_path_arg: bool = True) -> None:
        self.path_attr_name = path_attr_name
        self.add_path_arg = add_path_arg

    def add_args(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        doclines = [
            line.strip("\n ")
            for line in
            self.get_path_attr(Path).__doc__.splitlines(keepends = False)
        ]
        doclines = [line for line in doclines if line]
        doc = " ".join(doclines)

        parser = subparsers.add_parser(self.path_attr_name, description = doc, help = doc)

        if self.add_path_arg:
            parser.add_argument("path",
                help = "The path to test / explore / manipulate. Pass '-' to read paths from stdin",
                type = Path
            )

        return parser

    def get_path_attr(self, path: Path):
        return getattr(path, self.path_attr_name)

    def impl_call(self, path: Path, args: argparse.Namespace):
        raise NotImplementedError

    def __call__(self, path: Path | None, args: argparse.Namespace) -> str:
        if path is None:
            path = args.path

        return self.impl_call(path, args)
