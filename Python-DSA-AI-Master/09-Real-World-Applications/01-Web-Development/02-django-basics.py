"""
Django Basics: A Comprehensive Guide to the MTV Architecture

Learning Objectives:
1. Understand the core concepts of Django: MTV (Model-Template-View) architecture.
2. Learn how to set up models, views, and routing (URLs).
3. Gain practical knowledge of Django's ORM and Admin interface.
4. Professional implementation details including project structure and security best practices.

Concept Explanation:
Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It's free and open source.
Industry use cases include Content Management Systems (CMS), e-commerce platforms, scientific computing platforms, and social networks.

Django uses the MTV (Model-Template-View) architecture:
- Model: The data access layer. Handles database schema, queries, and business logic related to data.
- View: The business logic layer. Receives HTTP requests, interacts with models, and returns HTTP responses (often rendering a template).
- Template: The presentation layer. Defines how the data should be displayed using HTML and Django Template Language (DTL).

Below is a conceptual code example demonstrating how these components tie together in a standard Django app. Note that to run this, you would need a full Django project environment, but this file serves as a conceptual implementation guide.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import json

# ==========================================
# 1. Models (Database Layer)
# ==========================================
# In a real Django project, these would inherit from django.db.models.Model

class MockDjangoModel:
    """Mock base class for Django models to simulate ORM behavior."""
    objects: List[Any] = []
    
    def save(self) -> None:
        self.__class__.objects.append(self)
        
    @classmethod
    def filter(cls, **kwargs) -> List[Any]:
        results = []
        for obj in cls.objects:
            match = True
            for k, v in kwargs.items():
                if getattr(obj, k, None) != v:
                    match = False
                    break
            if match:
                results.append(obj)
        return results

class Article(MockDjangoModel):
    """
    Represents an Article in our blog system.
    In Django:
    class Article(models.Model):
        title = models.CharField(max_length=200)
        content = models.TextField()
        published = models.BooleanField(default=False)
    """
    def __init__(self, title: str, content: str, published: bool = False):
        self.title = title
        self.content = content
        self.published = published

    def __repr__(self) -> str:
        return f"<Article: {self.title}>"

# ==========================================
# 2. Views (Business Logic Layer)
# ==========================================
# In Django, views take a request and return a response.

@dataclass
class MockHttpRequest:
    method: str
    path: str
    GET: Dict[str, str]
    POST: Dict[str, str]

@dataclass
class MockHttpResponse:
    content: str
    status_code: int = 200

def article_list_view(request: MockHttpRequest) -> MockHttpResponse:
    """
    A view that retrieves published articles and renders them.
    In Django, you'd typically use `render(request, 'template_name.html', context)`.
    """
    if request.method != 'GET':
        return MockHttpResponse("Method not allowed", status_code=405)
        
    # Fetch published articles
    published_articles = Article.filter(published=True)
    
    # Render template (Mocked here as a simple string concatenation)
    context = {"articles": published_articles}
    html_content = "<h1>Blog Articles</h1><ul>"
    for art in context["articles"]:
        html_content += f"<li>{art.title}</li>"
    html_content += "</ul>"
    
    return MockHttpResponse(content=html_content, status_code=200)

def create_article_view(request: MockHttpRequest) -> MockHttpResponse:
    """
    A view to handle article creation.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if not title or not content:
            return MockHttpResponse("Missing title or content", status_code=400)
            
        new_article = Article(title=title, content=content, published=False)
        new_article.save()
        return MockHttpResponse("Article created successfully", status_code=201)
        
    return MockHttpResponse("Method not allowed", status_code=405)


# ==========================================
# 3. URL Routing (URLs Layer)
# ==========================================
# Simulating Django's urls.py behavior

URL_PATTERNS = {
    '/articles/': article_list_view,
    '/articles/create/': create_article_view,
}

def route_request(request: MockHttpRequest) -> MockHttpResponse:
    """Simulates Django's request routing engine."""
    view_func = URL_PATTERNS.get(request.path)
    if view_func:
        return view_func(request)
    return MockHttpResponse("Not Found", status_code=404)


# ==========================================
# Usage Example & Tests
# ==========================================
def run_tests():
    print("--- Running Django Basics Tests ---")
    
    # 1. Setup Data
    Article.objects = []
    a1 = Article("Django Intro", "Content here", published=True)
    a1.save()
    a2 = Article("Advanced Django", "Content there", published=False)
    a2.save()
    
    # 2. Test GET Articles View
    req_get = MockHttpRequest(method='GET', path='/articles/', GET={}, POST={})
    resp_get = route_request(req_get)
    assert resp_get.status_code == 200, "Should return 200 OK"
    assert "Django Intro" in resp_get.content, "Published article should be in content"
    assert "Advanced Django" not in resp_get.content, "Unpublished article should NOT be in content"
    print("GET View Test Passed!")
    
    # 3. Test POST Create Article View
    req_post = MockHttpRequest(method='POST', path='/articles/create/', GET={}, POST={"title": "New Post", "content": "Hello"})
    resp_post = route_request(req_post)
    assert resp_post.status_code == 201, "Should return 201 Created"
    assert len(Article.objects) == 3, "New article should be saved"
    print("POST View Test Passed!")
    
    # 4. Test 404
    req_404 = MockHttpRequest(method='GET', path='/non-existent/', GET={}, POST={})
    resp_404 = route_request(req_404)
    assert resp_404.status_code == 404, "Should return 404 Not Found"
    print("404 Routing Test Passed!")

    print("All Django concepts tests passed successfully.")

if __name__ == "__main__":
    run_tests()

"""
Complexity Analysis & Architecture Discussion:
- Scalability: Django handles scalability well through caching, asynchronous views (Django 3.1+), and scaling horizontally (multiple server nodes).
- Security: Django provides built-in protection against XSS, CSRF, SQL Injection, and Clickjacking. Always use Django's ORM instead of raw SQL queries to prevent SQL injection.
- Performance: ORM queries can become inefficient (N+1 query problem). Use `select_related()` and `prefetch_related()` for optimizing database queries in production.

Interview Challenge:
Q: Explain the N+1 query problem in Django and how to solve it.
A: The N+1 query problem occurs when you fetch a list of objects (1 query) and then iterate over them to fetch a related object for each one (N queries). 
   This severely degrades performance. 
   Solution: Use `select_related()` for single-valued relationships (Foreign Key/One-to-One) which performs a SQL JOIN. Use `prefetch_related()` for multi-valued relationships (Many-to-Many/Reverse Foreign Key) which performs a separate query and joins them in Python.
"""
