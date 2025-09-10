#!/usr/bin/env python3
"""
Online Courses and Tutorials Reference Guide

This module provides a comprehensive catalog of online courses, tutorials, and
educational platforms for learning data structures, algorithms, and Python programming.
Includes ratings, reviews, and personalized course recommendations.

Features:
- Curated collection of online courses and tutorials
- Platform-specific course catalogs (Coursera, edX, Udemy, etc.)
- Instructor profiles and credibility assessment  
- Course difficulty progression and prerequisites
- Interactive learning path generation
- Cost analysis and scholarship information

Author: Python DSA Master
Date: 2024
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from enum import Enum
import json
import datetime
from collections import defaultdict


class Platform(Enum):
    """Online learning platforms."""
    COURSERA = "coursera"
    EDX = "edx"
    UDEMY = "udemy"
    UDACITY = "udacity"
    PLURALSIGHT = "pluralsight"
    LINKEDIN_LEARNING = "linkedin_learning"
    CODECADEMY = "codecademy"
    YOUTUBE = "youtube"
    MIT_OCW = "mit_ocw"
    STANFORD_ONLINE = "stanford_online"
    FREECODECAMP = "freecodecamp"
    KHAN_ACADEMY = "khan_academy"
    ALGOEXPERT = "algoexpert"
    LEETCODE = "leetcode"


class CourseType(Enum):
    """Types of online courses."""
    FULL_COURSE = "full_course"
    SPECIALIZATION = "specialization"
    TUTORIAL_SERIES = "tutorial_series"
    BOOTCAMP = "bootcamp"
    WORKSHOP = "workshop"
    LECTURE_SERIES = "lecture_series"
    INTERACTIVE = "interactive"


class DifficultyLevel(Enum):
    """Course difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class CourseCategory(Enum):
    """Course categories by topic."""
    PYTHON_FUNDAMENTALS = "python_fundamentals"
    DATA_STRUCTURES = "data_structures"
    ALGORITHMS = "algorithms"
    INTERVIEW_PREP = "interview_prep"
    COMPETITIVE_PROGRAMMING = "competitive_programming"
    SYSTEM_DESIGN = "system_design"
    SOFTWARE_ENGINEERING = "software_engineering"
    WEB_DEVELOPMENT = "web_development"
    DATA_SCIENCE = "data_science"
    MACHINE_LEARNING = "machine_learning"


@dataclass
class Instructor:
    """Course instructor information."""
    name: str
    credentials: List[str] = field(default_factory=list)
    affiliations: List[str] = field(default_factory=list)
    experience_years: int = 0
    specializations: List[str] = field(default_factory=list)
    rating: float = 0.0
    courses_taught: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "credentials": self.credentials,
            "affiliations": self.affiliations,
            "experience_years": self.experience_years,
            "specializations": self.specializations,
            "rating": self.rating,
            "courses_taught": self.courses_taught
        }


@dataclass
class CourseReview:
    """Detailed course review and analysis."""
    overall_rating: float  # 1-5 scale
    content_quality: float
    instruction_quality: float
    practical_value: float
    difficulty_accuracy: float
    
    total_reviews: int = 0
    completion_rate: float = 0.0
    
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    best_for: List[str] = field(default_factory=list)
    avoid_if: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_rating": self.overall_rating,
            "content_quality": self.content_quality,
            "instruction_quality": self.instruction_quality,
            "practical_value": self.practical_value,
            "difficulty_accuracy": self.difficulty_accuracy,
            "total_reviews": self.total_reviews,
            "completion_rate": self.completion_rate,
            "pros": self.pros,
            "cons": self.cons,
            "best_for": self.best_for,
            "avoid_if": self.avoid_if
        }


@dataclass
class Course:
    """Comprehensive course information."""
    title: str
    platform: Platform
    course_type: CourseType
    category: CourseCategory
    difficulty: DifficultyLevel
    instructors: List[Instructor]
    
    url: str = ""
    description: str = ""
    duration_hours: int = 0
    duration_weeks: int = 0
    
    key_topics: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    learning_outcomes: List[str] = field(default_factory=list)
    
    price: str = ""  # "Free", "$49", "$39/month", etc.
    financial_aid: bool = False
    certificate_available: bool = False
    
    language: str = "English"
    subtitles: List[str] = field(default_factory=list)
    
    review: Optional[CourseReview] = None
    enrollment_count: int = 0
    last_updated: str = ""
    
    assignments: bool = False
    projects: bool = False
    quizzes: bool = False
    peer_review: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "platform": self.platform.value,
            "course_type": self.course_type.value,
            "category": self.category.value,
            "difficulty": self.difficulty.value,
            "instructors": [instructor.to_dict() for instructor in self.instructors],
            "url": self.url,
            "description": self.description,
            "duration_hours": self.duration_hours,
            "duration_weeks": self.duration_weeks,
            "key_topics": self.key_topics,
            "prerequisites": self.prerequisites,
            "learning_outcomes": self.learning_outcomes,
            "price": self.price,
            "financial_aid": self.financial_aid,
            "certificate_available": self.certificate_available,
            "language": self.language,
            "subtitles": self.subtitles,
            "review": self.review.to_dict() if self.review else None,
            "enrollment_count": self.enrollment_count,
            "last_updated": self.last_updated,
            "assignments": self.assignments,
            "projects": self.projects,
            "quizzes": self.quizzes,
            "peer_review": self.peer_review
        }


class CoursesCatalog:
    """Comprehensive catalog of online courses and tutorials."""
    
    def __init__(self):
        self.courses: List[Course] = []
        self._initialize_courses()
    
    def _initialize_courses(self):
        """Initialize course catalog with curated courses."""
        
        # Create instructor profiles
        tim_roughgarden = Instructor(
            name="Tim Roughgarden",
            credentials=["PhD Computer Science, Cornell University", "Professor at Stanford"],
            affiliations=["Stanford University"],
            experience_years=20,
            specializations=["Algorithms", "Game Theory", "Computer Science Theory"],
            rating=4.8,
            courses_taught=8
        )
        
        robert_sedgewick = Instructor(
            name="Robert Sedgewick",
            credentials=["PhD Computer Science, Stanford University", "Professor at Princeton"],
            affiliations=["Princeton University"],
            experience_years=40,
            specializations=["Algorithms", "Data Structures", "Computer Science"],
            rating=4.7,
            courses_taught=6
        )
        
        charles_severance = Instructor(
            name="Charles Severance",
            credentials=["PhD Computer Science", "Clinical Professor"],
            affiliations=["University of Michigan"],
            experience_years=25,
            specializations=["Python", "Web Development", "Education Technology"],
            rating=4.9,
            courses_taught=15
        )
        
        # Essential Courses
        courses = [
            # Stanford Algorithms Specialization
            Course(
                title="Algorithms Specialization",
                platform=Platform.COURSERA,
                course_type=CourseType.SPECIALIZATION,
                category=CourseCategory.ALGORITHMS,
                difficulty=DifficultyLevel.INTERMEDIATE,
                instructors=[tim_roughgarden],
                url="https://www.coursera.org/specializations/algorithms",
                description="Four-course series covering the essential information that every serious programmer needs to know about algorithms and data structures.",
                duration_hours=80,
                duration_weeks=16,
                key_topics=[
                    "Asymptotic Analysis", "Divide and Conquer Algorithms", "Sorting and Selection",
                    "Data Structures", "Graph Search", "Shortest Paths", "Hash Tables",
                    "Dynamic Programming", "Greedy Algorithms", "Network Flows", "Linear Programming"
                ],
                prerequisites=["Basic programming experience", "Mathematical maturity"],
                learning_outcomes=[
                    "Master fundamental algorithms and data structures",
                    "Analyze algorithm efficiency using Big O notation",
                    "Implement classic algorithms from scratch",
                    "Apply algorithmic thinking to solve complex problems"
                ],
                price="$39-79/month",
                financial_aid=True,
                certificate_available=True,
                review=CourseReview(
                    overall_rating=4.8,
                    content_quality=4.9,
                    instruction_quality=4.8,
                    practical_value=4.7,
                    difficulty_accuracy=4.6,
                    total_reviews=12000,
                    completion_rate=0.65,
                    pros=[
                        "Excellent theoretical foundation",
                        "World-class instructor",
                        "Comprehensive coverage of algorithms",
                        "Mathematical rigor with practical examples",
                        "High-quality video production"
                    ],
                    cons=[
                        "Mathematical heavy for some beginners",
                        "Limited programming assignments",
                        "Fast-paced for newcomers",
                        "Requires strong math background"
                    ],
                    best_for=[
                        "CS students and graduates",
                        "Software engineers seeking algorithmic depth",
                        "Interview preparation for top tech companies",
                        "Those comfortable with mathematical analysis"
                    ],
                    avoid_if=[
                        "Complete programming beginner",
                        "Weak mathematical background",
                        "Looking for hands-on coding focus"
                    ]
                ),
                enrollment_count=500000,
                last_updated="2023",
                assignments=True,
                projects=True,
                quizzes=True,
                peer_review=False
            ),
            
            # Python for Everybody
            Course(
                title="Python for Everybody Specialization",
                platform=Platform.COURSERA,
                course_type=CourseType.SPECIALIZATION,
                category=CourseCategory.PYTHON_FUNDAMENTALS,
                difficulty=DifficultyLevel.BEGINNER,
                instructors=[charles_severance],
                url="https://www.coursera.org/specializations/python",
                description="Learn to Program and Analyze Data with Python. Develop programs to gather, clean, analyze, and visualize data.",
                duration_hours=60,
                duration_weeks=12,
                key_topics=[
                    "Python Syntax and Semantics", "Data Structures", "Networked Programs",
                    "Database Programming", "Data Visualization", "Web Scraping",
                    "Regular Expressions", "Object-Oriented Programming"
                ],
                prerequisites=["No programming experience required"],
                learning_outcomes=[
                    "Master Python programming fundamentals",
                    "Build data analysis and visualization programs",
                    "Work with databases and web APIs",
                    "Create networked applications"
                ],
                price="$39-79/month",
                financial_aid=True,
                certificate_available=True,
                review=CourseReview(
                    overall_rating=4.8,
                    content_quality=4.7,
                    instruction_quality=4.9,
                    practical_value=4.8,
                    difficulty_accuracy=4.8,
                    total_reviews=45000,
                    completion_rate=0.72,
                    pros=[
                        "Excellent for complete beginners",
                        "Clear and engaging instruction",
                        "Practical real-world projects",
                        "Strong community support",
                        "Comprehensive Python coverage"
                    ],
                    cons=[
                        "May be too slow for experienced programmers",
                        "Limited advanced Python topics",
                        "Basic web development coverage"
                    ],
                    best_for=[
                        "Complete programming beginners",
                        "Those wanting practical Python skills",
                        "Career changers to tech",
                        "Students seeking comprehensive introduction"
                    ],
                    avoid_if=[
                        "Already have Python experience",
                        "Looking for advanced topics",
                        "Need algorithm-focused content"
                    ]
                ),
                enrollment_count=800000,
                last_updated="2023",
                assignments=True,
                projects=True,
                quizzes=True,
                peer_review=True
            ),
            
            # Princeton Algorithms Course
            Course(
                title="Algorithms, Part I",
                platform=Platform.COURSERA,
                course_type=CourseType.FULL_COURSE,
                category=CourseCategory.ALGORITHMS,
                difficulty=DifficultyLevel.INTERMEDIATE,
                instructors=[robert_sedgewick],
                url="https://www.coursera.org/learn/algorithms-part1",
                description="Essential information that every serious programmer needs to know about algorithms and data structures, with emphasis on applications and scientific performance analysis.",
                duration_hours=54,
                duration_weeks=6,
                key_topics=[
                    "Union-Find", "Analysis of Algorithms", "Stacks and Queues",
                    "Elementary Sorts", "Mergesort", "Quicksort", "Priority Queues",
                    "Binary Heaps", "Symbol Tables", "Binary Search Trees", "Balanced Search Trees",
                    "Hash Tables", "Symbol Table Applications"
                ],
                prerequisites=["Programming experience in Java or similar language", "High school mathematics"],
                learning_outcomes=[
                    "Implement fundamental data structures",
                    "Master sorting and searching algorithms",
                    "Analyze algorithm performance",
                    "Apply algorithms to solve practical problems"
                ],
                price="$39-79/month",
                financial_aid=True,
                certificate_available=True,
                review=CourseReview(
                    overall_rating=4.9,
                    content_quality=4.9,
                    instruction_quality=4.8,
                    practical_value=4.7,
                    difficulty_accuracy=4.7,
                    total_reviews=25000,
                    completion_rate=0.58,
                    pros=[
                        "Excellent practical implementation focus",
                        "High-quality programming assignments",
                        "Clear explanations with visual aids",
                        "Industry-relevant algorithms",
                        "Strong emphasis on performance analysis"
                    ],
                    cons=[
                        "Java-focused (though concepts translate)",
                        "Requires significant time investment",
                        "Challenging programming assignments",
                        "Less theoretical than Stanford course"
                    ],
                    best_for=[
                        "Programmers wanting practical algorithm skills",
                        "Those preparing for technical interviews",
                        "Software engineers seeking implementation depth",
                        "Students comfortable with programming"
                    ],
                    avoid_if=[
                        "Prefer theoretical approach",
                        "Not comfortable with Java",
                        "Looking for Python-specific content"
                    ]
                ),
                enrollment_count=400000,
                last_updated="2023",
                assignments=True,
                projects=True,
                quizzes=True,
                peer_review=False
            ),
            
            # MIT Introduction to Computer Science
            Course(
                title="Introduction to Computer Science and Programming Using Python",
                platform=Platform.EDX,
                course_type=CourseType.FULL_COURSE,
                category=CourseCategory.PYTHON_FUNDAMENTALS,
                difficulty=DifficultyLevel.BEGINNER,
                instructors=[
                    Instructor(
                        name="Eric Grimson",
                        credentials=["PhD", "MIT Professor"],
                        affiliations=["MIT"],
                        specializations=["Computer Science Education", "Algorithms"],
                        rating=4.7
                    )
                ],
                url="https://www.edx.org/course/introduction-to-computer-science-and-programming-7",
                description="An introduction to computer science as a tool to solve real-world analytical problems using Python 3.5.",
                duration_hours=45,
                duration_weeks=9,
                key_topics=[
                    "Computational Thinking", "Python Programming", "Data Structures",
                    "Algorithms", "Testing and Debugging", "Complexity Analysis",
                    "Object-Oriented Programming", "Problem Solving"
                ],
                prerequisites=["High school mathematics", "No programming experience required"],
                learning_outcomes=[
                    "Think computationally and solve problems systematically",
                    "Write small programs in Python",
                    "Understand basic algorithms and data structures",
                    "Test and debug programs effectively"
                ],
                price="Free (Verified certificate: $99)",
                financial_aid=True,
                certificate_available=True,
                review=CourseReview(
                    overall_rating=4.6,
                    content_quality=4.7,
                    instruction_quality=4.5,
                    practical_value=4.6,
                    difficulty_accuracy=4.4,
                    total_reviews=8000,
                    completion_rate=0.45,
                    pros=[
                        "MIT-quality education for free",
                        "Strong computational thinking focus",
                        "Rigorous problem-solving approach",
                        "Excellent introduction to CS concepts"
                    ],
                    cons=[
                        "Can be challenging for complete beginners",
                        "Less engaging than some alternatives",
                        "Heavy reading requirements",
                        "Limited interactive elements"
                    ],
                    best_for=[
                        "Serious learners wanting rigorous foundation",
                        "Those planning to pursue CS degree",
                        "Students comfortable with self-paced learning"
                    ],
                    avoid_if=[
                        "Looking for light introduction",
                        "Prefer highly interactive content",
                        "Need immediate practical applications"
                    ]
                ),
                enrollment_count=150000,
                last_updated="2023",
                assignments=True,
                projects=True,
                quizzes=True,
                peer_review=False
            ),
            
            # YouTube Series - CS Dojo
            Course(
                title="Data Structures and Algorithms",
                platform=Platform.YOUTUBE,
                course_type=CourseType.TUTORIAL_SERIES,
                category=CourseCategory.ALGORITHMS,
                difficulty=DifficultyLevel.BEGINNER,
                instructors=[
                    Instructor(
                        name="YK Sugi (CS Dojo)",
                        credentials=["Former Google Software Engineer"],
                        affiliations=["Google (former)"],
                        specializations=["Algorithms", "Interview Preparation"],
                        rating=4.6
                    )
                ],
                url="https://www.youtube.com/c/CSDojo",
                description="Beginner-friendly explanations of data structures and algorithms with coding examples.",
                duration_hours=20,
                duration_weeks=4,
                key_topics=[
                    "Arrays", "Linked Lists", "Stacks", "Queues", "Trees",
                    "Hash Tables", "Sorting Algorithms", "Search Algorithms",
                    "Dynamic Programming", "Graph Algorithms"
                ],
                prerequisites=["Basic programming knowledge"],
                learning_outcomes=[
                    "Understand fundamental data structures",
                    "Implement basic algorithms",
                    "Prepare for coding interviews",
                    "Develop problem-solving skills"
                ],
                price="Free",
                financial_aid=False,
                certificate_available=False,
                review=CourseReview(
                    overall_rating=4.5,
                    content_quality=4.3,
                    instruction_quality=4.6,
                    practical_value=4.5,
                    difficulty_accuracy=4.7,
                    total_reviews=5000,
                    completion_rate=0.85,
                    pros=[
                        "Completely free and accessible",
                        "Clear, beginner-friendly explanations",
                        "Good interview preparation focus",
                        "Short, digestible videos"
                    ],
                    cons=[
                        "Limited depth on advanced topics",
                        "No structured curriculum",
                        "No assignments or projects",
                        "Inconsistent video quality"
                    ],
                    best_for=[
                        "Complete beginners to algorithms",
                        "Visual learners",
                        "Those on tight budgets",
                        "Interview preparation beginners"
                    ],
                    avoid_if=[
                        "Need comprehensive structured course",
                        "Want hands-on projects",
                        "Seeking advanced algorithmic topics"
                    ]
                ),
                enrollment_count=200000,
                last_updated="2023",
                assignments=False,
                projects=False,
                quizzes=False,
                peer_review=False
            ),
            
            # AlgoExpert
            Course(
                title="AlgoExpert - Coding Interview Preparation",
                platform=Platform.ALGOEXPERT,
                course_type=CourseType.INTERACTIVE,
                category=CourseCategory.INTERVIEW_PREP,
                difficulty=DifficultyLevel.INTERMEDIATE,
                instructors=[
                    Instructor(
                        name="Clement Mihailescu",
                        credentials=["Former Google Software Engineer", "Former Facebook Software Engineer"],
                        affiliations=["AlgoExpert"],
                        specializations=["Algorithms", "System Design", "Interview Preparation"],
                        rating=4.7
                    )
                ],
                url="https://www.algoexpert.io",
                description="160+ coding interview questions with detailed video explanations and optimal solutions.",
                duration_hours=100,
                duration_weeks=12,
                key_topics=[
                    "Array Problems", "String Manipulation", "Linked Lists", "Binary Trees",
                    "Dynamic Programming", "Graph Algorithms", "Sorting Algorithms",
                    "Searching", "Recursion", "System Design"
                ],
                prerequisites=["Solid programming fundamentals", "Basic data structures knowledge"],
                learning_outcomes=[
                    "Master coding interview question patterns",
                    "Develop optimal solution thinking",
                    "Improve problem-solving speed",
                    "Understand system design fundamentals"
                ],
                price="$99-159 (one-time)",
                financial_aid=False,
                certificate_available=False,
                review=CourseReview(
                    overall_rating=4.7,
                    content_quality=4.8,
                    instruction_quality=4.7,
                    practical_value=4.9,
                    difficulty_accuracy=4.6,
                    total_reviews=3000,
                    completion_rate=0.70,
                    pros=[
                        "Excellent interview preparation focus",
                        "High-quality video explanations",
                        "Optimal solutions with multiple approaches",
                        "System design content included",
                        "Interactive coding environment"
                    ],
                    cons=[
                        "Expensive compared to other options",
                        "Limited to interview preparation",
                        "Not suitable for learning fundamentals",
                        "Can feel repetitive for experienced developers"
                    ],
                    best_for=[
                        "Software engineers preparing for FAANG interviews",
                        "Those wanting structured interview prep",
                        "Developers seeking optimal solution patterns",
                        "Anyone serious about coding interviews"
                    ],
                    avoid_if=[
                        "Complete beginner to programming",
                        "Not interested in interviews",
                        "Looking for comprehensive CS education",
                        "Budget-conscious learners"
                    ]
                ),
                enrollment_count=50000,
                last_updated="2024",
                assignments=True,
                projects=False,
                quizzes=True,
                peer_review=False
            )
        ]
        
        self.courses.extend(courses)
    
    def get_courses_by_platform(self, platform: Platform) -> List[Course]:
        """Get courses filtered by platform."""
        return [course for course in self.courses if course.platform == platform]
    
    def get_courses_by_category(self, category: CourseCategory) -> List[Course]:
        """Get courses filtered by category."""
        return [course for course in self.courses if course.category == category]
    
    def get_courses_by_difficulty(self, difficulty: DifficultyLevel) -> List[Course]:
        """Get courses filtered by difficulty level."""
        return [course for course in self.courses if course.difficulty == difficulty]
    
    def get_free_courses(self) -> List[Course]:
        """Get only free courses."""
        return [course for course in self.courses if "free" in course.price.lower()]
    
    def get_top_rated_courses(self, limit: int = 10) -> List[Course]:
        """Get top-rated courses."""
        rated_courses = [course for course in self.courses if course.review]
        return sorted(rated_courses, key=lambda c: c.review.overall_rating, reverse=True)[:limit]
    
    def search_courses(self, query: str) -> List[Course]:
        """Search courses by title, description, or topics."""
        query_lower = query.lower()
        results = []
        
        for course in self.courses:
            if (query_lower in course.title.lower() or
                query_lower in course.description.lower() or
                any(query_lower in topic.lower() for topic in course.key_topics)):
                results.append(course)
        
        return results
    
    def get_learning_path(self, goal: str) -> List[Course]:
        """Generate learning path for specific goals."""
        if goal == "python_beginner":
            return [
                course for course in self.courses
                if (course.category == CourseCategory.PYTHON_FUNDAMENTALS and
                    course.difficulty == DifficultyLevel.BEGINNER)
            ]
        elif goal == "algorithms_master":
            algo_courses = [
                course for course in self.courses
                if course.category == CourseCategory.ALGORITHMS
            ]
            return sorted(algo_courses, key=lambda c: c.difficulty.value)
        elif goal == "interview_prep":
            return [
                course for course in self.courses
                if course.category == CourseCategory.INTERVIEW_PREP
            ]
        
        return []
    
    def get_course_recommendations(self, user_profile: Dict[str, Any]) -> List[Course]:
        """Get personalized course recommendations based on user profile."""
        skill_level = user_profile.get("skill_level", DifficultyLevel.BEGINNER)
        interests = user_profile.get("interests", [])
        budget = user_profile.get("budget", "any")  # "free", "low", "medium", "high"
        
        suitable_courses = []
        
        for course in self.courses:
            # Filter by skill level
            if course.difficulty != skill_level:
                # Allow one level up for progression
                if not (skill_level == DifficultyLevel.BEGINNER and 
                       course.difficulty == DifficultyLevel.INTERMEDIATE):
                    continue
            
            # Filter by interests
            if interests:
                course_matches = any(
                    interest.lower() in course.category.value.lower() or
                    any(interest.lower() in topic.lower() for topic in course.key_topics)
                    for interest in interests
                )
                if not course_matches:
                    continue
            
            # Filter by budget
            if budget == "free" and "free" not in course.price.lower():
                continue
            
            suitable_courses.append(course)
        
        # Sort by rating and return top recommendations
        rated_courses = [c for c in suitable_courses if c.review]
        if rated_courses:
            return sorted(rated_courses, key=lambda c: c.review.overall_rating, reverse=True)[:5]
        
        return suitable_courses[:5]
    
    def export_catalog(self, filename: str):
        """Export course catalog to JSON."""
        data = {
            "courses": [course.to_dict() for course in self.courses],
            "export_date": datetime.datetime.now().isoformat(),
            "total_courses": len(self.courses)
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def demonstrate_courses_catalog():
    """Demonstrate course catalog functionality."""
    print("Online Courses and Tutorials Guide")
    print("=" * 40)
    
    catalog = CoursesCatalog()
    
    print(f"\nTotal Courses: {len(catalog.courses)}")
    
    # Show courses by platform
    print(f"\nCourses by Platform:")
    platform_counts = defaultdict(int)
    for course in catalog.courses:
        platform_counts[course.platform.value] += 1
    
    for platform, count in platform_counts.items():
        print(f"  {platform.replace('_', ' ').title()}: {count}")
    
    # Show top-rated courses
    print(f"\nTop-Rated Courses:")
    top_courses = catalog.get_top_rated_courses(5)
    for i, course in enumerate(top_courses, 1):
        rating = course.review.overall_rating if course.review else "N/A"
        print(f"  {i}. {course.title}")
        print(f"     Platform: {course.platform.value.replace('_', ' ').title()}")
        print(f"     Rating: {rating}/5.0 | Difficulty: {course.difficulty.value}")
        print(f"     Duration: {course.duration_hours}h | Price: {course.price}")
        print()
    
    # Show free courses
    print(f"Free Courses Available:")
    free_courses = catalog.get_free_courses()
    for course in free_courses:
        print(f"  - {course.title} ({course.platform.value})")


def generate_learning_paths():
    """Generate structured learning paths."""
    print("\n\nStructured Learning Paths")
    print("=" * 35)
    
    catalog = CoursesCatalog()
    
    learning_goals = [
        ("python_beginner", "Python Beginner Path"),
        ("algorithms_master", "Algorithms Mastery Path"),
        ("interview_prep", "Interview Preparation Path")
    ]
    
    for goal_key, goal_name in learning_goals:
        print(f"\n{goal_name}:")
        path_courses = catalog.get_learning_path(goal_key)
        
        total_hours = sum(course.duration_hours for course in path_courses)
        total_cost = "Varies"  # Would need more sophisticated cost calculation
        
        print(f"  Total Duration: ~{total_hours} hours")
        print(f"  Estimated Cost: {total_cost}")
        print(f"  Courses:")
        
        for i, course in enumerate(path_courses, 1):
            print(f"    {i}. {course.title}")
            print(f"       Platform: {course.platform.value} | Duration: {course.duration_hours}h")
            print(f"       Difficulty: {course.difficulty.value} | Price: {course.price}")
        print()


def analyze_course_recommendations():
    """Analyze and provide course recommendations for different user profiles."""
    print("\nPersonalized Course Recommendations")
    print("=" * 45)
    
    catalog = CoursesCatalog()
    
    # Define user profiles
    user_profiles = {
        "Complete Beginner": {
            "skill_level": DifficultyLevel.BEGINNER,
            "interests": ["python", "programming"],
            "budget": "free"
        },
        "Interview Candidate": {
            "skill_level": DifficultyLevel.INTERMEDIATE,
            "interests": ["algorithms", "interview"],
            "budget": "medium"
        },
        "Advanced Practitioner": {
            "skill_level": DifficultyLevel.ADVANCED,
            "interests": ["algorithms", "system design"],
            "budget": "high"
        }
    }
    
    for profile_name, profile in user_profiles.items():
        print(f"\nRecommendations for {profile_name}:")
        print(f"  Skill Level: {profile['skill_level'].value}")
        print(f"  Interests: {', '.join(profile['interests'])}")
        print(f"  Budget: {profile['budget']}")
        
        recommendations = catalog.get_course_recommendations(profile)
        
        if recommendations:
            print(f"  Top Recommendations:")
            for i, course in enumerate(recommendations, 1):
                rating = f"{course.review.overall_rating}/5" if course.review else "N/A"
                print(f"    {i}. {course.title}")
                print(f"       Platform: {course.platform.value} | Rating: {rating}")
                print(f"       Duration: {course.duration_hours}h | Price: {course.price}")
        else:
            print(f"  No suitable courses found for this profile.")
        print()


def create_platform_comparison():
    """Create comparison of different learning platforms."""
    print("\nLearning Platform Comparison")
    print("=" * 35)
    
    catalog = CoursesCatalog()
    
    # Analyze platforms
    platform_analysis = defaultdict(lambda: {
        "courses": 0,
        "avg_rating": 0,
        "free_courses": 0,
        "certificate_courses": 0,
        "total_hours": 0
    })
    
    for course in catalog.courses:
        platform = course.platform.value
        platform_analysis[platform]["courses"] += 1
        platform_analysis[platform]["total_hours"] += course.duration_hours
        
        if course.review:
            platform_analysis[platform]["avg_rating"] += course.review.overall_rating
        
        if "free" in course.price.lower():
            platform_analysis[platform]["free_courses"] += 1
        
        if course.certificate_available:
            platform_analysis[platform]["certificate_courses"] += 1
    
    # Calculate averages
    for platform_data in platform_analysis.values():
        if platform_data["courses"] > 0:
            platform_data["avg_rating"] /= platform_data["courses"]
    
    print(f"{'Platform':<20} {'Courses':<8} {'Avg Rating':<12} {'Free':<6} {'Certificates':<12}")
    print("-" * 65)
    
    for platform, data in platform_analysis.items():
        platform_name = platform.replace('_', ' ').title()[:18]
        avg_rating = f"{data['avg_rating']:.1f}/5" if data['avg_rating'] > 0 else "N/A"
        
        print(f"{platform_name:<20} {data['courses']:<8} {avg_rating:<12} {data['free_courses']:<6} {data['certificate_courses']:<12}")


def export_course_data():
    """Export course data for external use."""
    print("\n\nExporting Course Data")
    print("=" * 25)
    
    catalog = CoursesCatalog()
    
    # Export full catalog
    catalog.export_catalog("online_courses_catalog.json")
    print("Exported full catalog to online_courses_catalog.json")
    
    # Export platform-specific catalogs
    major_platforms = [Platform.COURSERA, Platform.EDX, Platform.YOUTUBE]
    
    for platform in major_platforms:
        platform_courses = catalog.get_courses_by_platform(platform)
        if platform_courses:
            platform_data = {
                "platform": platform.value,
                "courses": [course.to_dict() for course in platform_courses],
                "count": len(platform_courses),
                "export_date": datetime.datetime.now().isoformat()
            }
            
            filename = f"{platform.value}_courses.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(platform_data, f, indent=2, ensure_ascii=False)
            
            print(f"Exported {len(platform_courses)} {platform.value} courses to {filename}")


def main():
    """Main function to demonstrate online courses guide."""
    print("Python DSA Master - Online Courses and Tutorials Guide")
    print("=" * 60)
    
    try:
        demonstrate_courses_catalog()
        generate_learning_paths()
        analyze_course_recommendations()
        create_platform_comparison()
        export_course_data()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*60}")
    print("Online courses and tutorials guide demonstration complete!")


if __name__ == "__main__":
    main()


# ============================================================================
# ADDITIONAL COURSE RECOMMENDATIONS AND LEARNING STRATEGIES
# ============================================================================

"""
🎓 COMPREHENSIVE ONLINE LEARNING STRATEGY:

📚 PLATFORM-SPECIFIC STRENGTHS:

🔸 COURSERA:
• University partnerships (Stanford, MIT, etc.)
• High-quality production values
• Financial aid available
• Peer-reviewed assignments
• Specialization tracks
Best for: Comprehensive, university-level education

🔸 EDX:
• MIT, Harvard, and top university courses
• Often free with paid certificates
• Rigorous academic content
• Self-paced learning options
Best for: Academic rigor and prestigious institutions

🔸 UDEMY:
• Practical, job-focused content
• Frequent sales and discounts
• Wide variety of instructors
• Lifetime access to purchased courses
Best for: Practical skills and budget-conscious learning

🔸 YOUTUBE:
• Completely free content
• Diverse teaching styles
• Immediate accessibility
• Community discussions
Best for: Quick learning and budget constraints

🔸 CODECADEMY:
• Interactive coding environment
• Hands-on practice
• Immediate feedback
• Structured learning paths
Best for: Practical coding skills

💡 EFFECTIVE ONLINE LEARNING STRATEGIES:

🎯 GOAL SETTING:
• Define specific learning objectives
• Set realistic timelines
• Break large goals into milestones
• Track progress regularly

📅 SCHEDULING:
• Dedicate consistent time daily (30-60 minutes)
• Use calendar blocks for study sessions
• Balance theory and practice
• Schedule review sessions

🖥️ SETUP OPTIMIZATION:
• Create dedicated learning space
• Minimize distractions
• Use dual monitors if available
• Keep notebooks for key concepts

👥 COMMUNITY ENGAGEMENT:
• Join course discussion forums
• Form study groups with peers
• Share progress on social media
• Teach others what you learn

🔄 ACTIVE LEARNING TECHNIQUES:
• Take detailed notes
• Implement code examples
• Create personal projects
• Explain concepts aloud

📊 PROGRESS TRACKING:
• Maintain learning journal
• Complete all assignments
• Seek feedback from instructors
• Regular self-assessment

🚀 COURSE COMPLETION STRATEGIES:

⏰ TIME MANAGEMENT:
• Start with shorter courses to build momentum
• Use Pomodoro technique (25-min focused sessions)
• Set weekly completion targets
• Buffer time for challenging topics

🎯 RETENTION TECHNIQUES:
• Spaced repetition for key concepts
• Create visual mind maps
• Build practical projects
• Teach concepts to others

💻 HANDS-ON PRACTICE:
• Code along with examples
• Modify provided solutions
• Build variations of assignments
• Create personal portfolio projects

🔍 SUPPLEMENTARY RESOURCES:
• Cross-reference multiple courses
• Read relevant books
• Practice on coding platforms
• Join relevant communities

📈 SKILL PROGRESSION PATHS:

🌱 BEGINNER (0-6 months):
1. Python fundamentals course
2. Basic data structures tutorial
3. Simple algorithm explanations
4. Beginner coding challenges

🌿 INTERMEDIATE (6-18 months):
1. Comprehensive algorithms course
2. Advanced Python techniques
3. System design basics
4. Interview preparation courses

🌳 ADVANCED (18+ months):
1. Advanced algorithms specialization
2. Machine learning foundations
3. System architecture courses
4. Specialized domain knowledge

💰 BUDGET-CONSCIOUS LEARNING:

🆓 FREE RESOURCES:
• YouTube tutorials and lectures
• edX audit tracks
• Coursera audit option
• Khan Academy
• freeCodeCamp

💸 AFFORDABLE OPTIONS:
• Udemy sales (courses for $10-20)
• Coursera financial aid
• Pluralsight free weekends
• Library access to learning platforms

🏆 PREMIUM INVESTMENTS:
• AlgoExpert for interview prep
• Pluralsight annual subscription
• Coursera Plus subscription
• Udacity Nanodegrees

Remember: Consistency and practice are more valuable than expensive courses.
Focus on completing courses rather than collecting them!
"""
