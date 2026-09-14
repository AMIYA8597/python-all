"""
# ==============================================================================
# LABORATORY: SYSTEM DESIGN (REAL-TIME SYSTEMS & PUB/SUB)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are building a live chat application like Discord, or a live stock 
# ticker. 
#
# The standard HTTP protocol is strictly "Client-Pull". The server CANNOT 
# magically send data to the client; the client MUST ask for it first.
# 
# A junior engineer implements "Short Polling". The client sends an HTTP GET 
# request every 1 second: "Any new messages?". 99% of the time, the answer is 
# "No." If you have 1 Million users, you are DDOSing your own servers with 
# 1 Million useless HTTP requests per second. The system melts.
#
# You must upgrade to Real-Time communication protocols:
# 1. Long Polling: The server holds the request open until data arrives.
# 2. Server-Sent Events (SSE): A unidirectional permanent pipeline.
# 3. WebSockets: A true bidirectional, full-duplex TCP pipeline.
#
# But how do you scale WebSockets? If User A is connected to Server 1, and 
# User B is connected to Server 2, how does Server 1 send a message to User B? 
# 
# You must introduce a Pub/Sub Event Bus (like Apache Kafka or Redis PubSub) 
# into the absolute center of your architecture!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the horrific overhead of HTTP Polling.
# - Understand WebSockets (Full Duplex).
# - Master the Pub/Sub (Publish/Subscribe) pattern for decoupled microservices.
#
# ==============================================================================
"""

import time
import threading
import queue

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. WEBSOCKETS (CONCEPTUAL DIFFERENCE)
# ==============================================================================
def demonstrate_protocols():
    section_header("Communication Protocols")
    
    print("--- 1. Short Polling (The DDOS Method) ---")
    print("Client: Any new messages? (HTTP TCP Handshake Overhead: 50ms)")
    print("Server: No.")
    print("Client: Any new messages? (HTTP TCP Handshake Overhead: 50ms)")
    print("Server: No.")
    print("Conclusion: Wastes massive CPU and bandwidth on useless handshakes.\n")
    
    print("--- 2. Long Polling (The Holding Pattern) ---")
    print("Client: Any new messages?")
    print("Server: ... (Holds the connection open for 30 seconds) ...")
    print("Server: (12 seconds later) Yes, here is a message!")
    print("Client: Any new messages?")
    print("Conclusion: Much better, but still requires a new handshake after every message.\n")
    
    print("--- 3. WebSockets (Full Duplex) ---")
    print("Client: Let's upgrade to a WebSocket! (Initial HTTP Handshake)")
    print("Server: 101 Switching Protocols. Pipeline Established!")
    print("... (Days pass, zero handshakes) ...")
    print("Server: [Instantly pushes Message 1 at 0ms latency]")
    print("Client: [Instantly pushes Message 2 at 0ms latency]")
    print("Server: [Instantly pushes Message 3 at 0ms latency]")
    print("Conclusion: True bidirectional TCP pipe. Maximum performance for Real-Time.")


# ==============================================================================
# 4. PUB/SUB ARCHITECTURE (APACHE KAFKA / REDIS PATTERN)
# ==============================================================================
class EventBus:
    """
    A central Pub/Sub message broker (like Kafka or Redis).
    It completely decouples Producers (Publishers) from Consumers (Subscribers).
    """
    def __init__(self):
        # Maps a Topic (e.g., "chat_room_general") to a list of Subscriber Queues
        self.topics = {}
        self.lock = threading.Lock()

    def subscribe(self, topic: str) -> queue.Queue:
        """A user/server connects and wants to listen to a specific topic."""
        with self.lock:
            if topic not in self.topics:
                self.topics[topic] = []
            
            # Create a dedicated mailbox (Queue) for this specific subscriber
            subscriber_mailbox = queue.Queue()
            self.topics[topic].append(subscriber_mailbox)
            return subscriber_mailbox

    def publish(self, topic: str, message: str) -> None:
        """A user/server broadcasts a message to a topic."""
        with self.lock:
            if topic in self.topics:
                # Instantly clone and drop the message into EVERY subscriber's mailbox!
                for subscriber_mailbox in self.topics[topic]:
                    subscriber_mailbox.put(message)

def run_chat_server_simulation():
    section_header("Pub/Sub Architecture (Scaling WebSockets)")
    
    bus = EventBus()
    
    # 1. Users connect to completely different physical web servers!
    print("User A connects to Web Server 1 via WebSocket.")
    print("User B connects to Web Server 2 via WebSocket.")
    
    # Both servers subscribe to the backend Event Bus for the "general_chat" topic
    mailbox_server_1 = bus.subscribe("general_chat")
    mailbox_server_2 = bus.subscribe("general_chat")
    
    # 2. User A sends a message to Server 1
    print("\nUser A sends: 'Hello everyone!' to Server 1.")
    
    # 3. Server 1 DOES NOT know how to reach Server 2! 
    # It simply PUBLISHES the message to the central Event Bus.
    print("Server 1 PUBLISHES the message to the Event Bus topic 'general_chat'.")
    bus.publish("general_chat", "[Hello everyone!] (from User A)")
    
    # 4. The Event Bus instantly fans out the message to all subscribed servers.
    msg_for_s1 = mailbox_server_1.get()
    msg_for_s2 = mailbox_server_2.get()
    
    print(f"\nServer 1 Event Loop receives: {msg_for_s1}")
    print(f"Server 2 Event Loop receives: {msg_for_s2}")
    
    print("\nServer 2 then pushes the message down User B's WebSocket!")
    print("The Pub/Sub architecture allowed 10,000 completely independent servers ")
    print("to route real-time messages without explicitly knowing about each other!")


def run_all_labs():
    demonstrate_protocols()
    run_chat_server_simulation()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is the catastrophic overhead of HTTP Short Polling?
   Answer: Every single time a client sends an HTTP GET request, it must open a TCP connection. This requires the "TCP 3-Way Handshake" (SYN, SYN-ACK, ACK), taking at least 3 network round-trips. If the site uses HTTPS (which it should), it also requires a TLS/SSL Handshake, involving heavy cryptographic CPU calculations. In Short Polling, you do this massive 50-100ms song-and-dance every 1 second, just for the server to reply with a 1-byte "No new data". If you have 1 Million users, your CPU melts purely from cryptographic handshakes, completely bringing down the application. WebSockets perform the handshake exactly *once*, leaving the raw TCP socket permanently open.

2. Explain the difference between Server-Sent Events (SSE) and WebSockets.
   Answer: WebSockets are truly Full-Duplex (Bidirectional). Both the client and the server can push binary data into the pipe at any microsecond. SSE is Half-Duplex (Unidirectional). It operates over standard HTTP. The client requests data, and the server holds the HTTP connection open, pushing a continuous stream of text chunks *down* to the client. The client cannot use that same SSE pipe to send data *up* to the server (it must use a standard HTTP POST for that). SSE is incredibly easy to set up (no custom protocols needed) and is perfect for things like Live Stock Tickers or Twitter feeds where data only flows in one direction (Server -> Client).

3. In a distributed chat system (Discord/Slack), why is a Pub/Sub engine like Redis/Kafka mandatory?
   Answer: Without Pub/Sub, you have a massive routing problem. If User A is physically connected to Server 1 (via WebSocket), and User B is connected to Server 99, how does Server 1 know where User B is? Server 1 would have to maintain a synchronized global mapping of all 10 Million users to their current physical server, and manually open a TCP connection to Server 99 to deliver the message. This creates a brittle, $O(N^2)$ web of connections. Pub/Sub completely decouples the servers. Server 1 simply tosses the message into the "Channel_5" Kafka Topic and instantly forgets about it. Server 99, which previously subscribed to "Channel_5", receives the message from Kafka and pushes it to User B. The servers remain blissfully ignorant of each other!
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: System Design (Real-Time Systems) Completed.")
