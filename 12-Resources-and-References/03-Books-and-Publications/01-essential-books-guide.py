#!/usr/bin/env python3
"""
Essential Books and Publications Guide

This module provides a comprehensive guide to the most important books and publications
for mastering data structures, algorithms, and Python programming. Each book includes
detailed reviews, difficulty levels, and learning recommendations.

Features:
- Curated collection of essential programming books
- Detailed reviews and ratings
- Reading recommendations by skill level
- Topic-specific book collections
- Author profiles and credibility
- Comparison matrices for book selection

Author: Python DSA Master
Date: 2024
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
import json
import datetime


class BookCategory(Enum):
    """Book categories for organization."""
    ALGORITHMS = "algorithms"
    DATA_STRUCTURES = "data_structures"
    PYTHON = "python"
    INTERVIEW_PREP = "interview_prep"
    SYSTEM_DESIGN = "system_design"
    COMPETITIVE_PROGRAMMING = "competitive_programming"
    COMPUTER_SCIENCE = "computer_science"
    SOFTWARE_ENGINEERING = "software_engineering"


class SkillLevel(Enum):
    """Target skill levels for books."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class Author:
    """Represents a book author with credentials."""
    name: str
    credentials: List[str] = field(default_factory=list)
    affiliations: List[str] = field(default_factory=list)
    notable_works: List[str] = field(default_factory=list)
    expertise_areas: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "credentials": self.credentials,
            "affiliations": self.affiliations,
            "notable_works": self.notable_works,
            "expertise_areas": self.expertise_areas
        }


@dataclass
class BookReview:
    """Detailed book review and analysis."""
    overall_rating: float  # 1-5 scale
    content_quality: float
    readability: float
    practical_value: float
    depth_coverage: float
    
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    best_for: List[str] = field(default_factory=list)
    avoid_if: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_rating": self.overall_rating,
            "content_quality": self.content_quality,
            "readability": self.readability,
            "practical_value": self.practical_value,
            "depth_coverage": self.depth_coverage,
            "pros": self.pros,
            "cons": self.cons,
            "best_for": self.best_for,
            "avoid_if": self.avoid_if
        }


@dataclass
class Book:
    """Comprehensive book information."""
    title: str
    authors: List[Author]
    category: BookCategory
    skill_level: SkillLevel
    isbn: str = ""
    publisher: str = ""
    publication_year: int = 0
    pages: int = 0
    edition: str = "1st"
    
    description: str = ""
    key_topics: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    learning_outcomes: List[str] = field(default_factory=list)
    
    review: Optional[BookReview] = None
    price_range: str = ""  # e.g., "$30-40", "Free"
    availability: List[str] = field(default_factory=list)  # Physical, eBook, Audiobook
    online_resources: Dict[str, str] = field(default_factory=dict)
    
    estimated_reading_time: int = 0  # in hours
    companion_resources: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "authors": [author.to_dict() for author in self.authors],
            "category": self.category.value,
            "skill_level": self.skill_level.value,
            "isbn": self.isbn,
            "publisher": self.publisher,
            "publication_year": self.publication_year,
            "pages": self.pages,
            "edition": self.edition,
            "description": self.description,
            "key_topics": self.key_topics,
            "prerequisites": self.prerequisites,
            "learning_outcomes": self.learning_outcomes,
            "review": self.review.to_dict() if self.review else None,
            "price_range": self.price_range,
            "availability": self.availability,
            "online_resources": self.online_resources,
            "estimated_reading_time": self.estimated_reading_time,
            "companion_resources": self.companion_resources
        }


class BookCatalog:
    """Comprehensive catalog of programming books."""
    
    def __init__(self):
        self.books: List[Book] = []
        self._initialize_books()
    
    def _initialize_books(self):
        """Initialize the book catalog with essential programming books."""
        
        # Create author objects
        gayle_mcdowell = Author(
            name="Gayle Laakmann McDowell",
            credentials=["Former Google Engineer", "Former Microsoft Engineer", "Former Apple Engineer"],
            affiliations=["CareerCup"],
            notable_works=["Cracking the Coding Interview", "Cracking the PM Interview"],
            expertise_areas=["Technical Interviews", "Software Engineering", "Career Development"]
        )
        
        cormen_authors = [
            Author(name="Thomas H. Cormen", affiliations=["Dartmouth College"], expertise_areas=["Algorithms"]),
            Author(name="Charles E. Leiserson", affiliations=["MIT"], expertise_areas=["Algorithms", "Parallel Computing"]),
            Author(name="Ronald L. Rivest", affiliations=["MIT"], expertise_areas=["Cryptography", "Algorithms"]),
            Author(name="Clifford Stein", affiliations=["Columbia University"], expertise_areas=["Algorithms"])
        ]
        
        brett_slatkin = Author(
            name="Brett Slatkin",
            credentials=["Principal Software Engineer at Google"],
            affiliations=["Google"],
            notable_works=["Effective Python"],
            expertise_areas=["Python", "Software Engineering", "Distributed Systems"]
        )
        
        # Essential Books
        books = [
            # Interview Preparation
            Book(
                title="Cracking the Coding Interview: 189 Programming Questions and Solutions",
                authors=[gayle_mcdowell],
                category=BookCategory.INTERVIEW_PREP,
                skill_level=SkillLevel.INTERMEDIATE,
                isbn="978-0984782857",
                publisher="CareerCup",
                publication_year=2015,
                pages=696,
                edition="6th",
                description="The gold standard for technical interview preparation. Contains 189 programming questions with detailed solutions, interview strategies, and behind-the-scenes insights from hiring managers.",
                key_topics=[
                    "Data Structures", "Algorithms", "System Design", "Interview Strategy",
                    "Behavioral Questions", "Negotiation", "Big O Analysis"
                ],
                prerequisites=["Basic programming knowledge", "Understanding of fundamental data structures"],
                learning_outcomes=[
                    "Master common interview question patterns",
                    "Develop systematic problem-solving approach",
                    "Understand what interviewers look for",
                    "Build confidence for technical interviews"
                ],
                review=BookReview(
                    overall_rating=4.8,
                    content_quality=4.9,
                    readability=4.7,
                    practical_value=5.0,
                    depth_coverage=4.6,
                    pros=[
                        "Comprehensive coverage of interview topics",
                        "Real interview questions from top companies",
                        "Excellent explanations and multiple solutions",
                        "Great insights into interview process",
                        "Includes system design and behavioral prep"
                    ],
                    cons=[
                        "Can be overwhelming for beginners",
                        "Some solutions could be more optimized",
                        "Heavy focus on traditional tech companies"
                    ],
                    best_for=[
                        "Software engineers preparing for FAANG interviews",
                        "CS students entering job market",
                        "Anyone wanting systematic interview prep"
                    ],
                    avoid_if=[
                        "Complete programming beginner",
                        "Looking for language-specific prep only"
                    ]
                ),
                price_range="$35-45",
                availability=["Physical", "eBook", "Audiobook"],
                online_resources={
                    "Official Website": "https://www.crackingthecodinginterview.com/",
                    "GitHub": "https://github.com/careercup/CtCI-6th-Edition"
                },
                estimated_reading_time=80,
                companion_resources=["Video solutions", "Online practice platform"]
            ),
            
            # Algorithms Bible
            Book(
                title="Introduction to Algorithms",
                authors=cormen_authors,
                category=BookCategory.ALGORITHMS,
                skill_level=SkillLevel.ADVANCED,
                isbn="978-0262033848",
                publisher="MIT Press",
                publication_year=2009,
                pages=1312,
                edition="3rd",
                description="The definitive algorithms textbook, known as 'CLRS'. Provides comprehensive coverage of algorithms with rigorous mathematical analysis. Used in top universities worldwide.",
                key_topics=[
                    "Sorting and Order Statistics", "Data Structures", "Advanced Design Techniques",
                    "Graph Algorithms", "Network Flow", "String Algorithms", "Computational Geometry",
                    "Linear Programming", "Advanced Topics"
                ],
                prerequisites=[
                    "Strong mathematical background", "Discrete mathematics",
                    "Basic programming experience", "Comfort with mathematical proofs"
                ],
                learning_outcomes=[
                    "Deep understanding of algorithm design and analysis",
                    "Master advanced algorithmic techniques",
                    "Develop mathematical thinking about computation",
                    "Build foundation for research and advanced study"
                ],
                review=BookReview(
                    overall_rating=4.7,
                    content_quality=5.0,
                    readability=3.8,
                    practical_value=4.2,
                    depth_coverage=5.0,
                    pros=[
                        "Most comprehensive algorithms coverage",
                        "Rigorous mathematical treatment",
                        "Excellent for reference and deep study",
                        "Industry standard textbook",
                        "Covers both theory and practice"
                    ],
                    cons=[
                        "Very dense and mathematical",
                        "Not beginner-friendly",
                        "Limited programming examples",
                        "Can be intimidating"
                    ],
                    best_for=[
                        "CS graduate students",
                        "Researchers in algorithms",
                        "Advanced practitioners seeking depth",
                        "Those preparing for algorithm competitions"
                    ],
                    avoid_if=[
                        "Beginner programmer",
                        "Looking for quick practical solutions",
                        "Weak mathematical background"
                    ]
                ),
                price_range="$200-250",
                availability=["Physical", "eBook"],
                online_resources={
                    "MIT OpenCourseWare": "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-046j-design-and-analysis-of-algorithms-spring-2015/",
                    "Solutions Manual": "Available separately"
                },
                estimated_reading_time=200,
                companion_resources=["MIT lecture videos", "Problem sets", "Solutions manual"]
            ),
            
            # Python Mastery
            Book(
                title="Effective Python: 90 Specific Ways to Write Better Python",
                authors=[brett_slatkin],
                category=BookCategory.PYTHON,
                skill_level=SkillLevel.INTERMEDIATE,
                isbn="978-0134853987",
                publisher="Addison-Wesley",
                publication_year=2019,
                pages=352,
                edition="2nd",
                description="A collection of 90 best practices, tips, and shortcuts for writing effective Python code. Covers Python 3.7+ features and idiomatic Python programming.",
                key_topics=[
                    "Pythonic Thinking", "Lists and Dictionaries", "Functions", "Comprehensions",
                    "Classes and Interfaces", "Metaclasses", "Concurrency and Parallelism",
                    "Robustness and Performance", "Testing and Debugging", "Collaboration"
                ],
                prerequisites=[
                    "Basic Python programming experience",
                    "Familiarity with Python syntax and basic concepts"
                ],
                learning_outcomes=[
                    "Write more Pythonic and efficient code",
                    "Master Python's advanced features",
                    "Avoid common Python pitfalls",
                    "Improve code readability and maintainability"
                ],
                review=BookReview(
                    overall_rating=4.7,
                    content_quality=4.8,
                    readability=4.6,
                    practical_value=4.9,
                    depth_coverage=4.5,
                    pros=[
                        "Excellent practical advice",
                        "Covers modern Python features",
                        "Clear examples and explanations",
                        "Written by Google engineer with real experience",
                        "Covers both basics and advanced topics"
                    ],
                    cons=[
                        "Assumes some Python experience",
                        "Could benefit from more comprehensive examples",
                        "Some items are quite specific"
                    ],
                    best_for=[
                        "Python developers wanting to improve their code",
                        "Intermediate Python programmers",
                        "Anyone serious about Python development"
                    ],
                    avoid_if=[
                        "Complete Python beginner",
                        "Looking for language introduction"
                    ]
                ),
                price_range="$40-50",
                availability=["Physical", "eBook"],
                online_resources={
                    "Author's Blog": "https://effectivepython.com/",
                    "Code Examples": "Available on publisher's website"
                },
                estimated_reading_time=45,
                companion_resources=["Online code examples", "Author blog posts"]
            ),
            
            # Beginner-Friendly Algorithms
            Book(
                title="Grokking Algorithms: An Illustrated Guide for Programmers and Other Curious People",
                authors=[Author(name="Aditya Bhargava", expertise_areas=["Software Engineering", "Technical Writing"])],
                category=BookCategory.ALGORITHMS,
                skill_level=SkillLevel.BEGINNER,
                isbn="978-1617292231",
                publisher="Manning Publications",
                publication_year=2016,
                pages=256,
                description="A visual and intuitive approach to learning algorithms. Uses illustrations and simple explanations to make complex concepts accessible to beginners.",
                key_topics=[
                    "Binary Search", "Selection Sort", "Recursion", "Quicksort",
                    "Hash Tables", "Breadth-First Search", "Dijkstra's Algorithm",
                    "Greedy Algorithms", "Dynamic Programming", "K-Nearest Neighbors"
                ],
                prerequisites=["Basic programming knowledge in any language"],
                learning_outcomes=[
                    "Understand fundamental algorithms intuitively",
                    "Develop algorithmic thinking",
                    "Learn to analyze algorithm performance",
                    "Build foundation for advanced study"
                ],
                review=BookReview(
                    overall_rating=4.5,
                    content_quality=4.4,
                    readability=4.9,
                    practical_value=4.3,
                    depth_coverage=3.8,
                    pros=[
                        "Excellent visual explanations",
                        "Very beginner-friendly",
                        "Makes complex topics accessible",
                        "Engaging writing style",
                        "Good practical examples"
                    ],
                    cons=[
                        "Limited depth on advanced topics",
                        "Not comprehensive enough for advanced users",
                        "Some algorithms covered superficially"
                    ],
                    best_for=[
                        "Programming beginners",
                        "Visual learners",
                        "Those intimidated by traditional algorithms books",
                        "Self-taught programmers"
                    ],
                    avoid_if=[
                        "Already have strong algorithms background",
                        "Need comprehensive coverage",
                        "Prefer mathematical rigor"
                    ]
                ),
                price_range="$35-45",
                availability=["Physical", "eBook"],
                online_resources={
                    "Manning Publications": "https://www.manning.com/books/grokking-algorithms",
                    "Code Examples": "Available on publisher's website"
                },
                estimated_reading_time=30,
                companion_resources=["Online code examples", "Practice exercises"]
            ),
            
            # Python Interview Specific
            Book(
                title="Elements of Programming Interviews in Python: The Insiders' Guide",
                authors=[
                    Author(name="Adnan Aziz", affiliations=["University of Texas"], expertise_areas=["Algorithms", "Software Engineering"]),
                    Author(name="Tsung-Hsien Lee", affiliations=["Google"], expertise_areas=["Software Engineering"]),
                    Author(name="Amit Prakash", affiliations=["Google"], expertise_areas=["Software Engineering"])
                ],
                category=BookCategory.INTERVIEW_PREP,
                skill_level=SkillLevel.INTERMEDIATE,
                isbn="978-1537713946",
                publisher="CreateSpace",
                publication_year=2016,
                pages=424,
                description="Python-specific interview preparation with 300+ solved problems. Focuses on problem-solving patterns and Python-specific techniques.",
                key_topics=[
                    "Arrays", "Strings", "Linked Lists", "Stacks and Queues",
                    "Binary Trees", "Heaps", "Searching", "Hash Tables",
                    "Sorting", "Binary Search Trees", "Recursion", "Dynamic Programming",
                    "Greedy Algorithms", "Graphs", "Parallel Computing"
                ],
                prerequisites=["Python programming experience", "Basic data structures knowledge"],
                learning_outcomes=[
                    "Master Python-specific interview techniques",
                    "Learn to implement algorithms efficiently in Python",
                    "Understand Python's standard library for interviews",
                    "Develop systematic approach to problem-solving"
                ],
                review=BookReview(
                    overall_rating=4.6,
                    content_quality=4.7,
                    readability=4.4,
                    practical_value=4.8,
                    depth_coverage=4.5,
                    pros=[
                        "Python-specific focus",
                        "Comprehensive problem coverage",
                        "Good explanations of solutions",
                        "Leverages Python's strengths",
                        "Written by industry experts"
                    ],
                    cons=[
                        "Less popular than language-agnostic books",
                        "Some problems are quite challenging",
                        "Could use more system design content"
                    ],
                    best_for=[
                        "Python developers preparing for interviews",
                        "Those wanting Python-specific techniques",
                        "Experienced programmers switching to Python"
                    ],
                    avoid_if=[
                        "Prefer language-agnostic approach",
                        "Complete programming beginner",
                        "Not using Python in interviews"
                    ]
                ),
                price_range="$50-60",
                availability=["Physical", "eBook"],
                online_resources={
                    "Official Website": "https://elementsofprogramminginterviews.com/",
                    "Judge Platform": "Available for additional practice"
                },
                estimated_reading_time=70,
                companion_resources=["Online judge", "Additional problems", "Solution videos"]
            )
        ]
        
        self.books.extend(books)
    
    def get_books_by_category(self, category: BookCategory) -> List[Book]:
        """Get books filtered by category."""
        return [book for book in self.books if book.category == category]
    
    def get_books_by_skill_level(self, level: SkillLevel) -> List[Book]:
        """Get books filtered by skill level."""
        return [book for book in self.books if book.skill_level == level]
    
    def get_top_rated_books(self, limit: int = 10) -> List[Book]:
        """Get top-rated books."""
        rated_books = [book for book in self.books if book.review]
        return sorted(rated_books, key=lambda b: b.review.overall_rating, reverse=True)[:limit]
    
    def search_books(self, query: str) -> List[Book]:
        """Search books by title, author, or topics."""
        query_lower = query.lower()
        results = []
        
        for book in self.books:
            # Search in title
            if query_lower in book.title.lower():
                results.append(book)
                continue
            
            # Search in authors
            if any(query_lower in author.name.lower() for author in book.authors):
                results.append(book)
                continue
            
            # Search in topics
            if any(query_lower in topic.lower() for topic in book.key_topics):
                results.append(book)
                continue
        
        return results
    
    def get_reading_path(self, goal: str) -> List[Book]:
        """Get recommended reading path for specific goals."""
        if goal == "interview_prep":
            return [
                book for book in self.books 
                if book.category in [BookCategory.INTERVIEW_PREP, BookCategory.ALGORITHMS]
            ]
        elif goal == "python_mastery":
            return [
                book for book in self.books 
                if book.category == BookCategory.PYTHON
            ]
        elif goal == "algorithms_deep":
            return [
                book for book in self.books 
                if book.category == BookCategory.ALGORITHMS
            ]
        
        return []
    
    def export_catalog(self, filename: str):
        """Export book catalog to JSON."""
        data = {
            "books": [book.to_dict() for book in self.books],
            "export_date": datetime.datetime.now().isoformat(),
            "total_books": len(self.books)
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def demonstrate_book_catalog():
    """Demonstrate book catalog functionality."""
    print("Essential Programming Books Guide")
    print("=" * 40)
    
    catalog = BookCatalog()
    
    print(f"\nTotal Books in Catalog: {len(catalog.books)}")
    
    # Show books by category
    print("\nBooks by Category:")
    for category in BookCategory:
        books = catalog.get_books_by_category(category)
        if books:
            print(f"  {category.value.replace('_', ' ').title()}: {len(books)}")
    
    # Show top-rated books
    print("\nTop-Rated Books:")
    top_books = catalog.get_top_rated_books(5)
    for i, book in enumerate(top_books, 1):
        rating = book.review.overall_rating if book.review else "N/A"
        print(f"  {i}. {book.title}")
        print(f"     Rating: {rating}/5.0 | Level: {book.skill_level.value}")
        print(f"     Authors: {', '.join(author.name for author in book.authors)}")
        print()
    
    # Show detailed review for top book
    if top_books and top_books[0].review:
        book = top_books[0]
        review = book.review
        print(f"Detailed Review: {book.title}")
        print("-" * 30)
        print(f"Content Quality: {review.content_quality}/5.0")
        print(f"Readability: {review.readability}/5.0")
        print(f"Practical Value: {review.practical_value}/5.0")
        
        print(f"\nPros:")
        for pro in review.pros[:3]:
            print(f"  + {pro}")
        
        print(f"\nBest For:")
        for target in review.best_for[:2]:
            print(f"  • {target}")


def generate_reading_recommendations():
    """Generate personalized reading recommendations."""
    print("\n\nPersonalized Reading Recommendations")
    print("=" * 45)
    
    catalog = BookCatalog()
    
    # Define user profiles
    user_profiles = {
        "Beginner Python Developer": {
            "skill_level": SkillLevel.BEGINNER,
            "interests": ["python", "algorithms"],
            "goal": "Build strong foundation"
        },
        "Interview Candidate": {
            "skill_level": SkillLevel.INTERMEDIATE,
            "interests": ["interview_prep", "algorithms"],
            "goal": "Pass technical interviews"
        },
        "Advanced Practitioner": {
            "skill_level": SkillLevel.ADVANCED,
            "interests": ["algorithms", "system_design"],
            "goal": "Deep technical knowledge"
        }
    }
    
    for profile_name, profile in user_profiles.items():
        print(f"\nRecommendations for {profile_name}:")
        print(f"Goal: {profile['goal']}")
        print(f"Skill Level: {profile['skill_level'].value}")
        
        # Get books matching profile
        suitable_books = []
        for book in catalog.books:
            if book.skill_level == profile['skill_level']:
                suitable_books.append(book)
            elif (book.skill_level == SkillLevel.BEGINNER and 
                  profile['skill_level'] == SkillLevel.INTERMEDIATE):
                suitable_books.append(book)
        
        # Sort by rating and relevance
        if suitable_books:
            rated_books = [b for b in suitable_books if b.review]
            if rated_books:
                top_recommendations = sorted(
                    rated_books, 
                    key=lambda b: b.review.overall_rating, 
                    reverse=True
                )[:2]
            else:
                top_recommendations = suitable_books[:2]
            
            for i, book in enumerate(top_recommendations, 1):
                print(f"  {i}. {book.title}")
                print(f"     Level: {book.skill_level.value}")
                print(f"     Reading Time: ~{book.estimated_reading_time}h")
                if book.review:
                    print(f"     Rating: {book.review.overall_rating}/5.0")
        print()


def create_book_comparison_matrix():
    """Create comparison matrix for book selection."""
    print("\nBook Comparison Matrix")
    print("=" * 30)
    
    catalog = BookCatalog()
    interview_books = catalog.get_books_by_category(BookCategory.INTERVIEW_PREP)
    
    if not interview_books:
        print("No interview books found.")
        return
    
    print("\nInterview Preparation Books Comparison:")
    print("-" * 50)
    
    # Header
    headers = ["Book", "Rating", "Pages", "Level", "Price"]
    print(f"{'Book':<35} {'Rating':<8} {'Pages':<8} {'Level':<12} {'Price':<10}")
    print("-" * 80)
    
    for book in interview_books:
        title = book.title[:32] + "..." if len(book.title) > 35 else book.title
        rating = f"{book.review.overall_rating}/5" if book.review else "N/A"
        level = book.skill_level.value
        price = book.price_range if book.price_range else "N/A"
        
        print(f"{title:<35} {rating:<8} {book.pages:<8} {level:<12} {price:<10}")


def export_book_data():
    """Export book data for external use."""
    print("\n\nExporting Book Data")
    print("=" * 25)
    
    catalog = BookCatalog()
    
    # Export full catalog
    catalog.export_catalog("programming_books_catalog.json")
    print("Exported full catalog to programming_books_catalog.json")
    
    # Create category-specific exports
    categories = [BookCategory.INTERVIEW_PREP, BookCategory.PYTHON, BookCategory.ALGORITHMS]
    
    for category in categories:
        books = catalog.get_books_by_category(category)
        if books:
            category_data = {
                "category": category.value,
                "books": [book.to_dict() for book in books],
                "count": len(books),
                "export_date": datetime.datetime.now().isoformat()
            }
            
            filename = f"{category.value}_books.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(category_data, f, indent=2, ensure_ascii=False)
            
            print(f"Exported {len(books)} {category.value} books to {filename}")


def main():
    """Main function to demonstrate books and publications guide."""
    print("Python DSA Master - Essential Books and Publications Guide")
    print("=" * 65)
    
    try:
        demonstrate_book_catalog()
        generate_reading_recommendations()
        create_book_comparison_matrix()
        export_book_data()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*65}")
    print("Books and publications guide demonstration complete!")


if __name__ == "__main__":
    main()


# ============================================================================
# ADDITIONAL READING RECOMMENDATIONS
# ============================================================================

"""
📚 COMPREHENSIVE READING ROADMAP BY SKILL LEVEL:

🎯 BEGINNER LEVEL (0-1 years experience):
1. "Python Crash Course" by Eric Matthes
   • Perfect introduction to Python programming
   • Hands-on projects and exercises
   • Web development and data visualization basics

2. "Grokking Algorithms" by Aditya Bhargava
   • Visual approach to learning algorithms
   • Beginner-friendly explanations
   • Foundation for advanced study

3. "Automate the Boring Stuff with Python" by Al Sweigart
   • Practical Python applications
   • Real-world automation examples
   • Available free online

🚀 INTERMEDIATE LEVEL (1-3 years experience):
1. "Effective Python" by Brett Slatkin
   • Advanced Python techniques and best practices
   • Performance optimization
   • Pythonic code patterns

2. "Cracking the Coding Interview" by Gayle McDowell
   • Essential for technical interviews
   • Comprehensive problem-solving strategies
   • Industry insights

3. "Elements of Programming Interviews in Python"
   • Python-specific interview preparation
   • 300+ solved problems
   • Advanced problem-solving patterns

⚡ ADVANCED LEVEL (3+ years experience):
1. "Introduction to Algorithms" by Cormen et al.
   • Definitive algorithms reference
   • Mathematical rigor and depth
   • Research-level coverage

2. "Designing Data-Intensive Applications" by Martin Kleppmann
   • System design and scalability
   • Distributed systems concepts
   • Modern architecture patterns

3. "The Algorithm Design Manual" by Steven Skiena
   • Practical algorithm design
   • Real-world case studies
   • Implementation guidance

📖 SPECIALIZED TOPICS:

🏆 COMPETITIVE PROGRAMMING:
• "Competitive Programming" by Steven & Felix Halim
• "Guide to Competitive Programming" by Antti Laaksonen
• "Programming Challenges" by Skiena & Revilla

🖥️ SYSTEM DESIGN:
• "Building Microservices" by Sam Newman
• "High Performance Python" by Micha Gorelick
• "Site Reliability Engineering" by Google

🧠 MACHINE LEARNING (for CS background):
• "Pattern Recognition and Machine Learning" by Bishop
• "The Elements of Statistical Learning" by Hastie et al.
• "Hands-On Machine Learning" by Aurélien Géron

💡 READING STRATEGY TIPS:

📅 READING SCHEDULE:
• Dedicate 30-60 minutes daily to reading
• Alternate between theoretical and practical books
• Take notes and implement examples
• Join book clubs or discussion groups

🎯 ACTIVE READING TECHNIQUES:
• Implement code examples as you read
• Create summaries for each chapter
• Teach concepts to others
• Apply techniques to personal projects

📊 PROGRESS TRACKING:
• Set monthly reading goals
• Maintain a reading journal
• Rate books and write reviews
• Share insights with peers

🔄 REVIEW STRATEGY:
• Revisit key books annually
• Update knowledge with new editions
• Cross-reference concepts across books
• Build a personal reference library

Remember: Books are investments in your career.
Choose quality over quantity and focus on understanding rather than completion.
"""
