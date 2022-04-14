import sys
from trains.xmap.xmap import xmap


def main():
    """
    Invokes the ``xmap`` program with the process's STDIN, STDOUT handles
    and command-line arguments.
    """
    exit_code = xmap(sys.stdin, sys.stdout)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
