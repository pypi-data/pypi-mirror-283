import argparse
from pathlib import Path

from .Handler import Handler

class TesterHandlerSimple(Handler):
    def impl_call(self, path: Path, args: argparse.Namespace, *attr_args, **attr_kwargs):
        if not self.get_path_attr(path)(*attr_args, **attr_kwargs):
            raise SystemExit(1)

class TesterHandlerExists(TesterHandlerSimple):
    def add_args(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        parser = super().add_args(subparsers)
        parser.add_argument("--follow-symlinks", action = argparse.BooleanOptionalAction, default = True)

    def impl_call(self, path: Path, args: argparse.Namespace):
        return super().impl_call(path, args, follow_symlinks = args.follow_symlinks)

class TesterHandlerSamefile(TesterHandlerSimple):
    def add_args(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        parser = super().add_args(subparsers)
        parser.add_argument("other_path", type = Path)

    def impl_call(self, path: Path, args: argparse.Namespace):
        return super().impl_call(path, args, args.other_path)

class TesterHandlerMatch(TesterHandlerSimple):
    def add_args(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        parser = super().add_args(subparsers)
        parser.add_argument("path_pattern")
        parser.add_argument("--case-sensitive", action = argparse.BooleanOptionalAction)

    def impl_call(self, path: Path, args: argparse.Namespace):
        return super().impl_call(path, args, args.path_pattern, case_sensitive = args.case_sensitive)

class TesterHandlerIsRelativeTo(TesterHandlerSimple):
    def add_args(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        parser = super().add_args(subparsers)
        parser.add_argument("other")

    def impl_call(self, path: Path, args: argparse.Namespace):
        return super().impl_call(path, args, args.other)

handlers = [
    TesterHandlerExists("exists"),
    TesterHandlerSimple("is_symlink"),
    TesterHandlerSimple("is_file"),
    TesterHandlerSimple("is_dir"),
    TesterHandlerSimple("is_char_device"),
    TesterHandlerSimple("is_block_device"),
    TesterHandlerSimple("is_fifo"),
    TesterHandlerSimple("is_socket"),

    TesterHandlerSimple("is_junction"),
    TesterHandlerSimple("is_mount"),
    TesterHandlerSimple("is_absolute"),
    TesterHandlerSimple("is_reserved"),

    TesterHandlerSamefile("samefile"),
    TesterHandlerMatch("match"),
    TesterHandlerIsRelativeTo("is_relative_to"),
]
