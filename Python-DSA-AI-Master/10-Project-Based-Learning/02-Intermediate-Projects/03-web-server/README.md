# Build Your Own HTTP Web Server from Scratch

## 1. Overview
This module explores one of the most fundamental systems in modern software: **The HTTP Web Server**. 
Instead of relying on heavy frameworks like Django, Flask, or FastAPI, we will build a low-level, multithreaded HTTP server using raw TCP sockets in Python.

## 2. Why This Exists & Industry Use Cases
Web servers are the backbone of the internet. Tools like Nginx, Apache, and Gunicorn use the exact concepts we are building here. 
Understanding how raw bytes sent over a network translate into web pages (HTML, JSON, Images) is crucial for:
- **Backend Engineers:** To optimize network bottlenecks and handle custom protocols.
- **Cybersecurity Professionals:** To understand HTTP vulnerabilities like Header Injection and Slowloris attacks.
- **System Architects:** To build reverse proxies, load balancers, or lightweight IoT servers.

## 3. Beginner Explanation
Imagine a restaurant. 
- You (the **Client / Browser**) sit down and look at the menu.
- You give your order (an **HTTP Request**) to the waiter.
- The waiter (our **Web Server**) takes your order to the kitchen, prepares the food, and brings it back to you on a plate (an **HTTP Response**).

In the digital world:
- Your order is a block of text requesting a specific page (e.g., "Give me /index.html").
- The server reads this text, finds the file on its hard drive, and sends it back to you.

## 4. Deep Technical Explanation
HTTP (Hypertext Transfer Protocol) operates over TCP/IP. 
Our Python application will:
1. Create a **Socket** bound to a specific IP (`127.0.0.1`) and Port (`8080`).
2. Listen for incoming TCP connections.
3. Accept connections and spawn a new **Thread** for each client to handle concurrency.
4. Read the raw socket data stream to extract the HTTP Request.
5. Parse the Request Line (Method, URI, Version) and Headers.
6. Generate a strictly formatted HTTP Response.
7. Send the response bytes back over the socket and gracefully close the connection.

### HTTP Request Format
```http
GET /hello HTTP/1.1
Host: localhost:8080
User-Agent: curl/7.68.0
Accept: */*

```

### HTTP Response Format
```http
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 13

Hello, World!
```

## 5. Implementation Roadmap
The `main.py` file contains the complete server implementation. It features:
- `HTTPServer` class for managing the socket lifecycle.
- `HTTPRequest` class for parsing raw bytes into a manageable object.
- Routing mechanism to map URIs to specific handler functions.
- Concurrency utilizing the `threading` module to prevent blocking I/O operations.

## 6. Interview Questions & Exercises
### Questions
1. **Q:** What is the difference between TCP and HTTP?
   **A:** TCP is a transport layer protocol ensuring reliable delivery of data packets. HTTP is an application layer protocol that defines the structure and semantics of the data being transmitted over TCP.
2. **Q:** Why did we use multithreading for the web server instead of a single loop?
   **A:** A single-threaded server blocks while waiting for network I/O or processing a request. Multithreading allows simultaneous processing of multiple clients, heavily increasing throughput.

### Exercises
- **Add POST Support:** Modify the server to parse a body payload for POST requests.
- **File Serving:** Write a route handler that reads static files (HTML/CSS) from a folder and sends them back with the correct `Content-Type` header.
- **Implement Keep-Alive:** Instead of closing the socket after one request, parse the `Connection: keep-alive` header and reuse the socket.
