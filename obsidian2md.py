from argparse import ArgumentParser
import contextlib
from pathlib import Path
import re
import shutil
import sys


def parse_args():
    parser = ArgumentParser(
        description=(
            "Utility script for changing obsidian image links to regular markdown"
        )
    )
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit("Not enough args!")
    parser.add_argument(
        "paths", type=Path, nargs="+", help="Single or multiple paths to markdown files"
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Perform dry run with no actual overwriting",
    )
    return parser.parse_args()


def transform_line(line: str) -> str:
    match = re.search(r"^!\[\[(.*)\]\]", line)
    if not match:
        print("[!] Could not match!")
        return line

    image_name = match.group(1)
    new_line = f"![{image_name}](images/{image_name})"
    return new_line


def convert_obsidian_to_md(path: Path) -> str:
    content = path.read_text("utf-8")
    new_content = []
    for line in content.split("\n"):
        if line.strip().startswith("![["):
            line = transform_line(line)
            print(f"Transformed: {line}")
        new_content.append(line)
    return "\n".join(new_content)


@contextlib.contextmanager
def backup_context(path):
    backup_path: Path = path.parent.joinpath(path.name + "~")
    try:
        shutil.copyfile(path, backup_path)
        yield backup_path
    except Exception as e:
        print(e)
        shutil.copyfile(backup_path, path)
    finally:
        backup_path.unlink()


def overwrite_file(path: Path, content: str) -> None:
    if path.read_text() == content:
        print("Contents are the same, doing nothing.")
        return

    with backup_context(path):
        path.write_text(content)


def main() -> int:
    path = Path("content/articles/Blogs/Software/icu-71-breaking-my-system.md")
    for path in args.paths:
        print("PROCESSING".center(50, "-"))
        print(f"{path.name}")
        content = convert_obsidian_to_md(path)
        if not args.dry_run:
            overwrite_file(path, content)
        else:
            print("Overwiten (not)")
    print("~> Done 🪄")
    return 0


if __name__ == "__main__":
    args = parse_args()
    sys.exit(main())
