import sys

from trains.xclients.xclients import xclients


def main():
    host = '127.0.0.1'
    if len(sys.argv) == 3:
        host = sys.argv[2]

    rc = xclients(sys.stdin, sys.stdout, int(sys.argv[1]), host)
    sys.exit(rc)


if __name__ == '__main__':
    main()
