"""
# ==============================================================================
# LABORATORY: PROJECT-BASED LEARNING (RAW HTTP WEB SERVER)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer uses `Flask` to build a web application. They type 
# `@app.route('/home')` and return a string. They believe that 'Flask' is 
# magically teleporting the string to the user's browser. They have no idea 
# what a Socket is, what a TCP Port is, or what the HTTP Protocol looks like.
# When a production server drops TCP packets, they are mathematically incapable 
# of debugging the issue.
#
# A senior network architect builds a raw Web Server from scratch. They import 
# the low-level OS `socket` library. They bind a mathematical port, listen for 
# binary TCP byte streams, manually parse the raw HTTP Headers (`GET /home HTTP/1.1`), 
# and mathematically format the `200 OK` response. They understand the Internet 
# is nothing more than raw text sent over copper wires.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master OS-level TCP Sockets (Bind, Listen, Accept, Receive, Send).
# - Execute raw HTTP Protocol Parsing (Headers, Body, Status Codes).
# - Understand Multi-Threading for concurrent network requests.
#
# ==============================================================================
"""

import socket
import threading
import time

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE PROTOCOL PARSER (HTTP)
# ==============================================================================
class HTTPParser:
    """
    The Internet is just text!
    This class mathematically parses raw byte strings into HTTP components.
    """
    @staticmethod
    def parse_request(raw_request: str) -> dict:
        # HTTP separates lines with Carriage Return Line Feed (\r\n)
        lines = raw_request.split("\r\n")
        
        # The absolute first line is ALWAYS the Request Line (e.g., "GET /about HTTP/1.1")
        request_line = lines[0]
        method, path, protocol = request_line.split(" ")
        
        return {
            "method": method,
            "path": path,
            "protocol": protocol
        }
        
    @staticmethod
    def build_response(status_code: str, body: str) -> bytes:
        """
        Mathematically constructs a flawless HTTP Response.
        If you miss a single \r\n, the user's browser will violently crash!
        """
        # 1. The Status Line (e.g., "HTTP/1.1 200 OK")
        response = f"HTTP/1.1 {status_code}\r\n"
        
        # 2. The Headers (We must mathematically declare the Content-Type and Length!)
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(body)}\r\n"
        
        # 3. The BLANK LINE (This mathematically tells the browser: HEADERS ARE DONE!)
        response += "\r\n"
        
        # 4. The actual HTML Payload
        response += body
        
        # The OS Socket requires raw binary bytes, not Python Strings!
        return response.encode('utf-8')


# ==============================================================================
# 4. THE OS SOCKET ENGINE (THE SERVER)
# ==============================================================================
class RawWebServer:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.is_running = True
        
        # We ask the Operating System for a raw IPv4 (AF_INET), TCP (SOCK_STREAM) Socket!
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Allow the OS to instantly reuse the port if the server crashes (SO_REUSEADDR)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        # 1. BIND: We mathematically chain our Socket to Port 8080.
        self.server_socket.bind((self.host, self.port))
        
        # 2. LISTEN: We tell the OS to start queuing incoming connections!
        self.server_socket.listen(5)
        print(f"  [BOOT] Server listening on http://{self.host}:{self.port} ...")
        
        # We run the accept loop in a background thread to prevent blocking the lab!
        accept_thread = threading.Thread(target=self._accept_connections, daemon=True)
        accept_thread.start()

    def _accept_connections(self):
        """The Infinite Network Loop."""
        while self.is_running:
            try:
                # 3. ACCEPT: The thread mathematically freezes here until a browser connects!
                client_socket, client_address = self.server_socket.accept()
                
                # To prevent a slow client from freezing the entire server, 
                # we immediately spawn a NEW thread to handle the request!
                client_thread = threading.Thread(
                    target=self._handle_client, 
                    args=(client_socket, client_address),
                    daemon=True
                )
                client_thread.start()
            except OSError:
                break # Socket was closed cleanly

    def _handle_client(self, client_socket: socket.socket, client_address: tuple):
        """The Business Logic Pipeline."""
        try:
            # 4. RECEIVE: We read the raw binary TCP packets from the OS Buffer (up to 1024 bytes)
            raw_data = client_socket.recv(1024).decode('utf-8')
            
            if not raw_data:
                return
                
            # Mathematically parse the HTTP Protocol
            request = HTTPParser.parse_request(raw_data)
            
            # The Router!
            if request["path"] == "/":
                html = "<h1>Welcome to the Raw Web Server!</h1><p>TCP Sockets are awesome.</p>"
                response_bytes = HTTPParser.build_response("200 OK", html)
            elif request["path"] == "/about":
                html = "<h1>About Us</h1><p>We build everything from scratch.</p>"
                response_bytes = HTTPParser.build_response("200 OK", html)
            else:
                html = "<h1>404 Not Found</h1><p>The requested route does not exist.</p>"
                response_bytes = HTTPParser.build_response("404 NOT FOUND", html)
                
            # 5. SEND: We blast the binary bytes back through the copper wires!
            client_socket.sendall(response_bytes)
            
        except Exception as e:
            print(f"  [ERROR] Client connection failed: {e}")
        finally:
            # 6. CLOSE: We mathematically sever the TCP Connection.
            client_socket.close()

    def stop(self):
        self.is_running = False
        self.server_socket.close()
        print("  [SHUTDOWN] Server cleanly terminated.")


# ==============================================================================
# 5. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_server():
    section_header("Project: Raw HTTP Web Server")
    
    server = RawWebServer()
    server.start()
    
    # We simulate a Browser by acting as a raw TCP Client!
    time.sleep(0.5) # Give the server a millisecond to boot
    
    print("\n  [SIMULATION] Spawning a virtual browser to hit '/'...")
    # We create a dummy client socket to test our server!
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))
    
    # We manually blast a raw HTTP GET request!
    client.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
    
    # We await the server's response!
    server_response = client.recv(4096).decode('utf-8')
    client.close()
    
    print("  [SERVER RESPONSE PAYLOAD]")
    # We split it to show the headers and the body clearly
    headers, body = server_response.split("\r\n\r\n")
    print(f"    [HEADERS]\n{headers}")
    print(f"    [BODY]\n{body}")
    
    server.stop()


def run_all_labs():
    demonstrate_server()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why did we use `threading.Thread` to handle the `client_socket` immediately after executing `server_socket.accept()`? Why not just handle the data right there in the main loop?"
   Senior Answer: "Head-of-Line Blocking and Concurrency. `socket.recv(1024)` is a mathematically 'Blocking' network call. If a malicious user connects to the server but intentionally delays sending any data for $10$ seconds, the main `while` loop will completely freeze on the `recv()` line. During those $10$ seconds, if $5,000$ legitimate users try to connect, the server will ignore them all because the main loop cannot reach the `accept()` function again. By instantly spawning a background Thread (or utilizing AsyncIO), the slow user blocks their *own* isolated thread, while the main engine instantly loops back to `accept()`, mathematically guaranteeing that the server can accept thousands of concurrent TCP connections."

2. Interviewer: "What is the architectural significance of the double `\\r\\n\\r\\n` sequence in the HTTP Protocol?"
   Senior Answer: "It is the Protocol Delimiter. A Web Browser has absolutely no way of knowing when the Server's HTTP Headers stop and the actual HTML payload begins. The HTTP Protocol mathematically mandates that every single Header is separated by a Carriage Return Line Feed (`\\r\\n`). When the Headers are completely finished, the Server must send a blank line (a second `\\r\\n`). The exact millisecond the Browser's parser detects `\\r\\n\\r\\n`, it stops parsing configuration metadata and physically shifts its internal state to start rendering the visual HTML DOM on the user's screen."

3. Interviewer: "If we want to stream a massive $50$ GB Video File to the user, we obviously cannot load it into RAM and set the `Content-Length: 50000000000`. How does the HTTP Protocol handle massive streams of unknown length?"
   Senior Answer: "Chunked Transfer Encoding. Instead of calculating the absolute file size and sending a `Content-Length` header, the server sends the header `Transfer-Encoding: chunked`. This mathematically alters the HTTP protocol. The server reads the $50$ GB file from the hard drive in tiny $8$ KB chunks. It calculates the hexadecimal length of that specific chunk, sends the hex length over the socket, followed by the $8$ KB binary payload, and repeats this loop continuously. The browser renders the video frame by frame as it arrives. When the file finishes, the server sends a chunk length of `0`, mathematically signaling the browser that the TCP stream is successfully complete without ever exhausting the server's RAM."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Capstone Project (Raw Web Server) Completed.")
