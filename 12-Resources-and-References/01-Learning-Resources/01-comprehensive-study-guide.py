#!/usr/bin/env python3
"""
Comprehensive Study Guide and Learning Resources

This module serves as a comprehensive reference for Python DSA learning resources,
study materials, and practice platforms. It includes curated lists of books,
courses, websites, tools, and communities for mastering data structures and
algorithms in Python.

Features:
- Curated book recommendations with reviews
- Online course platforms and MOOCs
- Practice problem platforms with difficulty levels
- YouTube channels and video resources
- Community resources and study groups
- Tools and development environments
- Progress tracking and assessment

Author: Python DSA Master
Date: 2024
"""

import json
import webbrowser
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import datetime
import random
from collections import defaultdict


class DifficultyLevel(Enum):
    """Difficulty levels for learning resources."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ResourceType(Enum):
    """Types of learning resources."""
    BOOK = "book"
    COURSE = "course"
    VIDEO = "video"
    WEBSITE = "website"
    TOOL = "tool"
    COMMUNITY = "community"
    PRACTICE = "practice"


@dataclass
class LearningResource:
    """Represents a learning resource with metadata."""
    title: str
    type: ResourceType
    url: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    rating: float = 0.0
    description: str = ""
    topics: List[str] = field(default_factory=list)
    cost: str = "free"  # free, paid, freemium
    language: str = "english"
    estimated_hours: int = 0
    prerequisites: List[str] = field(default_factory=list)
    author: str = ""
    last_updated: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert resource to dictionary."""
        return {
            "title": self.title,
            "type": self.type.value,
            "url": self.url,
            "difficulty": self.difficulty.value,
            "rating": self.rating,
            "description": self.description,
            "topics": self.topics,
            "cost": self.cost,
            "language": self.language,
            "estimated_hours": self.estimated_hours,
            "prerequisites": self.prerequisites,
            "author": self.author,
            "last_updated": self.last_updated
        }


class ResourceCatalog:
    """Comprehensive catalog of learning resources."""
    
    def __init__(self):
        self.resources: List[LearningResource] = []
        self._initialize_resources()
    
    def _initialize_resources(self):
        """Initialize with curated learning resources."""
        
        # Books
        books = [
            LearningResource(
                title="Cracking the Coding Interview",
                type=ResourceType.BOOK,
                difficulty=DifficultyLevel.INTERMEDIATE,
                rating=4.8,
                description="The gold standard for technical interview preparation. 189+ programming questions and solutions.",
                topics=["interviews", "algorithms", "data-structures", "system-design"],
                cost="paid",
                author="Gayle Laakmann McDowell",
                estimated_hours=100,
                prerequisites=["basic-programming"]
            ),
            LearningResource(
                title="Introduction to Algorithms (CLRS)",
                type=ResourceType.BOOK,
                difficulty=DifficultyLevel.ADVANCED,
                rating=4.7,
                description="The definitive algorithms textbook. Comprehensive and rigorous treatment of algorithms.",
                topics=["algorithms", "complexity-analysis", "mathematical-foundations"],
                cost="paid",
                author="Cormen, Leiserson, Rivest, Stein",
                estimated_hours=200,
                prerequisites=["mathematics", "programming-experience"]
            ),
            LearningResource(
                title="Elements of Programming Interviews in Python",
                type=ResourceType.BOOK,
                difficulty=DifficultyLevel.INTERMEDIATE,
                rating=4.6,
                description="Python-specific interview preparation with 300+ solved problems.",
                topics=["python", "interviews", "algorithms", "problem-solving"],
                cost="paid",
                author="Aziz, Lee, Prakash",
                estimated_hours=80,
                prerequisites=["python-basics"]
            ),
            LearningResource(
                title="Grokking Algorithms",
                type=ResourceType.BOOK,
                difficulty=DifficultyLevel.BEGINNER,
                rating=4.5,
                description="Visual and intuitive approach to algorithms. Great for beginners.",
                topics=["algorithms", "data-structures", "visual-learning"],
                cost="paid",
                author="Aditya Bhargava",
                estimated_hours=40,
                prerequisites=["basic-programming"]
            ),
            LearningResource(
                title="Effective Python",
                type=ResourceType.BOOK,
                difficulty=DifficultyLevel.INTERMEDIATE,
                rating=4.7,
                description="90 specific ways to write better Python. Essential for Python developers.",
                topics=["python", "best-practices", "performance", "idioms"],
                cost="paid",
                author="Brett Slatkin",
                estimated_hours=50,
                prerequisites=["python-basics"]
            )
        ]
        
        # Online Courses
        courses = [
            LearningResource(
                title="Algorithms Specialization - Stanford",
                type=ResourceType.COURSE,
                url="https://coursera.org/specializations/algorithms",
                difficulty=DifficultyLevel.INTERMEDIATE,
                rating=4.8,
                description="4-course specialization covering divide-and-conquer, graph algorithms, greedy algorithms, and dynamic programming.",
                topics=["algorithms", "graph-theory", "dynamic-programming", "complexity-analysis"],
                cost="freemium",
                author="Tim Roughgarden",
                estimated_hours=80,
                prerequisites=["basic-programming", "mathematics"]
            ),
            LearningResource(
                title="Data Structures and Algorithms - UC San Diego",
                type=ResourceType.COURSE,
                url="https://coursera.org/specializations/data-structures-algorithms",
                difficulty=DifficultyLevel.INTERMEDIATE,
                rating=4.6,
                description="6-course specialization with hands-on programming assignments in multiple languages.",
                topics=["data-structures", "algorithms", "implementation", "problem-solving"],
                cost="freemium",
                author="UC San Diego",
                estimated_hours=120,
                prerequisites=["programming-experience"]
            ),
            LearningResource(
                title="Python for Everybody - University of Michigan",
                type=ResourceType.COURSE,
                url="https://coursera.org/specializations/python",
                difficulty=DifficultyLevel.BEGINNER,
                rating=4.8,
                description="Complete Python specialization from basics to data analysis.",
                topics=["python", "programming-fundamentals", "data-analysis"],
                cost="freemium",
                author="Charles Severance",
                estimated_hours=60,
                prerequisites=[]
            ),
            LearningResource(
                title="AlgoExpert",
                type=ResourceType.COURSE,
                url="https://algoexpert.io",
                difficulty=DifficultyLevel.INTERMEDIATE,
                rating=4.7,
                description="160+ coding interview questions with video explanations and optimal solutions.",
                topics=["interviews", "algorithms", "data-structures", "system-design"],
                cost="paid",
                author="Clement Mihailescu",
                estimated_hours=100,
                prerequisites=["programming-experience"]
            )
        ]
        
        # Practice Platforms
        practice_platforms = [
            LearningResource(
                title="LeetCode",
                type=ResourceType.PRACTICE,
                url="https://leetcode.com",
                difficulty=DifficultyLevel.INTERMEDIATE,
                rating=4.7,
                description="2000+ coding problems with detailed solutions. Popular for interview prep.",
                topics=["algorithms", "data-structures", "interviews", "contests"],
                cost="freemium",
                estimated_hours=500,
                prerequisites=["programming-basics"]
            ),
            LearningResource(
                title="HackerRank",
                type=ResourceType.PRACTICE,
                url="https://hackerrank.com",
                difficulty=DifficultyLevel.BEGINNER,
                rating=4.5,
                description="Skills-based coding challenges and interview preparation platform.",
                topics=["programming", "algorithms", "data-structures", "mathematics"],
                cost="freemium",
                estimated_hours=200,
                prerequisites=["basic-programming"]
            ),
            LearningResource(
                title="Codeforces",
                type=ResourceType.PRACTICE,
                url="https://codeforces.com",
                difficulty=DifficultyLevel.ADVANCED,
                rating=4.8,
                description="Competitive programming platform with regular contests.",
                topics=["competitive-programming", "algorithms", "mathematics"],
                cost="free",
                estimated_hours=1000,
                prerequisites=["strong-programming", "mathematics"]
            ),
            LearningResource(
                title="AtCoder",
                type=ResourceType.PRACTICE,
                url="https://atcoder.jp",
                difficulty=DifficultyLevel.INTERMEDIATE,
                rating=4.6,
                description="Japanese competitive programming platform with English support.",
                topics=["competitive-programming", "algorithms", "implementation"],
                cost="free",
                estimated_hours=300,
                prerequisites=["programming-experience"]
            ),
            LearningResource(
                title="CodeChef",
                type=ResourceType.PRACTICE,
                url="https://codechef.com",
                difficulty=DifficultyLevel.INTERMEDIATE,
                rating=4.4,
                description="Indian competitive programming platform with monthly contests.",
                topics=["competitive-programming", "algorithms", "data-structures"],
                cost="freemium",
                estimated_hours=200,
                prerequisites=["programming-basics"]
            )
        ]
        
        # Video Resources
        video_resources = [
            LearningResource(
                title="MIT 6.006 Introduction to Algorithms",
                type=ResourceType.VIDEO,
                url="https://youtube.com/playlist?list=PLUl4u3cNGP61Oq3tWYp6V_F-5jb5L2iHb",
                difficulty=DifficultyLevel.ADVANCED,
                rating=4.9,
                description="MIT's introductory algorithms course. Rigorous and comprehensive.",
                topics=["algorithms", "data-structures", "complexity-analysis"],
                cost="free",
                author="MIT OpenCourseWare",
                estimated_hours=40,
                prerequisites=["mathematics", "programming"]
            ),
            LearningResource(
                title="CS Dojo",
                type=ResourceType.VIDEO,
                url="https://youtube.com/c/CSDojo",
                difficulty=DifficultyLevel.BEGINNER,
                rating=4.6,
                description="Beginner-friendly programming and algorithm tutorials.",
                topics=["algorithms", "programming", "interviews", "python"],
                cost="free",
                author="YK Sugi",
                estimated_hours=50,
                prerequisites=["basic-programming"]
            ),
            LearningResource(
                title="Back to Back SWE",
                type=ResourceType.VIDEO,
                url="https://youtube.com/c/BackToBackSWE",
                difficulty=DifficultyLevel.INTERMEDIATE,
                rating=4.7,
                description="In-depth algorithm explanations for interview preparation.",
                topics=["algorithms", "interviews", "leetcode", "explanations"],
                cost="free",
                author="Ben Awad",
                estimated_hours=100,
                prerequisites=["programming-experience"]
            ),
            LearningResource(
                title="Abdul Bari Algorithms",
                type=ResourceType.VIDEO,
                url="https://youtube.com/watch?v=0IAPZzGSbME&list=PLDN4rrl48XKpZkf03iYFl-O29szjTrs_O",
                difficulty=DifficultyLevel.INTERMEDIATE,
                rating=4.8,
                description="Comprehensive algorithms course with clear explanations.",
                topics=["algorithms", "data-structures", "analysis"],
                cost="free",
                author="Abdul Bari",
                estimated_hours=80,
                prerequisites=["programming-basics"]
            )
        ]
        
        # Tools and Development Environment
        tools = [
            LearningResource(
                title="Visual Studio Code",
                type=ResourceType.TOOL,
                url="https://code.visualstudio.com",
                difficulty=DifficultyLevel.BEGINNER,
                rating=4.8,
                description="Free, powerful code editor with Python support and debugging.",
                topics=["development", "python", "debugging", "productivity"],
                cost="free",
                prerequisites=[]
            ),
            LearningResource(
                title="PyCharm Community Edition",
                type=ResourceType.TOOL,
                url="https://jetbrains.com/pycharm",
                difficulty=DifficultyLevel.BEGINNER,
                rating=4.7,
                description="Professional Python IDE with advanced debugging and refactoring.",
                topics=["development", "python", "debugging", "refactoring"],
                cost="freemium",
                prerequisites=[]
            ),
            LearningResource(
                title="Jupyter Notebook",
                type=ResourceType.TOOL,
                url="https://jupyter.org",
                difficulty=DifficultyLevel.BEGINNER,
                rating=4.6,
                description="Interactive computing environment perfect for learning and experimentation.",
                topics=["development", "data-science", "learning", "visualization"],
                cost="free",
                prerequisites=["python-basics"]
            ),
            LearningResource(
                title="Git",
                type=ResourceType.TOOL,
                url="https://git-scm.com",
                difficulty=DifficultyLevel.BEGINNER,
                rating=4.9,
                description="Version control system essential for software development.",
                topics=["version-control", "collaboration", "development"],
                cost="free",
                prerequisites=[]
            )
        ]
        
        # Communities and Forums
        communities = [
            LearningResource(
                title="r/Python",
                type=ResourceType.COMMUNITY,
                url="https://reddit.com/r/Python",
                difficulty=DifficultyLevel.BEGINNER,
                rating=4.6,
                description="Large Python community on Reddit with news, tutorials, and help.",
                topics=["python", "community", "help", "news"],
                cost="free",
                prerequisites=[]
            ),
            LearningResource(
                title="Stack Overflow",
                type=ResourceType.COMMUNITY,
                url="https://stackoverflow.com/questions/tagged/python",
                difficulty=DifficultyLevel.BEGINNER,
                rating=4.8,
                description="Programming Q&A site with millions of Python-related questions.",
                topics=["programming", "help", "problem-solving"],
                cost="free",
                prerequisites=[]
            ),
            LearningResource(
                title="Python Discord",
                type=ResourceType.COMMUNITY,
                url="https://discord.gg/python",
                difficulty=DifficultyLevel.BEGINNER,
                rating=4.5,
                description="Active Python community on Discord for real-time help and discussions.",
                topics=["python", "community", "real-time-help"],
                cost="free",
                prerequisites=[]
            ),
            LearningResource(
                title="Competitive Programming Discord",
                type=ResourceType.COMMUNITY,
                url="https://discord.gg/algorithms",
                difficulty=DifficultyLevel.INTERMEDIATE,
                rating=4.4,
                description="Community focused on competitive programming and algorithms.",
                topics=["competitive-programming", "algorithms", "contests"],
                cost="free",
                prerequisites=["programming-experience"]
            )
        ]
        
        # Add all resources
        self.resources.extend(books)
        self.resources.extend(courses)
        self.resources.extend(practice_platforms)
        self.resources.extend(video_resources)
        self.resources.extend(tools)
        self.resources.extend(communities)
    
    def get_resources_by_type(self, resource_type: ResourceType) -> List[LearningResource]:
        """Get resources filtered by type."""
        return [r for r in self.resources if r.type == resource_type]
    
    def get_resources_by_difficulty(self, difficulty: DifficultyLevel) -> List[LearningResource]:
        """Get resources filtered by difficulty."""
        return [r for r in self.resources if r.difficulty == difficulty]
    
    def get_free_resources(self) -> List[LearningResource]:
        """Get only free resources."""
        return [r for r in self.resources if r.cost == "free"]
    
    def get_resources_by_topic(self, topic: str) -> List[LearningResource]:
        """Get resources that cover a specific topic."""
        return [r for r in self.resources if topic.lower() in [t.lower() for t in r.topics]]
    
    def search_resources(self, query: str) -> List[LearningResource]:
        """Search resources by title, description, or topics."""
        query = query.lower()
        results = []
        
        for resource in self.resources:
            if (query in resource.title.lower() or 
                query in resource.description.lower() or
                any(query in topic.lower() for topic in resource.topics) or
                query in resource.author.lower()):
                results.append(resource)
        
        return results
    
    def get_top_rated(self, limit: int = 10) -> List[LearningResource]:
        """Get top-rated resources."""
        return sorted(self.resources, key=lambda r: r.rating, reverse=True)[:limit]
    
    def get_beginner_path(self) -> List[LearningResource]:
        """Get recommended learning path for beginners."""
        beginner_resources = self.get_resources_by_difficulty(DifficultyLevel.BEGINNER)
        return sorted(beginner_resources, key=lambda r: r.estimated_hours)
    
    def export_to_json(self, filename: str):
        """Export resources to JSON file."""
        data = {
            "resources": [r.to_dict() for r in self.resources],
            "export_date": datetime.datetime.now().isoformat(),
            "total_count": len(self.resources)
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


class StudyPlan:
    """Create and track personalized study plans."""
    
    def __init__(self, name: str):
        self.name = name
        self.resources: List[LearningResource] = []
        self.completed_resources: List[str] = []
        self.start_date = datetime.date.today()
        self.target_date: Optional[datetime.date] = None
        self.daily_hours = 2.0
    
    def add_resource(self, resource: LearningResource):
        """Add a resource to the study plan."""
        self.resources.append(resource)
    
    def mark_completed(self, resource_title: str):
        """Mark a resource as completed."""
        if resource_title not in self.completed_resources:
            self.completed_resources.append(resource_title)
    
    def get_progress(self) -> Dict[str, Any]:
        """Get study plan progress."""
        total_resources = len(self.resources)
        completed_count = len(self.completed_resources)
        
        total_hours = sum(r.estimated_hours for r in self.resources)
        completed_hours = sum(
            r.estimated_hours for r in self.resources 
            if r.title in self.completed_resources
        )
        
        progress_percentage = (completed_count / total_resources * 100) if total_resources > 0 else 0
        hours_percentage = (completed_hours / total_hours * 100) if total_hours > 0 else 0
        
        days_elapsed = (datetime.date.today() - self.start_date).days
        estimated_completion_days = total_hours / self.daily_hours if self.daily_hours > 0 else 0
        
        return {
            "name": self.name,
            "total_resources": total_resources,
            "completed_resources": completed_count,
            "progress_percentage": progress_percentage,
            "total_hours": total_hours,
            "completed_hours": completed_hours,
            "hours_percentage": hours_percentage,
            "days_elapsed": days_elapsed,
            "estimated_completion_days": estimated_completion_days,
            "daily_hours": self.daily_hours
        }
    
    def get_next_resources(self, count: int = 3) -> List[LearningResource]:
        """Get next resources to study."""
        uncompleted = [
            r for r in self.resources 
            if r.title not in self.completed_resources
        ]
        return uncompleted[:count]


class LearningPathGenerator:
    """Generate personalized learning paths based on goals."""
    
    def __init__(self, catalog: ResourceCatalog):
        self.catalog = catalog
    
    def create_interview_prep_path(self, experience_level: DifficultyLevel) -> StudyPlan:
        """Create an interview preparation study plan."""
        plan = StudyPlan("Technical Interview Preparation")
        
        if experience_level == DifficultyLevel.BEGINNER:
            # Start with fundamentals
            python_resources = self.catalog.get_resources_by_topic("python")
            plan.add_resource(python_resources[2])  # Python for Everybody
            
            beginner_books = [r for r in self.catalog.get_resources_by_type(ResourceType.BOOK) 
                            if r.difficulty == DifficultyLevel.BEGINNER]
            if beginner_books:
                plan.add_resource(beginner_books[0])  # Grokking Algorithms
        
        # Add intermediate resources
        interview_resources = self.catalog.get_resources_by_topic("interviews")
        for resource in interview_resources:
            if resource.difficulty in [DifficultyLevel.INTERMEDIATE, experience_level]:
                plan.add_resource(resource)
        
        # Add practice platform
        leetcode = next((r for r in self.catalog.resources if r.title == "LeetCode"), None)
        if leetcode:
            plan.add_resource(leetcode)
        
        return plan
    
    def create_competitive_programming_path(self) -> StudyPlan:
        """Create a competitive programming study plan."""
        plan = StudyPlan("Competitive Programming Mastery")
        
        # Add algorithm course
        mit_course = next((r for r in self.catalog.resources 
                          if "MIT" in r.title), None)
        if mit_course:
            plan.add_resource(mit_course)
        
        # Add practice platforms
        competitive_platforms = ["Codeforces", "AtCoder", "CodeChef"]
        for platform_name in competitive_platforms:
            platform = next((r for r in self.catalog.resources 
                           if r.title == platform_name), None)
            if platform:
                plan.add_resource(platform)
        
        return plan
    
    def create_python_mastery_path(self) -> StudyPlan:
        """Create a Python mastery study plan."""
        plan = StudyPlan("Python Mastery")
        
        # Add Python-specific resources
        python_resources = self.catalog.get_resources_by_topic("python")
        for resource in python_resources:
            plan.add_resource(resource)
        
        return plan


def demonstrate_resource_catalog():
    """Demonstrate the resource catalog functionality."""
    print("Learning Resources Catalog")
    print("=" * 40)
    
    catalog = ResourceCatalog()
    
    # Show statistics
    total_resources = len(catalog.resources)
    free_resources = len(catalog.get_free_resources())
    
    print(f"\nTotal Resources: {total_resources}")
    print(f"Free Resources: {free_resources}")
    print(f"Resource Types:")
    
    for resource_type in ResourceType:
        count = len(catalog.get_resources_by_type(resource_type))
        print(f"  {resource_type.value.title()}: {count}")
    
    # Show top-rated resources
    print(f"\nTop 5 Rated Resources:")
    top_resources = catalog.get_top_rated(5)
    for i, resource in enumerate(top_resources, 1):
        print(f"  {i}. {resource.title} ({resource.rating}/5.0) - {resource.type.value}")
    
    # Show free resources by type
    print(f"\nFree Resources by Type:")
    free_resources = catalog.get_free_resources()
    by_type = defaultdict(list)
    
    for resource in free_resources:
        by_type[resource.type].append(resource.title)
    
    for resource_type, titles in by_type.items():
        print(f"  {resource_type.value.title()}: {len(titles)} resources")
    
    # Search example
    print(f"\nSearch Results for 'algorithm':")
    search_results = catalog.search_resources("algorithm")
    for resource in search_results[:3]:
        print(f"  - {resource.title} ({resource.type.value})")
    
    # Beginner path
    print(f"\nBeginner Learning Path:")
    beginner_path = catalog.get_beginner_path()
    for resource in beginner_path[:3]:
        print(f"  1. {resource.title} (~{resource.estimated_hours}h)")


def demonstrate_study_plans():
    """Demonstrate study plan creation and tracking."""
    print("\n\nStudy Plan Management")
    print("=" * 30)
    
    catalog = ResourceCatalog()
    path_generator = LearningPathGenerator(catalog)
    
    # Create interview prep plan
    interview_plan = path_generator.create_interview_prep_path(DifficultyLevel.INTERMEDIATE)
    
    print(f"Created study plan: {interview_plan.name}")
    print(f"Resources in plan: {len(interview_plan.resources)}")
    
    # Simulate some progress
    if interview_plan.resources:
        interview_plan.mark_completed(interview_plan.resources[0].title)
        if len(interview_plan.resources) > 1:
            interview_plan.mark_completed(interview_plan.resources[1].title)
    
    # Show progress
    progress = interview_plan.get_progress()
    print(f"\nProgress Report:")
    print(f"  Completed: {progress['completed_resources']}/{progress['total_resources']} resources")
    print(f"  Progress: {progress['progress_percentage']:.1f}%")
    print(f"  Hours completed: {progress['completed_hours']}/{progress['total_hours']}")
    print(f"  Days elapsed: {progress['days_elapsed']}")
    
    # Show next resources
    next_resources = interview_plan.get_next_resources(2)
    print(f"\nNext Resources to Study:")
    for i, resource in enumerate(next_resources, 1):
        print(f"  {i}. {resource.title} (~{resource.estimated_hours}h)")


def generate_learning_recommendations():
    """Generate personalized learning recommendations."""
    print("\n\nPersonalized Learning Recommendations")
    print("=" * 45)
    
    catalog = ResourceCatalog()
    
    # Simulate user preferences
    user_preferences = {
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "interests": ["algorithms", "interviews", "python"],
        "budget": "freemium",  # free, paid, freemium
        "time_per_day": 2,  # hours
        "learning_style": "video"  # book, video, practice, course
    }
    
    print(f"User Preferences:")
    for key, value in user_preferences.items():
        print(f"  {key}: {value}")
    
    # Filter recommendations based on preferences
    recommendations = []
    
    for interest in user_preferences["interests"]:
        topic_resources = catalog.get_resources_by_topic(interest)
        
        # Filter by difficulty and cost
        filtered = [
            r for r in topic_resources
            if (r.difficulty == user_preferences["difficulty"] and
                r.cost in ["free", user_preferences["budget"]])
        ]
        
        # Prefer user's learning style
        learning_style_match = [
            r for r in filtered
            if (user_preferences["learning_style"] == "video" and r.type == ResourceType.VIDEO) or
               (user_preferences["learning_style"] == "book" and r.type == ResourceType.BOOK) or
               (user_preferences["learning_style"] == "practice" and r.type == ResourceType.PRACTICE) or
               (user_preferences["learning_style"] == "course" and r.type == ResourceType.COURSE)
        ]
        
        recommendations.extend(learning_style_match)
        recommendations.extend(filtered[:2])  # Add other good matches
    
    # Remove duplicates and sort by rating
    unique_recommendations = []
    seen_titles = set()
    
    for rec in recommendations:
        if rec.title not in seen_titles:
            unique_recommendations.append(rec)
            seen_titles.add(rec.title)
    
    unique_recommendations.sort(key=lambda r: r.rating, reverse=True)
    
    print(f"\nTop Recommendations:")
    for i, resource in enumerate(unique_recommendations[:5], 1):
        cost_indicator = "💰" if resource.cost == "paid" else "🆓" if resource.cost == "free" else "🔄"
        print(f"  {i}. {resource.title} {cost_indicator}")
        print(f"     {resource.description[:100]}...")
        print(f"     Topics: {', '.join(resource.topics[:3])}")
        print(f"     Time: ~{resource.estimated_hours}h | Rating: {resource.rating}/5.0")
        print()


def export_resources():
    """Export resources to JSON file."""
    print("\nExporting Resources")
    print("=" * 20)
    
    catalog = ResourceCatalog()
    filename = "learning_resources_export.json"
    catalog.export_to_json(filename)
    
    print(f"Exported {len(catalog.resources)} resources to {filename}")
    
    # Show export structure
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Export contains:")
    print(f"  - {data['total_count']} total resources")
    print(f"  - Export date: {data['export_date']}")
    print(f"  - File size: {len(json.dumps(data))} characters")


def main():
    """Main function to demonstrate learning resources."""
    print("Python DSA Master - Learning Resources & Study Guide")
    print("=" * 60)
    
    try:
        demonstrate_resource_catalog()
        demonstrate_study_plans()
        generate_learning_recommendations()
        export_resources()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*60}")
    print("Learning resources demonstration complete!")


if __name__ == "__main__":
    main()


# ============================================================================
# ADDITIONAL LEARNING RESOURCES AND STUDY TIPS
# ============================================================================

"""
📚 COMPREHENSIVE LEARNING ROADMAP:

🎯 BEGINNER PATH (0-6 months):
1. Python Fundamentals
   - "Python Crash Course" or "Automate the Boring Stuff"
   - Python for Everybody (Coursera)
   - Practice: HackerRank Python domain

2. Basic Data Structures
   - "Grokking Algorithms" book
   - CS Dojo YouTube channel
   - Practice: LeetCode Easy problems

3. Problem Solving
   - "Think Like a Programmer" concepts
   - Simple algorithm implementations
   - Pattern recognition practice

🚀 INTERMEDIATE PATH (6-12 months):
1. Advanced Data Structures
   - Trees, Graphs, Hash Tables
   - "Elements of Programming Interviews"
   - Practice: LeetCode Medium problems

2. Core Algorithms
   - Sorting, Searching, Graph algorithms
   - Dynamic Programming basics
   - Time/Space complexity analysis

3. Interview Preparation
   - "Cracking the Coding Interview"
   - Mock interview practice
   - System design basics

⚡ ADVANCED PATH (12+ months):
1. Advanced Algorithms
   - "Introduction to Algorithms" (CLRS)
   - MIT 6.006 and 6.046 courses
   - Competitive programming

2. System Design
   - "Designing Data-Intensive Applications"
   - High-level system architecture
   - Scalability patterns

3. Specialization
   - Machine Learning algorithms
   - Distributed systems
   - Domain-specific optimization

🏆 COMPETITIVE PROGRAMMING:
• Platforms: Codeforces, AtCoder, TopCoder
• Practice: 3-4 problems daily
• Focus: Speed + accuracy
• Study: Editorial solutions

💼 INTERVIEW PREPARATION:
• Timeline: 3-6 months dedicated prep
• Practice: 150-300 problems minimum
• Mock interviews: Weekly practice
• System design: 10+ case studies

📈 PROGRESS TRACKING:
• Daily coding practice (1-2 hours)
• Weekly progress reviews
• Monthly skill assessments
• Problem-solving journal

🛠️ ESSENTIAL TOOLS:
• IDE: VS Code / PyCharm
• Version Control: Git
• Visualization: Python Tutor
• Performance: cProfile, memory_profiler
• Testing: pytest

🌐 COMMUNITIES TO JOIN:
• r/Python, r/cscareerquestions
• Discord: Python, Competitive Programming
• Local: Python meetups, coding groups
• Online: Stack Overflow, GeeksforGeeks

💡 STUDY TIPS:
• Spaced repetition for problem patterns
• Active recall vs passive reading
• Teach others to reinforce learning
• Build projects to apply concepts
• Review and analyze mistakes

📊 SUCCESS METRICS:
• Problems solved per week
• Interview success rate
• Code quality improvements
• Time to solve problems
• Understanding depth

🎯 CAREER GOALS:
• Entry Level: 50+ LeetCode problems
• Mid Level: 200+ problems + system design
• Senior Level: Advanced algorithms + architecture
• Principal: Research + innovation

Remember: Consistency beats intensity. 
Daily practice for 1 hour is better than 7 hours once a week!
"""
