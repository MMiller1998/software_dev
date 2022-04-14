import sys

from trains.xlegal.xlegal import xlegal


def main():
    rc = xlegal(sys.stdin, sys.stdout)
    sys.exit(rc)


if __name__ == '__main__':
    main()
