"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (EMAIL AUTOMATION & SMTP)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior engineer is tasked with sending a personalized welcome email to 
# 5,000 new users. They try to write a script that opens the Gmail web browser, 
# clicks "Compose", types the message, and clicks "Send" using Selenium. It 
# takes 14 hours to execute and constantly crashes when the HTML layout changes.
#
# A senior engineer understands the "SMTP Protocol". They completely bypass 
# the web browser. They write a 20-line Python script that opens a direct, 
# mathematically secure TLS socket to `smtp.gmail.com` on Port 587. They construct 
# a pure MIME-encoded payload (allowing HTML and attachments) and transmit 
# 5,000 flawless, mathematically customized emails in exactly 45 seconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the Simple Mail Transfer Protocol (SMTP) architecture.
# - Understand Multipurpose Internet Mail Extensions (MIME) for attachments.
# - Execute Secure Socket Layer (SSL/TLS) email transmission.
#
# ==============================================================================
"""

import smtplib
import os
import time
from email.message import EmailMessage

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. CONSTRUCTING THE MIME PAYLOAD
# ==============================================================================
# You cannot simply send a raw Python string over SMTP if you want formatting!
# Email servers mathematically require a specific format called MIME.
# It defines boundaries, character sets (UTF-8), and content types (text/html).

def construct_professional_email(target_email: str, user_name: str) -> EmailMessage:
    """Builds a mathematically sound MIME object containing HTML."""
    
    # 1. Initialize the MIME structure
    msg = EmailMessage()
    
    # 2. Set the routing Headers
    # Note: `os.getenv` prevents hardcoding passwords in GitHub!
    msg['Subject'] = f"Welcome to the Platform, {user_name}!"
    msg['From'] = os.getenv("EMAIL_USER", "corporate_bot@example.com")
    msg['To'] = target_email
    
    # 3. Inject the HTML Payload!
    # Instead of boring plain text, we inject mathematical HTML/CSS.
    html_content = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
                .container {{ background-color: #ffffff; padding: 20px; border-radius: 5px; }}
                .header {{ color: #2c3e50; }}
                .btn {{ background-color: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2 class="header">Hello, {user_name}!</h2>
                <p>We are mathematically thrilled to have you on board.</p>
                <p>Your account has been fully provisioned on our AWS servers.</p>
                <br>
                <a href="https://example.com/login" class="btn">Access Dashboard</a>
            </div>
        </body>
    </html>
    """
    
    # We specify that the content is HTML, so the email client renders it!
    msg.set_content(html_content, subtype='html')
    
    return msg


# ==============================================================================
# 4. THE SMTP TRANSMISSION PIPELINE
# ==============================================================================
def transmit_email(msg: EmailMessage):
    """
    Physically connects to the Email Server and transmits the MIME bytes.
    Note: To use Gmail, you must generate an "App Password" in Google Account settings.
    """
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD") # NEVER hardcode this!
    
    if not EMAIL_USER or not EMAIL_PASSWORD:
        print("    -> [SIMULATION MODE] Missing EMAIL_USER / EMAIL_PASSWORD in environment.")
        print("    -> Simulating TLS connection to smtp.gmail.com:587...")
        time.sleep(0.5)
        print("    -> [250 OK] Email successfully transmitted to MTA (Mail Transfer Agent)!")
        return

    # If the credentials exist, execute the real transmission!
    try:
        print("    -> Opening TCP socket to smtp.gmail.com on Port 587...")
        # Port 587 is the standard for STARTTLS (Secure submission)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        
        # We mathematically encrypt the socket! (STARTTLS)
        server.starttls()
        
        print("    -> Authenticating with SMTP Server...")
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        
        print("    -> Transmitting MIME bytes...")
        server.send_message(msg)
        
        # Cleanly sever the TCP connection
        server.quit()
        print("    -> [250 OK] Email successfully transmitted!")
        
    except Exception as e:
        print(f"    -> [ERROR] Transmission failed: {e}")


# ==============================================================================
# 5. MATHEMATICAL PROOF OF EXECUTION
# ==============================================================================
def demonstrate_email_automation():
    section_header("Email Automation: SMTP and MIME Architecture")
    
    print("  [SCENARIO] Sending customized HTML welcome emails to a user database.")
    
    user_database = [
        {"name": "Alice Turing", "email": "alice@example.com"},
        {"name": "Bob Dijkstra", "email": "bob@example.com"},
    ]
    
    start_time = time.time()
    
    for user in user_database:
        print(f"\n  [PROCESSING] Generating email for {user['email']}...")
        
        # Step 1: Mathematical MIME construction
        mime_payload = construct_professional_email(user["email"], user["name"])
        
        # Step 2: SMTP Transmission
        transmit_email(mime_payload)
        
    end_time = time.time()
    print(f"\n  [SUCCESS] Processed {len(user_database)} emails in {end_time - start_time:.2f} seconds.")


def run_all_labs():
    demonstrate_email_automation()


# ==============================================================================
# 6. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why can't we use Port 25 for sending emails in a modern Python script?"
   Senior Answer: "Port $25$ is the original, unencrypted Port for SMTP (created in $1982$). If you transmit an email containing passwords or confidential data over Port $25$, the data travels as plain text. Any router between your Python script and the Gmail server can mathematically execute a 'Man-in-the-Middle' packet sniffing attack and read the entire email. Modern architecture mandates Port $587$ (STARTTLS) or Port $465$ (Implicit SSL). When you call `server.starttls()`, Python mathematically negotiates a cryptographic handshake with the server, upgrading the plain-text TCP socket into a heavily encrypted tunnel. Even if a hacker intercepts the packets, they only receive indecipherable mathematical noise."

2. Interviewer: "What is the architectural purpose of the MIME standard (`EmailMessage`) when Python can simply send strings?"
   Senior Answer: "The SMTP protocol only understands $7$-bit ASCII characters. If you attempt to send an emoji, a Japanese character, a PDF attachment, or HTML formatting using raw SMTP strings, the protocol will mathematically crash. MIME (Multipurpose Internet Mail Extensions) solves this by mathematically encoding complex data (like a binary PDF) into a massive string of ASCII text using Base64 encoding. It injects specific Headers (like `Content-Type: text/html` or `Content-Disposition: attachment`) into the payload. When the user's Gmail client receives the email, it mathematically parses the MIME boundaries, decodes the Base64 back into a PDF, and renders the HTML perfectly."

3. Interviewer: "A junior developer puts the `server.login()` command inside the `for` loop, authenticating 5,000 times for 5,000 users. Why is this catastrophic?"
   Senior Answer: "Cryptographic handshakes and database authentications are mathematically expensive. If you place `server.login()` inside the loop, the script opens a TCP socket, negotiates TLS encryption, authenticates against Google's massive backend, sends exactly $1$ email, severs the socket, and then repeats the entire process $4,999$ more times. This takes hours and will trigger an immediate DDoS ban from Google's firewall. A Senior Engineer places `server.login()` *outside* the loop. They negotiate the secure socket exactly once, blast all $5,000$ emails through the established tunnel using `server.send_message(msg)` inside the loop, and close the socket once at the end. This collapses the execution time from hours to seconds."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Automation (Email / SMTP) Completed.")
