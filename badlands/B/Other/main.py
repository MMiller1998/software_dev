import sys


def parse_args(args):
    lines_input = args[1]

    lines_str = lines_input[1:]
    lines = int(lines_str)

    if len(args) != 2 or lines_input[0] != "-" or not lines_str[0].isnumeric() or lines < 0:
        raise ValueError("Bad input")

    return lines

if __name__ == '__main__':
    try:
        args = sys.argv
        lines = parse_args(args)

        for line in sys.stdin:
            if lines <= 0:
                break

            print(line.rstrip("\n"))
            lines -= 1
    except (IndexError, ValueError):
        print("\"error\"")
        exit(1)
