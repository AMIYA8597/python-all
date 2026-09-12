"""
Custom Multi-threaded HTTP Web Server
======================================

Overview:
---------
A professional-grade implementation of an HTTP/1.1 web server from scratch 
using Python's `socket` library. This server handles incoming TCP connections,
parses HTTP requests, routes them to specific handlers, and generates valid 
HTTP responses.

Concepts Covered:
-----------------
- Raw Network Sockets (TCP/IP).
- Multi-threading for concurrent client handling.
- String encoding/decoding (UTF-8).
- HTTP Protocol structure (Headers, Status Codes, Body).
"""

import socket
import threading
from typing import Callable, Dict, Tuple

# Type alias for Route Handlers
# A route handler takes an HTTPRequest object and returns a tuple of (status_code, content_type, body)
RouteHandler = Callable[['HTTPRequest'], Tuple[int, str, str]]


class HTTPRequest:
    """Represents a parsed HTTP request."""
    def __init__(self, raw_request: str):
        self.raw_request = raw_request
        self.method = ""
        self.path = ""
        self.protocol = ""
        self.headers: Dict[str, str] = {}
        self.body = ""
        self._parse()

    def _parse(self) -> None:
        """Parses the raw HTTP string into components."""
        if not self.raw_request:
            return

        lines = self.raw_request.split("\r\n")
        if not lines:
            return

        # Parse Request Line (e.g., GET /index.html HTTP/1.1)
        request_line = lines[0].split()
        if len(request_line) >= 3:
            self.method, self.path, self.protocol = request_line[:3]

        # Parse Headers
        header_lines = lines[1:]
        body_index = -1

        for i, line in enumerate(header_lines):
            if line == "":  # Blank line separates headers from body
                body_index = i + 1
                break
            if ":" in line:
                key, value = line.split(":", 1)
                self.headers[key.strip()] = value.strip()

        # Extract Body if present
        if body_index != -1 and body_index < len(header_lines):
            self.body = "\r\n".join(header_lines[body_index:])


class HTTPServer:
    def __init__(self, host: str = '127.0.0.1', port: int = 8080):
        self.host = host
        self.port = port
        self.routes: Dict[str, RouteHandler] = {}
        # Create a TCP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow immediate reuse of the port after server restarts
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def route(self, path: str):
        """Decorator to register a route handler."""
        def decorator(handler: RouteHandler) -> RouteHandler:
            self.routes[path] = handler
            return handler
        return decorator

    def start(self) -> None:
        """Binds the socket and starts listening for connections."""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[*] Server listening on http://{self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"[+] Accepted connection from {client_address}")
                # Dispatch client to a new thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket,)
                )
                client_thread.start()
        except KeyboardInterrupt:
            print("\n[*] Shutting down server.")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket: socket.socket) -> None:
        """Reads client data, processes the request, and sends a response."""
        try:
            # Read data from the socket
            request_data = client_socket.recv(4096).decode('utf-8')
            if not request_data:
                return

            # Parse Request
            request = HTTPRequest(request_data)
            print(f"[{request.method}] {request.path}")

            # Routing Logic
            handler = self.routes.get(request.path)
            if handler:
                try:
                    status_code, content_type, body = handler(request)
                    response = self.build_response(status_code, content_type, body)
                except Exception as e:
                    response = self.build_response(500, "text/plain", f"Internal Server Error: {e}")
            else:
                response = self.build_response(404, "text/plain", "404 Not Found")

            # Send Response
            client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"[-] Error handling client: {e}")
        finally:
            client_socket.close()

    def build_response(self, status_code: int, content_type: str, body: str) -> str:
        """Constructs a valid HTTP response string."""
        status_messages = {
            200: "OK",
            404: "Not Found",
            500: "Internal Server Error"
        }
        status_text = status_messages.get(status_code, "Unknown")
        
        response = f"HTTP/1.1 {status_code} {status_text}\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(body)}\r\n"
        response += "Connection: close\r\n\r\n"
        response += body
        return response


# ---------------------------------------------------------
# Application Code (Using the Framework)
# ---------------------------------------------------------
if __name__ == "__main__":
    app = HTTPServer(host="127.0.0.1", port=8000)

    @app.route("/")
    def index(req: HTTPRequest) -> Tuple[int, str, str]:
        html = """
        <html>
            <head><title>Home</title></head>
            <body>
                <h1>Welcome to Custom Web Server!</h1>
                <p>Built entirely from scratch in Python.</p>
            </body>
        </html>
        """
        return 200, "text/html", html

    @app.route("/api/ping")
    def ping(req: HTTPRequest) -> Tuple[int, str, str]:
        return 200, "application/json", '{"status": "success", "message": "pong"}'

    # Start the server (Uncomment to run)
    print("Run `curl http://127.0.0.1:8000/` or visit in browser after starting.")
    # app.start()
