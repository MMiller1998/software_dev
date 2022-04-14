import socketserver
import json
from typing import IO
import c

"""
A custom TCP handler object inheriting from socketserver's StreamRequestHandler
that reverses JSON values from a TCP connection. 

It reads json from the read stream (self.rfile) and writes to the write stream
(self.wfile). Reversing functionality is implemented by a reverse method 
from assignment C.
"""
class TCPJsonReverser(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        TCPJsonReverser._read_and_write_reversed_json(self.rfile, self.wfile)

    # Reads JSON values from the given reader, reverses them, and writes
    # them to the writer
    @staticmethod
    def _read_and_write_reversed_json(reader: IO, writer: IO) -> None:
        json_input = c.get_next_json(reader)

        while json_input != "":
            writer.write(json.dumps(c.reverse_json(json_input)).encode())
            writer.write("\n".encode())
            json_input = c.get_next_json(reader)