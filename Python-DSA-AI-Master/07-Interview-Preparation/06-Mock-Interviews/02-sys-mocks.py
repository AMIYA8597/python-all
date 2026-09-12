"""
Module: 02-sys-mocks
Learning Objectives:
- Understand the components of a System Design interview.
- Learn how to structure a system design discussion.
- Implement mock classes representing system components.

This script simulates a System Design mock interview scenario: URL Shortener (e.g., TinyURL).
"""

from typing import Dict
import hashlib
import time

# --- Concept Explanation ---
# In a system design interview, you are expected to:
# 1. Clarify requirements (functional and non-functional).
# 2. Back-of-the-envelope estimation.
# 3. High-level design (API, DB schema, basic architecture).
# 4. Deep dives (scaling, partitioning, caching, rate limiting).

# --- Basic / Intermediate Implementation ---
# We will create a basic mock of a URL shortener system.

class URLShortener:
    """
    A basic mock implementation of a URL Shortener system.
    """
    def __init__(self, domain: str = "http://tinyurl.com/"):
        self.domain = domain
        self.url_to_hash: Dict[str, str] = {}
        self.hash_to_url: Dict[str, str] = {}
        
    def _generate_hash(self, long_url: str) -> str:
        """
        Generate a short hash for the URL.
        Using MD5 and taking the first 6 characters for simplicity.
        """
        hasher = hashlib.md5()
        hasher.update(long_url.encode('utf-8'))
        return hasher.hexdigest()[:6]

    def shorten(self, long_url: str) -> str:
        """
        Functional Requirement: Shorten a given long URL.
        """
        if long_url in self.url_to_hash:
            return self.domain + self.url_to_hash[long_url]
            
        short_hash = self._generate_hash(long_url)
        
        # Handling collision (very simplistically)
        while short_hash in self.hash_to_url and self.hash_to_url[short_hash] != long_url:
            short_hash = self._generate_hash(long_url + str(time.time()))
            
        self.url_to_hash[long_url] = short_hash
        self.hash_to_url[short_hash] = long_url
        
        return self.domain + short_hash

    def redirect(self, short_url: str) -> str:
        """
        Functional Requirement: Redirect short URL to long URL.
        """
        short_hash = short_url.replace(self.domain, "")
        if short_hash in self.hash_to_url:
            return self.hash_to_url[short_hash]
        return "Error: URL not found"

# --- Performance Analysis ---
# Time: O(1) for shorten (assuming low collisions) and O(1) for redirect.
# Space: O(N) where N is the number of shortened URLs.

# --- Edge Cases ---
# 1. Hash collisions.
# 2. Custom alias requests.
# 3. Expired URLs (not implemented here, requires a timestamp field).

# --- Interview Challenge ---
# Challenge: Design a distributed URL shortener. How would you partition the database?
# How do you generate unique IDs at scale? (e.g., Snowflake, Ticket Server).

# --- Tests ---
def test_url_shortener():
    sys = URLShortener()
    long_url = "https://www.example.com/some/long/path?param=value"
    short = sys.shorten(long_url)
    assert short.startswith("http://tinyurl.com/"), "Test 1 failed"
    
    orig = sys.redirect(short)
    assert orig == long_url, "Test 2 failed"
    
    # Same URL should return same short URL
    short2 = sys.shorten(long_url)
    assert short == short2, "Test 3 failed"
    
    print("All tests passed!")

if __name__ == "__main__":
    test_url_shortener()
