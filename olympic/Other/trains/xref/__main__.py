import sys

from trains.xref.xref import xref


def main():
    rc = xref(sys.stdin, sys.stdout)
    sys.exit(rc)


if __name__ == '__main__':
    main()
