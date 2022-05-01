import sys
from argparse import ArgumentParser
import shlex
import subprocess


DWLD_CMD = "rsync -rtvzP syb:/var/www/blog/ /home/cny/Projects/blog.syberu.xyz/blog"
UPLD_CMD = "rsync -rtvzP /home/cny/Projects/blog.syberu.xyz/blog/ syb:/var/www/blog"


def execute(cmd: str):
    print(f"Executing: {cmd}")
    cmd = shlex.split(cmd)
    if not args.dry_run:
        out = subprocess.check_output(cmd)
        out = out.decode("utf-8")
        print(out)
    else:
        print("~> Dry run complete!")


def parse_args():
    parser = ArgumentParser(
        description="Remote management utility for syncing `blog.syberu.xyz`"
    )
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit("Not enough args")

    parser.add_argument("-d", "--dry-run", action="store_true")
    action = parser.add_subparsers(dest="action")
    action.add_parser("down")
    action.add_parser("up")
    return parser.parse_args()


def main():
    print("SYNCER".center(60, "-"))
    match args.action:
        case "down":
            execute(DWLD_CMD)
        case "up":
            execute(UPLD_CMD)
    return 0


if __name__ == "__main__":
    args = parse_args()
    sys.exit(main())
