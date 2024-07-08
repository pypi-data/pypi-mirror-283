import argparse
from pathlib import Path

from .Handler import Handler

class PropertyHandlerSimple(Handler):
    def impl_call(self, path: Path, args: argparse.Namespace):
        print(self.get_path_attr(path))

class PropertyHandlerIterable(Handler):
    def impl_call(self, path: Path, args: argparse.Namespace):
        for line in self.get_path_attr(path):
            print(line)

class PropertyHandlerIterableJoinable(PropertyHandlerIterable):
    def add_args(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        parser = super().add_args(subparsers)
        parser.add_argument("--join", "-j", action = "store_true", help = "Concatenate suffixes eg return '.tar.gz' as one")

    def impl_call(self, path: Path, args: argparse.Namespace):
        if not args.join:
            return super().impl_call(path, args)

        print("".join(self.get_path_attr(path)))

class CallableHandlerSimple(PropertyHandlerSimple):
    def impl_call(self, path: Path, args: argparse.Namespace, *attr_args, **attr_kwargs):
        print(self.get_path_attr(path)(*attr_args, **attr_kwargs))

class CallableHandlerSimplePathless(CallableHandlerSimple):
    def __init__(self, path_attr_name: str) -> None:
        super().__init__(path_attr_name, add_path_arg = False)

    def __call__(self, path: Path | None, args: argparse.Namespace) -> str:
        path = Path(".") # why make life difficult?
        return super().__call__(path, args)

class CallableHandlerResolve(CallableHandlerSimple):
    def add_args(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        parser = super().add_args(subparsers)
        parser.add_argument("--strict", action = "store_true")

    def impl_call(self, path: Path, args: argparse.Namespace):
        return super().impl_call(path, args, strict = args.strict)

class CallableHandlerWithName(CallableHandlerSimple):
    def add_args(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        parser = super().add_args(subparsers)
        parser.add_argument("name")

    def impl_call(self, path: Path, args: argparse.Namespace):
        return super().impl_call(path, args, args.name)

class CallableHandlerWithStem(CallableHandlerSimple):
    def add_args(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        parser = super().add_args(subparsers)
        parser.add_argument("stem")

    def impl_call(self, path: Path, args: argparse.Namespace):
        return super().impl_call(path, args, args.stem)

class CallableHandlerWithSuffix(CallableHandlerSimple):
    def add_args(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        parser = super().add_args(subparsers)
        parser.add_argument("suffix")

    def impl_call(self, path: Path, args: argparse.Namespace):
        return super().impl_call(path, args, args.suffix)

class CallableHandlerWithSegments(CallableHandlerSimple):
    def add_args(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        parser = super().add_args(subparsers)
        parser.add_argument("segments", nargs = "*")

    def impl_call(self, path: Path, args: argparse.Namespace):
        return super().impl_call(path, args, *args.segments)

class CallableHandlerRelativeTo(CallableHandlerSimple):
    def add_args(self, subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
        parser = super().add_args(subparsers)
        parser.add_argument("other")
        parser.add_argument("--walk-up", action = "store_true")

    def impl_call(self, path: Path, args: argparse.Namespace):
        return super().impl_call(path, args, args.other, walk_up = args.walk_up)

handlers = [
    PropertyHandlerSimple("drive"),
    PropertyHandlerSimple("root"),
    PropertyHandlerSimple("anchor"),
    PropertyHandlerSimple("name"),
    PropertyHandlerSimple("stem"),
    PropertyHandlerSimple("suffix"),
    PropertyHandlerIterableJoinable("suffixes"),
    PropertyHandlerSimple("parent"),
    PropertyHandlerIterable("parents"),
    PropertyHandlerIterable("parts"),

    CallableHandlerSimplePathless("cwd"),  # pwd -P
    CallableHandlerSimplePathless("home"), # echo $HOME

    # in Python 3.13 these accept follow_symlinks
    # https://github.com/python/cpython/issues/103363
    # TODO add that option eventually in a way that doesn't break compatibility
    CallableHandlerSimple("owner"), # stat -c %U
    CallableHandlerSimple("group"), # stat -c %G

    CallableHandlerSimple("as_uri"),
    CallableHandlerSimple("as_posix"),
    CallableHandlerSimple("expanduser"),
    CallableHandlerSimple("readlink"),
    CallableHandlerSimple("absolute"),
    CallableHandlerResolve("resolve"),

    CallableHandlerWithName("with_name"),
    CallableHandlerWithStem("with_stem"),
    CallableHandlerWithSuffix("with_suffix"),
    CallableHandlerWithSegments("with_segments"), # the path argument of this one seems a bit weird
    CallableHandlerRelativeTo("relative_to"),
]
