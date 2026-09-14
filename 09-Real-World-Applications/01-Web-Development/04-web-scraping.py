"""
# ==============================================================================
# LABORATORY: REAL-WORLD APPLICATIONS (WEB SCRAPING & AUTOMATION)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A massive Fortune 500 company needs to aggregate pricing data from 50 competitors 
# daily. The competitors do not have an API. 
#
# A junior engineer hires 10 interns to manually click on websites and copy-paste 
# prices into an Excel sheet, costing $500,000 a year and generating massive 
# human error.
#
# A senior engineer writes a 50-line Python script using `requests` and `BeautifulSoup`. 
# It runs silently on a Cron job at 3:00 AM, programmatically downloading the HTML, 
# mathematically extracting the CSS nodes containing the prices, and dumping the 
# flawless data into a PostgreSQL database in 4 seconds.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master HTTP Requests (Headers, User-Agents, Proxies).
# - Master the DOM (Document Object Model) and CSS Selectors.
# - Differentiate between Static HTML Scraping and Dynamic JS Execution.
#
# ==============================================================================
"""

import time
import requests
# We gracefully handle missing dependencies!
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. HTTP HEADERS & RATE LIMIT EVASION
# ==============================================================================
# If you simply run `requests.get('https://amazon.com')`, the target server 
# mathematically analyzes the incoming HTTP headers. It sees:
# `User-Agent: python-requests/2.28.1`
# The WAF (Web Application Firewall) instantly triggers an IP Ban.

def demonstrate_http_headers():
    section_header("Bypassing Basic WAFs (User-Agent Spoofing)")
    
    print("  [SCENARIO] We are attempting to scrape a secure endpoint.")
    
    # 1. The Naive Request
    print("\n  [NAIVE REQUEST]")
    print("    headers = {}")
    print("    response = requests.get('https://example.com/api', headers=headers)")
    print("    -> Result: 403 FORBIDDEN (WAF Blocked!)")
    
    # 2. The Spoofed Request
    # We mathematically forge the HTTP Headers to exactly match a real Google 
    # Chrome browser running on Windows 10.
    professional_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    
    print("\n  [PROFESSIONAL REQUEST]")
    print(f"    headers = {professional_headers['User-Agent'][:40]}...")
    print("    response = requests.get('https://example.com/api', headers=headers)")
    print("    -> Result: 200 OK (WAF Bypassed!)")


# ==============================================================================
# 4. PARSING THE DOM (BEAUTIFUL SOUP)
# ==============================================================================
def demonstrate_dom_parsing():
    section_header("Extracting Data from the DOM (BeautifulSoup)")
    
    if not HAS_BS4:
        print("  [ERROR] BeautifulSoup4 is not installed. Run `pip install beautifulsoup4`.")
        return
        
    # We will simulate an HTTP response containing raw HTML!
    raw_html = """
    <html>
        <head><title>E-Commerce Store</title></head>
        <body>
            <div id="product-list">
                <div class="card product-card">
                    <h2 class="title">Quantum Keyboard</h2>
                    <span class="price">$199.99</span>
                    <p class="stock in-stock">In Stock (42 units)</p>
                </div>
                <div class="card product-card">
                    <h2 class="title">Optical Mouse</h2>
                    <span class="price">$49.99</span>
                    <p class="stock out-of-stock">Out of Stock</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    print("  [INIT] Loading HTML payload into the DOM Parser...")
    
    # The parser mathematically converts the raw string into a traversable Tree (AST)!
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    print("\n  [TASK 1: Extract the Page Title]")
    # We navigate the DOM nodes directly!
    title = soup.title.text
    print(f"    -> {title}")
    
    print("\n  [TASK 2: Extract all Product Prices]")
    # CSS SELECTORS! We instruct the C-level parser to find all span tags with class 'price'.
    # This is mathematically equivalent to `document.querySelectorAll('.price')` in JS.
    product_cards = soup.find_all('div', class_='product-card')
    
    total_value = 0.0
    for card in product_cards:
        # We search *within* the specific node!
        name = card.find('h2', class_='title').text
        price_str = card.find('span', class_='price').text
        stock_status = card.find('p', class_='stock').text
        
        # Data Cleaning! Strip the '$' and convert to Float for mathematical analysis.
        price_float = float(price_str.replace('$', ''))
        
        print(f"    -> Product: {name:<20} | Price: ${price_float:<7.2f} | Status: {stock_status}")
        total_value += price_float
        
    print(f"\n  [ANALYSIS] Total Store Value: ${total_value:.2f}")


def run_all_labs():
    demonstrate_http_headers()
    demonstrate_dom_parsing()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "What is the difference between scraping with `requests` + `BeautifulSoup`, versus using a tool like `Selenium` or `Playwright`?"
   Senior Answer: "`requests` simply opens a TCP socket, downloads the raw HTML file from the server, and closes the connection. It is mathematically instant ($0.05$ seconds). However, modern web frameworks (React, Vue, Angular) often return a blank HTML file containing only a massive JavaScript bundle. If you use `BeautifulSoup` to parse a React app, it finds absolutely zero data, because the data doesn't exist yet! Tools like `Selenium` and `Playwright` boot up an actual, physical instance of Google Chrome (a headless browser). They download the HTML, execute the JavaScript V8 engine, wait for the JS to dynamically render the DOM, and *then* extract the data. While they can scrape anything, booting a physical browser requires Gigabytes of RAM and takes $5.0+$ seconds per page, completely destroying extraction throughput."

2. Interviewer: "How do large-scale web scrapers prevent their IP addresses from being permanently banned by Cloudflare or AWS WAF?"
   Senior Answer: "Spoofing the `User-Agent` is only step one. WAFs deploy mathematical rate-limiting (e.g., detecting if a single IP address requests 50 pages in 1 second). To scale horizontally, professional scrapers route their TCP packets through Rotating Proxy Networks. A proxy pool intercepts the Python script's outbound request and mathematically funnels it through thousands of different IP addresses worldwide (often residential IPs). The target WAF perceives the attack as 10,000 distinct human beings browsing the site slowly, perfectly masking the single Python script executing the logic."

3. Interviewer: "If an E-Commerce site is rendered using React (making BeautifulSoup useless), how can you extract the data without resorting to a slow Selenium browser?"
   Senior Answer: "Reverse Engineering the API. Even though React renders the data dynamically in the browser, the React code must physically retrieve that data from somewhere! By opening the Chrome Network DevTools (XHR/Fetch tab), you can mathematically trace the exact hidden JSON API endpoint that the React frontend is querying (e.g., `https://api.store.com/v1/products`). You completely bypass the HTML, bypass React, bypass Selenium, and simply execute a raw `requests.get()` directly against their hidden API endpoint, extracting flawless, pre-formatted JSON data at lightning speed."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Web Development (Scraping) Completed.")
