import sys

from trains.xstrategy.xstrategy import xstrategy


def main():
    rc = xstrategy(sys.stdin, sys.stdout)
    sys.exit(rc)


if __name__ == '__main__':
    main()
