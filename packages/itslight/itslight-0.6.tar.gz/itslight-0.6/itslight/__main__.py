import sys

from .download import download, get_config


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        print("usage: itslight <command>")
        return

    if args[0] in {"i", "install", "download"}:
        if len(args) < 2:
            print("usage: itslight i <repo>")
            exit(0)

        download("\n".join(args[1:]))


if __name__ == "__main__":
    main()
