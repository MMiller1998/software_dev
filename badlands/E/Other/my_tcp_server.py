import socketserver

"""
A custom TCPServer object inheriting from socketserver's TCPServer. 
This TCP server specifies timeout functionality.
"""
class MyTCPServer(socketserver.TCPServer):
    timeout = 3 # seconds

    def handle_timeout(self):
        print("Error! No data received in 3 seconds, shutting down.")