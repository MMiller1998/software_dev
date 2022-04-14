import sys

from trains.xserver.xserver import xserver


def main():
    rc = xserver(sys.stdin, sys.stdout, int(sys.argv[1]))
    sys.exit(rc)


if __name__ == '__main__':
    main()
