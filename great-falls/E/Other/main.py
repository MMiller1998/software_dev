import sys
from typing import List
from tcp_json_reverser import TCPJsonReverser
from my_tcp_server import MyTCPServer


LOCALHOST = "127.0.0.1"
DEFAULT_PORT = 45678


# Main function that starts the TCP listener with the given port
def main() -> None:
    host, port = LOCALHOST, get_port(sys.argv)

    with MyTCPServer((host, port), TCPJsonReverser) as server:
        server.handle_request()


# Gets port from passed in args - if port is not specified, return default port
def get_port(args: List[str]) -> int:
    port = DEFAULT_PORT
    if len(args) == 2:
        port = args[1]

    return int(port)


if __name__ == "__main__":
    main()
