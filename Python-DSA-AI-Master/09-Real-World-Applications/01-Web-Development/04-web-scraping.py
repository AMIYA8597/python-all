"""
Web Scraping: Automating Data Extraction from the Web

Learning Objectives:
1. Understand the fundamentals of HTTP requests and HTML parsing.
2. Master tools like `requests` and `BeautifulSoup` (concepts mocked using standard libraries).
3. Learn advanced concepts: handling pagination, dynamic content, and anti-scraping mechanisms.
4. Professional implementation adhering to ethical scraping rules.

Concept Explanation:
Web scraping is the automated process of extracting data from websites. It involves making an HTTP request to a URL, retrieving the HTML content, parsing it, and extracting the desired information.
Industry use cases include:
- Price monitoring and competitor analysis for e-commerce.
- Lead generation and contact extraction.
- Data collection for Machine Learning models (e.g., NLP datasets).
- News aggregation and social media sentiment analysis.

Ethical Considerations (Important):
1. Always check `robots.txt` before scraping.
2. Do not overload servers; implement rate limiting (`time.sleep()`).
3. Identify your scraper via a custom `User-Agent` string.
4. Respect terms of service of the website.

Below is an educational implementation simulating `requests` and `BeautifulSoup` functionality to teach the concepts.
"""

from typing import List, Dict, Optional
import re
import urllib.request
import urllib.error
import time

# ==========================================
# 1. Simulating `requests` Library
# ==========================================
class SimpleResponse:
    def __init__(self, status_code: int, text: str):
        self.status_code = status_code
        self.text = text

def simple_get(url: str, headers: Optional[Dict[str, str]] = None) -> SimpleResponse:
    """A minimal wrapper around urllib to simulate requests.get()"""
    req_headers = headers or {'User-Agent': 'Python/Educational-Scraper'}
    req = urllib.request.Request(url, headers=req_headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            return SimpleResponse(response.status, html)
    except urllib.error.HTTPError as e:
        return SimpleResponse(e.code, "")
    except Exception as e:
        return SimpleResponse(500, "")

# ==========================================
# 2. Simulating HTML Parsing (like BeautifulSoup)
# ==========================================
class SimpleParser:
    """A minimal regex-based parser to simulate BeautifulSoup's find mechanisms.
    NOTE: In production, NEVER use regex for complex HTML parsing. Always use BeautifulSoup or lxml.
    This is strictly for educational, standalone demonstration.
    """
    def __init__(self, html: str):
        self.html = html

    def find_all(self, tag: str, class_name: Optional[str] = None) -> List[str]:
        """Finds all contents of a specific tag, optionally filtering by class."""
        if class_name:
            # Pattern to match <tag class="class_name">content</tag>
            pattern = f'<{tag}[^>]*class=["\'][^"\']*\\b{class_name}\\b[^"\']*["\'][^>]*>(.*?)</{tag}>'
        else:
            pattern = f'<{tag}[^>]*>(.*?)</{tag}>'
            
        matches = re.findall(pattern, self.html, re.IGNORECASE | re.DOTALL)
        return [m.strip() for m in matches]

# ==========================================
# 3. Professional Scraper Implementation
# ==========================================

class BlogScraper:
    """A class designed to scrape blog titles from a given URL."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (Educational Scraper)',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
    def fetch_page(self, url: str) -> Optional[str]:
        """Fetches the HTML content of the page with error handling."""
        print(f"Fetching: {url} ...")
        response = simple_get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return None

    def parse_titles(self, html: str) -> List[str]:
        """Parses article titles from the HTML."""
        parser = SimpleParser(html)
        # Assuming the blog titles are inside <h2> tags with class "post-title"
        titles = parser.find_all("h2", class_name="post-title")
        
        # Clean up HTML entities or tags within the title if necessary
        clean_titles = [re.sub(r'<[^>]+>', '', title).strip() for title in titles]
        return clean_titles

    def scrape_multiple_pages(self, num_pages: int) -> List[str]:
        """Scrapes multiple paginated pages."""
        all_titles = []
        for page in range(1, num_pages + 1):
            url = f"{self.base_url}?page={page}"
            html = self.fetch_page(url)
            if html:
                titles = self.parse_titles(html)
                all_titles.extend(titles)
            
            # Rate Limiting: Be polite to the server
            time.sleep(1) 
            
        return all_titles


# ==========================================
# Usage Example & Tests
# ==========================================
def run_tests():
    print("--- Running Web Scraping Tests ---")
    
    # Mock HTML content to test parsing logic
    mock_html = """
    <html>
        <body>
            <div class="content">
                <h2 class="post-title">Python 101</h2>
                <p>Learn basics</p>
                <h2 class="post-title"> <span>Advanced Scraping</span> </h2>
                <h2>Not a target title</h2>
            </div>
        </body>
    </html>
    """
    
    # 1. Test HTML Parser
    parser = SimpleParser(mock_html)
    titles = parser.find_all("h2", class_name="post-title")
    assert len(titles) == 2, "Should find exactly 2 titles with class 'post-title'"
    assert titles[0] == "Python 101"
    assert "Advanced Scraping" in titles[1]
    print("HTML Parsing tests passed.")
    
    # 2. Test Scraper class methods (using mocked HTML to avoid network calls in tests)
    scraper = BlogScraper("http://dummy-url.com")
    parsed = scraper.parse_titles(mock_html)
    assert len(parsed) == 2
    assert parsed[0] == "Python 101"
    assert parsed[1] == "Advanced Scraping" # Checks if inner tags are stripped
    print("Scraper parsing tests passed.")
    
    print("All Web Scraping concepts tests passed successfully.")

if __name__ == "__main__":
    run_tests()

"""
Complexity Analysis & Architecture Discussion:
- Performance & Concurrency: Sequential requests are slow. For large-scale scraping, use asynchronous libraries like `aiohttp` combined with `asyncio`, or distributed task queues like Celery.
- Dynamic Content: The `requests` library cannot render JavaScript. For Modern SPAs (React/Vue/Angular), you must use headless browsers like `Playwright`, `Selenium`, or intercept the underlying API calls the website makes via browser DevTools.
- Robustness: Websites change frequently. Scrapers are fragile. Implement robust error handling, retries with exponential backoff, and logging to detect when your parsers break.

Interview Challenge:
Q: You are scraping a site, but you keep getting blocked or receiving HTTP 403 Forbidden. What are the common reasons and how do you bypass this?
A: 
1. Missing/Default User-Agent: Servers block default user agents like "python-requests". Fix: Rotate realistic User-Agent strings.
2. IP Blocking: Too many requests from a single IP. Fix: Implement delays (`time.sleep()`), use proxies, or proxy-rotating services.
3. Cookies/Session Tokens: The site requires session state. Fix: Use a Session object (`requests.Session()`) to maintain cookies across requests.
4. CAPTCHAs/JS Challenges: Sites use Cloudflare or Datadome. Fix: Difficult to bypass completely; may require Headless Browsers + CAPTCHA solving services, though at this point, you should evaluate if an official API exists.
"""
