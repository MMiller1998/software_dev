import sys

from trains.xmanager.xmanager import xmanager


def main():
    rc = xmanager(sys.stdin, sys.stdout)
    sys.exit(rc)


if __name__ == '__main__':
    main()
