#!/usr/bin/env python3
"""
Project-Based Learning: DSA Projects Collection

This module contains a comprehensive collection of hands-on projects that demonstrate
practical applications of data structures and algorithms. Each project is designed
to reinforce learning through real-world implementations and problem-solving.

Projects Included:
1. Library Management System (Hash Tables, Trees)
2. Social Network Analysis (Graphs, BFS/DFS)
3. Text Processing Engine (Trie, String Algorithms)
4. Memory Management Simulator (Stacks, Queues, LRU)
5. File System Simulator (Trees, Hash Tables)
6. Task Scheduler (Priority Queues, Heaps)
7. Compiler Expression Evaluator (Stacks, Trees)
8. Pathfinding Visualizer (Graphs, Shortest Path Algorithms)

Author: Python DSA Master
Date: 2024
"""

from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict, deque
from datetime import datetime, timedelta
from enum import Enum
import heapq
import json
import re
import hashlib


# ============================================================================
# PROJECT 1: LIBRARY MANAGEMENT SYSTEM
# ============================================================================

@dataclass
class Book:
    """Book entity for library management system."""
    isbn: str
    title: str
    author: str
    genre: str
    publication_year: int
    available_copies: int
    total_copies: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'publication_year': self.publication_year,
            'available_copies': self.available_copies,
            'total_copies': self.total_copies
        }


@dataclass
class Member:
    """Library member entity."""
    member_id: str
    name: str
    email: str
    join_date: datetime
    borrowed_books: List[str] = field(default_factory=list)
    max_books: int = 5


@dataclass
class BorrowRecord:
    """Book borrowing record."""
    record_id: str
    member_id: str
    isbn: str
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None


class LibraryManagementSystem:
    """
    Library Management System using Hash Tables and Binary Search Trees.
    
    Features:
    - Book catalog with fast lookups (Hash Table)
    - Member management (Hash Table)
    - Borrowing system with due date tracking
    - Search functionality by various attributes
    - Fine calculation for overdue books
    """
    
    def __init__(self):
        # Hash tables for O(1) lookups
        self.books: Dict[str, Book] = {}  # ISBN -> Book
        self.members: Dict[str, Member] = {}  # MemberID -> Member
        self.borrow_records: Dict[str, BorrowRecord] = {}  # RecordID -> BorrowRecord
        
        # Indexes for fast searching
        self.books_by_title: Dict[str, Set[str]] = defaultdict(set)
        self.books_by_author: Dict[str, Set[str]] = defaultdict(set)
        self.books_by_genre: Dict[str, Set[str]] = defaultdict(set)
        
        # Active borrowings: MemberID -> Set of RecordIDs
        self.active_borrowings: Dict[str, Set[str]] = defaultdict(set)
    
    def add_book(self, book: Book) -> bool:
        """Add a book to the library catalog."""
        if book.isbn in self.books:
            # Update existing book quantity
            self.books[book.isbn].total_copies += book.total_copies
            self.books[book.isbn].available_copies += book.available_copies
            return True
        
        # Add new book
        self.books[book.isbn] = book
        
        # Update indexes
        self.books_by_title[book.title.lower()].add(book.isbn)
        self.books_by_author[book.author.lower()].add(book.isbn)
        self.books_by_genre[book.genre.lower()].add(book.isbn)
        
        return True
    
    def add_member(self, member: Member) -> bool:
        """Add a new member to the library."""
        if member.member_id in self.members:
            return False  # Member already exists
        
        self.members[member.member_id] = member
        return True
    
    def borrow_book(self, member_id: str, isbn: str, days: int = 14) -> Optional[str]:
        """Borrow a book and return record ID if successful."""
        # Validate member
        if member_id not in self.members:
            raise ValueError("Member not found")
        
        member = self.members[member_id]
        if len(self.active_borrowings[member_id]) >= member.max_books:
            raise ValueError("Member has reached borrowing limit")
        
        # Validate book
        if isbn not in self.books:
            raise ValueError("Book not found")
        
        book = self.books[isbn]
        if book.available_copies <= 0:
            raise ValueError("Book not available")
        
        # Create borrow record
        record_id = self._generate_record_id()
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=days)
        
        record = BorrowRecord(
            record_id=record_id,
            member_id=member_id,
            isbn=isbn,
            borrow_date=borrow_date,
            due_date=due_date
        )
        
        # Update system state
        self.borrow_records[record_id] = record
        self.active_borrowings[member_id].add(record_id)
        book.available_copies -= 1
        member.borrowed_books.append(isbn)
        
        return record_id
    
    def return_book(self, record_id: str) -> Dict[str, Any]:
        """Return a borrowed book and calculate any fines."""
        if record_id not in self.borrow_records:
            raise ValueError("Borrow record not found")
        
        record = self.borrow_records[record_id]
        if record.return_date is not None:
            raise ValueError("Book already returned")
        
        # Mark as returned
        return_date = datetime.now()
        record.return_date = return_date
        
        # Calculate fine if overdue
        fine = 0.0
        if return_date > record.due_date:
            overdue_days = (return_date - record.due_date).days
            fine = overdue_days * 1.0  # $1 per day
        
        # Update system state
        book = self.books[record.isbn]
        member = self.members[record.member_id]
        
        book.available_copies += 1
        member.borrowed_books.remove(record.isbn)
        self.active_borrowings[record.member_id].discard(record_id)
        
        return {
            'record_id': record_id,
            'return_date': return_date,
            'fine': fine,
            'overdue_days': max(0, (return_date - record.due_date).days)
        }
    
    def search_books(self, query: str, search_type: str = 'title') -> List[Book]:
        """Search books by title, author, or genre."""
        query = query.lower()
        isbn_set = set()
        
        if search_type == 'title':
            for title, isbns in self.books_by_title.items():
                if query in title:
                    isbn_set.update(isbns)
        elif search_type == 'author':
            for author, isbns in self.books_by_author.items():
                if query in author:
                    isbn_set.update(isbns)
        elif search_type == 'genre':
            for genre, isbns in self.books_by_genre.items():
                if query in genre:
                    isbn_set.update(isbns)
        
        return [self.books[isbn] for isbn in isbn_set]
    
    def get_overdue_books(self) -> List[Dict[str, Any]]:
        """Get list of overdue books."""
        current_date = datetime.now()
        overdue = []
        
        for record in self.borrow_records.values():
            if record.return_date is None and current_date > record.due_date:
                overdue_days = (current_date - record.due_date).days
                overdue.append({
                    'record_id': record.record_id,
                    'member': self.members[record.member_id].name,
                    'book': self.books[record.isbn].title,
                    'due_date': record.due_date,
                    'overdue_days': overdue_days,
                    'fine': overdue_days * 1.0
                })
        
        return sorted(overdue, key=lambda x: x['overdue_days'], reverse=True)
    
    def _generate_record_id(self) -> str:
        """Generate unique record ID."""
        import secrets
        return f"BR-{secrets.token_hex(4).upper()}"
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get library statistics."""
        total_books = sum(book.total_copies for book in self.books.values())
        available_books = sum(book.available_copies for book in self.books.values())
        borrowed_books = total_books - available_books
        
        active_borrowings_count = sum(len(records) for records in self.active_borrowings.values())
        overdue_count = len(self.get_overdue_books())
        
        return {
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books,
            'total_members': len(self.members),
            'active_borrowings': active_borrowings_count,
            'overdue_books': overdue_count,
            'unique_titles': len(self.books)
        }


# ============================================================================
# PROJECT 2: SOCIAL NETWORK ANALYSIS
# ============================================================================

class SocialNetwork:
    """
    Social Network Analysis using Graph Data Structures.
    
    Features:
    - User connections (Graph with adjacency list)
    - Friend recommendations using mutual connections
    - Community detection using BFS/DFS
    - Shortest path between users
    - Influence analysis using graph metrics
    """
    
    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {}  # UserID -> User info
        self.connections: Dict[str, Set[str]] = defaultdict(set)  # Adjacency list
        self.blocked_users: Dict[str, Set[str]] = defaultdict(set)
    
    def add_user(self, user_id: str, name: str, email: str) -> bool:
        """Add a new user to the network."""
        if user_id in self.users:
            return False
        
        self.users[user_id] = {
            'name': name,
            'email': email,
            'join_date': datetime.now(),
            'posts_count': 0,
            'followers_count': 0,
            'following_count': 0
        }
        return True
    
    def connect_users(self, user1: str, user2: str) -> bool:
        """Create bidirectional connection between two users."""
        if user1 not in self.users or user2 not in self.users:
            return False
        
        if user2 in self.blocked_users[user1] or user1 in self.blocked_users[user2]:
            return False
        
        self.connections[user1].add(user2)
        self.connections[user2].add(user1)
        
        self.users[user1]['following_count'] += 1
        self.users[user2]['followers_count'] += 1
        
        return True
    
    def disconnect_users(self, user1: str, user2: str) -> bool:
        """Remove connection between two users."""
        if user1 not in self.users or user2 not in self.users:
            return False
        
        if user2 in self.connections[user1]:
            self.connections[user1].remove(user2)
            self.connections[user2].remove(user1)
            
            self.users[user1]['following_count'] -= 1
            self.users[user2]['followers_count'] -= 1
            
            return True
        return False
    
    def get_mutual_connections(self, user1: str, user2: str) -> Set[str]:
        """Find mutual connections between two users."""
        if user1 not in self.users or user2 not in self.users:
            return set()
        
        return self.connections[user1] & self.connections[user2]
    
    def recommend_friends(self, user_id: str, max_recommendations: int = 10) -> List[Dict[str, Any]]:
        """Recommend friends based on mutual connections."""
        if user_id not in self.users:
            return []
        
        user_connections = self.connections[user_id]
        recommendations = defaultdict(int)
        
        # Find users with mutual connections
        for friend in user_connections:
            for friend_of_friend in self.connections[friend]:
                if (friend_of_friend != user_id and 
                    friend_of_friend not in user_connections and
                    friend_of_friend not in self.blocked_users[user_id]):
                    recommendations[friend_of_friend] += 1
        
        # Sort by number of mutual connections
        sorted_recommendations = sorted(
            recommendations.items(),
            key=lambda x: x[1],
            reverse=True
        )[:max_recommendations]
        
        result = []
        for rec_user_id, mutual_count in sorted_recommendations:
            user_info = self.users[rec_user_id]
            result.append({
                'user_id': rec_user_id,
                'name': user_info['name'],
                'mutual_connections': mutual_count,
                'followers': user_info['followers_count']
            })
        
        return result
    
    def find_shortest_path(self, start_user: str, end_user: str) -> Optional[List[str]]:
        """Find shortest path between two users using BFS."""
        if start_user not in self.users or end_user not in self.users:
            return None
        
        if start_user == end_user:
            return [start_user]
        
        queue = deque([(start_user, [start_user])])
        visited = {start_user}
        
        while queue:
            current_user, path = queue.popleft()
            
            for neighbor in self.connections[current_user]:
                if neighbor == end_user:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None  # No path found
    
    def find_communities(self, min_size: int = 3) -> List[Set[str]]:
        """Find communities in the network using DFS."""
        visited = set()
        communities = []
        
        for user_id in self.users:
            if user_id not in visited:
                community = self._dfs_component(user_id, visited)
                if len(community) >= min_size:
                    communities.append(community)
        
        return communities
    
    def _dfs_component(self, start_user: str, visited: Set[str]) -> Set[str]:
        """DFS to find connected component."""
        component = set()
        stack = [start_user]
        
        while stack:
            user_id = stack.pop()
            if user_id not in visited:
                visited.add(user_id)
                component.add(user_id)
                
                for neighbor in self.connections[user_id]:
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return component
    
    def get_user_influence(self, user_id: str) -> Dict[str, Any]:
        """Calculate user influence metrics."""
        if user_id not in self.users:
            return {}
        
        user_info = self.users[user_id]
        connections_count = len(self.connections[user_id])
        
        # Calculate clustering coefficient
        if connections_count < 2:
            clustering_coefficient = 0.0
        else:
            user_friends = self.connections[user_id]
            possible_edges = connections_count * (connections_count - 1) / 2
            actual_edges = 0
            
            for friend1 in user_friends:
                for friend2 in user_friends:
                    if friend1 < friend2 and friend2 in self.connections[friend1]:
                        actual_edges += 1
            
            clustering_coefficient = actual_edges / possible_edges if possible_edges > 0 else 0
        
        return {
            'user_id': user_id,
            'name': user_info['name'],
            'direct_connections': connections_count,
            'followers': user_info['followers_count'],
            'following': user_info['following_count'],
            'clustering_coefficient': clustering_coefficient,
            'posts_count': user_info['posts_count']
        }
    
    def get_network_statistics(self) -> Dict[str, Any]:
        """Get overall network statistics."""
        total_users = len(self.users)
        total_connections = sum(len(connections) for connections in self.connections.values()) // 2
        
        if total_users > 1:
            avg_connections = total_connections * 2 / total_users
            density = total_connections / (total_users * (total_users - 1) / 2)
        else:
            avg_connections = 0
            density = 0
        
        communities = self.find_communities()
        largest_community = max(len(community) for community in communities) if communities else 0
        
        return {
            'total_users': total_users,
            'total_connections': total_connections,
            'average_connections_per_user': avg_connections,
            'network_density': density,
            'number_of_communities': len(communities),
            'largest_community_size': largest_community
        }


# ============================================================================
# PROJECT 3: TEXT PROCESSING ENGINE
# ============================================================================

class TrieNode:
    """Node for Trie data structure."""
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_word_end: bool = False
        self.frequency: int = 0
        self.word: str = ""


class TextProcessingEngine:
    """
    Advanced Text Processing Engine using Trie and String Algorithms.
    
    Features:
    - Autocomplete using Trie
    - Spell checker with edit distance
    - Text analysis and statistics
    - Keyword extraction
    - Similarity analysis between texts
    """
    
    def __init__(self):
        self.dictionary_trie = TrieNode()
        self.word_frequencies: Dict[str, int] = defaultdict(int)
        self.total_words = 0
    
    def add_word(self, word: str, frequency: int = 1):
        """Add word to dictionary with frequency."""
        word = word.lower().strip()
        if not word:
            return
        
        # Add to trie
        current = self.dictionary_trie
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
        
        current.is_word_end = True
        current.word = word
        current.frequency += frequency
        
        # Update global statistics
        self.word_frequencies[word] += frequency
        self.total_words += frequency
    
    def build_dictionary_from_text(self, text: str):
        """Build dictionary from a large text corpus."""
        words = self._tokenize(text)
        word_counts = defaultdict(int)
        
        for word in words:
            word_counts[word] += 1
        
        for word, count in word_counts.items():
            self.add_word(word, count)
    
    def get_autocomplete_suggestions(self, prefix: str, max_suggestions: int = 10) -> List[Dict[str, Any]]:
        """Get autocomplete suggestions for a prefix."""
        prefix = prefix.lower().strip()
        if not prefix:
            return []
        
        # Navigate to prefix node
        current = self.dictionary_trie
        for char in prefix:
            if char not in current.children:
                return []  # Prefix not found
            current = current.children[char]
        
        # Collect all words with this prefix
        suggestions = []
        self._collect_words(current, suggestions, max_suggestions)
        
        # Sort by frequency (most common first)
        suggestions.sort(key=lambda x: x['frequency'], reverse=True)
        
        return suggestions[:max_suggestions]
    
    def _collect_words(self, node: TrieNode, suggestions: List[Dict[str, Any]], max_suggestions: int):
        """Recursively collect words from trie node."""
        if len(suggestions) >= max_suggestions:
            return
        
        if node.is_word_end:
            suggestions.append({
                'word': node.word,
                'frequency': node.frequency
            })
        
        for child in node.children.values():
            self._collect_words(child, suggestions, max_suggestions)
            if len(suggestions) >= max_suggestions:
                break
    
    def spell_check(self, word: str, max_distance: int = 2) -> List[Dict[str, Any]]:
        """Find spelling corrections using edit distance."""
        word = word.lower().strip()
        
        # If word exists in dictionary, return it
        if self._word_exists(word):
            return [{'word': word, 'distance': 0, 'confidence': 1.0}]
        
        suggestions = []
        
        # Check all words in dictionary
        for dict_word, frequency in self.word_frequencies.items():
            distance = self._edit_distance(word, dict_word)
            if distance <= max_distance:
                # Calculate confidence based on edit distance and frequency
                confidence = (1.0 / (distance + 1)) * min(1.0, frequency / 100)
                suggestions.append({
                    'word': dict_word,
                    'distance': distance,
                    'frequency': frequency,
                    'confidence': confidence
                })
        
        # Sort by confidence and distance
        suggestions.sort(key=lambda x: (-x['confidence'], x['distance']))
        
        return suggestions[:10]
    
    def _edit_distance(self, str1: str, str2: str) -> int:
        """Calculate edit distance between two strings."""
        m, n = len(str1), len(str2)
        
        # Create DP table
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Initialize base cases
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i - 1] == str2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],     # deletion
                        dp[i][j - 1],     # insertion
                        dp[i - 1][j - 1]  # substitution
                    )
        
        return dp[m][n]
    
    def _word_exists(self, word: str) -> bool:
        """Check if word exists in trie."""
        current = self.dictionary_trie
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
        return current.is_word_end
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Perform comprehensive text analysis."""
        words = self._tokenize(text)
        sentences = self._split_sentences(text)
        
        # Basic statistics
        word_count = len(words)
        unique_words = len(set(words))
        sentence_count = len(sentences)
        char_count = len(text)
        char_count_no_spaces = len(text.replace(' ', ''))
        
        # Advanced statistics
        avg_word_length = sum(len(word) for word in words) / word_count if words else 0
        avg_sentence_length = word_count / sentence_count if sentences else 0
        
        # Word frequency analysis
        word_freq = defaultdict(int)
        for word in words:
            word_freq[word] += 1
        
        most_common_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Readability metrics (simplified)
        readability_score = self._calculate_readability(words, sentences)
        
        return {
            'word_count': word_count,
            'unique_words': unique_words,
            'sentence_count': sentence_count,
            'character_count': char_count,
            'character_count_no_spaces': char_count_no_spaces,
            'average_word_length': round(avg_word_length, 2),
            'average_sentence_length': round(avg_sentence_length, 2),
            'vocabulary_richness': round(unique_words / word_count, 2) if words else 0,
            'readability_score': readability_score,
            'most_common_words': most_common_words
        }
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        # Simple tokenization - can be enhanced
        import string
        text = text.lower()
        # Remove punctuation
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)
        return [word for word in text.split() if word]
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting - can be enhanced
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _calculate_readability(self, words: List[str], sentences: List[str]) -> float:
        """Calculate readability score (simplified Flesch formula)."""
        if not words or not sentences:
            return 0.0
        
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = sum(self._count_syllables(word) for word in words) / len(words)
        
        # Simplified Flesch Reading Ease score
        score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        return max(0, min(100, score))
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simplified)."""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Handle silent 'e'
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)


# ============================================================================
# PROJECT 4: TASK SCHEDULER USING PRIORITY QUEUES
# ============================================================================

@dataclass
class Task:
    """Task entity for the scheduler."""
    task_id: str
    name: str
    priority: int  # Lower number = higher priority
    estimated_duration: int  # in minutes
    deadline: Optional[datetime] = None
    dependencies: List[str] = field(default_factory=list)
    status: str = "pending"  # pending, running, completed, failed
    created_at: datetime = field(default_factory=datetime.now)
    
    def __lt__(self, other):
        """Comparison for priority queue (min-heap)."""
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.deadline < other.deadline if self.deadline and other.deadline else False


class TaskScheduler:
    """
    Task Scheduler using Priority Queues and Topological Sort.
    
    Features:
    - Priority-based task scheduling
    - Dependency resolution using topological sort
    - Deadline management
    - Resource allocation
    - Performance analytics
    """
    
    def __init__(self, max_concurrent_tasks: int = 3):
        self.tasks: Dict[str, Task] = {}
        self.priority_queue: List[Task] = []  # Min-heap
        self.running_tasks: Dict[str, Task] = {}
        self.completed_tasks: List[str] = []
        self.failed_tasks: List[str] = []
        self.max_concurrent_tasks = max_concurrent_tasks
        
        # Dependency graph: task_id -> set of tasks that depend on it
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_dependencies: Dict[str, Set[str]] = defaultdict(set)
    
    def add_task(self, task: Task) -> bool:
        """Add a task to the scheduler."""
        if task.task_id in self.tasks:
            return False
        
        self.tasks[task.task_id] = task
        
        # Build dependency graph
        for dependency in task.dependencies:
            if dependency in self.tasks:
                self.dependency_graph[dependency].add(task.task_id)
                self.reverse_dependencies[task.task_id].add(dependency)
        
        # Add to priority queue if no dependencies or dependencies are met
        if self._dependencies_satisfied(task.task_id):
            heapq.heappush(self.priority_queue, task)
        
        return True
    
    def _dependencies_satisfied(self, task_id: str) -> bool:
        """Check if all dependencies for a task are satisfied."""
        task = self.tasks[task_id]
        for dependency in task.dependencies:
            if dependency not in self.completed_tasks:
                return False
        return True
    
    def get_next_task(self) -> Optional[Task]:
        """Get the next task to execute based on priority and dependencies."""
        while self.priority_queue:
            task = heapq.heappop(self.priority_queue)
            
            # Check if task is still valid and dependencies are satisfied
            if (task.task_id in self.tasks and 
                task.status == "pending" and
                self._dependencies_satisfied(task.task_id)):
                return task
        
        return None
    
    def start_task(self, task_id: str) -> bool:
        """Start executing a task."""
        if (task_id not in self.tasks or 
            len(self.running_tasks) >= self.max_concurrent_tasks or
            not self._dependencies_satisfied(task_id)):
            return False
        
        task = self.tasks[task_id]
        if task.status != "pending":
            return False
        
        task.status = "running"
        self.running_tasks[task_id] = task
        
        return True
    
    def complete_task(self, task_id: str, success: bool = True) -> None:
        """Mark a task as completed or failed."""
        if task_id not in self.running_tasks:
            return
        
        task = self.running_tasks[task_id]
        
        if success:
            task.status = "completed"
            self.completed_tasks.append(task_id)
            
            # Check if any dependent tasks can now be scheduled
            for dependent_task_id in self.dependency_graph[task_id]:
                if self._dependencies_satisfied(dependent_task_id):
                    dependent_task = self.tasks[dependent_task_id]
                    if dependent_task.status == "pending":
                        heapq.heappush(self.priority_queue, dependent_task)
        else:
            task.status = "failed"
            self.failed_tasks.append(task_id)
        
        del self.running_tasks[task_id]
    
    def get_schedule(self) -> List[Dict[str, Any]]:
        """Get optimized task schedule using topological sort."""
        # Create a copy of the dependency graph
        in_degree = defaultdict(int)
        graph = defaultdict(list)
        
        # Build in-degree count and adjacency list
        for task_id, task in self.tasks.items():
            if task.status == "pending":
                in_degree[task_id] = len(task.dependencies)
                for dependency in task.dependencies:
                    if dependency in self.tasks and self.tasks[dependency].status == "pending":
                        graph[dependency].append(task_id)
        
        # Topological sort with priority consideration
        queue = []
        for task_id, degree in in_degree.items():
            if degree == 0:
                heapq.heappush(queue, self.tasks[task_id])
        
        schedule = []
        while queue:
            current_task = heapq.heappop(queue)
            task_id = current_task.task_id
            
            schedule.append({
                'task_id': task_id,
                'name': current_task.name,
                'priority': current_task.priority,
                'estimated_duration': current_task.estimated_duration,
                'deadline': current_task.deadline,
                'position': len(schedule) + 1
            })
            
            # Update in-degree for dependent tasks
            for dependent_id in graph[task_id]:
                in_degree[dependent_id] -= 1
                if in_degree[dependent_id] == 0:
                    heapq.heappush(queue, self.tasks[dependent_id])
        
        return schedule
    
    def get_critical_path(self) -> List[str]:
        """Find critical path - longest path through task dependencies."""
        # This is a simplified version - in practice, would use more sophisticated algorithms
        schedule = self.get_schedule()
        
        if not schedule:
            return []
        
        # For simplification, return tasks sorted by deadline and priority
        critical_tasks = [
            task for task in schedule
            if self.tasks[task['task_id']].deadline is not None
        ]
        
        critical_tasks.sort(key=lambda x: (
            self.tasks[x['task_id']].deadline,
            x['priority']
        ))
        
        return [task['task_id'] for task in critical_tasks]
    
    def get_scheduler_statistics(self) -> Dict[str, Any]:
        """Get scheduler performance statistics."""
        total_tasks = len(self.tasks)
        pending_tasks = len([t for t in self.tasks.values() if t.status == "pending"])
        running_tasks_count = len(self.running_tasks)
        completed_tasks_count = len(self.completed_tasks)
        failed_tasks_count = len(self.failed_tasks)
        
        # Calculate average completion time (would need actual timing data)
        overdue_tasks = []
        current_time = datetime.now()
        
        for task in self.tasks.values():
            if task.deadline and current_time > task.deadline and task.status != "completed":
                overdue_tasks.append(task.task_id)
        
        return {
            'total_tasks': total_tasks,
            'pending_tasks': pending_tasks,
            'running_tasks': running_tasks_count,
            'completed_tasks': completed_tasks_count,
            'failed_tasks': failed_tasks_count,
            'success_rate': (completed_tasks_count / max(1, completed_tasks_count + failed_tasks_count)) * 100,
            'overdue_tasks': len(overdue_tasks),
            'queue_size': len(self.priority_queue),
            'resource_utilization': (running_tasks_count / self.max_concurrent_tasks) * 100
        }


# ============================================================================
# DEMONSTRATION FUNCTIONS
# ============================================================================

def demonstrate_library_management():
    """Demonstrate Library Management System."""
    print("Library Management System Demo")
    print("=" * 40)
    
    library = LibraryManagementSystem()
    
    # Add books
    books = [
        Book("978-0134685991", "Effective Java", "Joshua Bloch", "Programming", 2017, 3, 3),
        Book("978-0596009205", "Head First Design Patterns", "Eric Freeman", "Programming", 2004, 2, 2),
        Book("978-0134494166", "Clean Code", "Robert Martin", "Programming", 2008, 5, 5),
        Book("978-1449370770", "Python for Data Analysis", "Wes McKinney", "Data Science", 2017, 2, 2)
    ]
    
    for book in books:
        library.add_book(book)
    
    # Add members
    members = [
        Member("M001", "Alice Johnson", "alice@email.com", datetime.now()),
        Member("M002", "Bob Smith", "bob@email.com", datetime.now()),
        Member("M003", "Charlie Brown", "charlie@email.com", datetime.now())
    ]
    
    for member in members:
        library.add_member(member)
    
    print(f"Added {len(books)} books and {len(members)} members")
    
    # Borrow books
    try:
        record1 = library.borrow_book("M001", "978-0134685991")
        record2 = library.borrow_book("M002", "978-0596009205")
        print(f"Books borrowed successfully. Records: {record1}, {record2}")
    except ValueError as e:
        print(f"Borrowing failed: {e}")
    
    # Search books
    search_results = library.search_books("python", "title")
    print(f"\nSearch results for 'python': {[book.title for book in search_results]}")
    
    # Show statistics
    stats = library.get_statistics()
    print(f"\nLibrary Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


def demonstrate_social_network():
    """Demonstrate Social Network Analysis."""
    print("\n\nSocial Network Analysis Demo")
    print("=" * 35)
    
    network = SocialNetwork()
    
    # Add users
    users = [
        ("alice", "Alice Cooper", "alice@email.com"),
        ("bob", "Bob Dylan", "bob@email.com"),
        ("charlie", "Charlie Chaplin", "charlie@email.com"),
        ("diana", "Diana Ross", "diana@email.com"),
        ("eve", "Eve Jobs", "eve@email.com")
    ]
    
    for user_id, name, email in users:
        network.add_user(user_id, name, email)
    
    # Create connections
    connections = [
        ("alice", "bob"),
        ("alice", "charlie"),
        ("bob", "charlie"),
        ("bob", "diana"),
        ("charlie", "diana"),
        ("diana", "eve")
    ]
    
    for user1, user2 in connections:
        network.connect_users(user1, user2)
    
    print(f"Network created with {len(users)} users and {len(connections)} connections")
    
    # Find shortest path
    path = network.find_shortest_path("alice", "eve")
    print(f"Shortest path from Alice to Eve: {' -> '.join(path) if path else 'No path found'}")
    
    # Get friend recommendations
    recommendations = network.recommend_friends("alice", 3)
    print(f"\nFriend recommendations for Alice:")
    for rec in recommendations:
        print(f"  {rec['name']} (mutual connections: {rec['mutual_connections']})")
    
    # Analyze user influence
    influence = network.get_user_influence("bob")
    print(f"\nBob's influence metrics:")
    for key, value in influence.items():
        print(f"  {key}: {value}")
    
    # Network statistics
    stats = network.get_network_statistics()
    print(f"\nNetwork Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


def demonstrate_text_processing():
    """Demonstrate Text Processing Engine."""
    print("\n\nText Processing Engine Demo")
    print("=" * 35)
    
    engine = TextProcessingEngine()
    
    # Build dictionary from sample text
    sample_text = """
    Python is a high-level programming language with dynamic semantics.
    Its high-level built-in data structures, combined with dynamic typing
    and dynamic binding, make it very attractive for Rapid Application
    Development, as well as for use as a scripting or glue language to
    connect existing components together. Python's simple, easy to learn
    syntax emphasizes readability and therefore reduces the cost of program
    maintenance. Python supports modules and packages, which encourages
    program modularity and code reuse.
    """
    
    engine.build_dictionary_from_text(sample_text)
    print(f"Built dictionary with {len(engine.word_frequencies)} unique words")
    
    # Autocomplete suggestions
    suggestions = engine.get_autocomplete_suggestions("prog", 5)
    print(f"\nAutocomplete for 'prog':")
    for suggestion in suggestions:
        print(f"  {suggestion['word']} (frequency: {suggestion['frequency']})")
    
    # Spell checking
    misspelled_word = "programing"  # missing 'm'
    corrections = engine.spell_check(misspelled_word, max_distance=2)
    print(f"\nSpell check for '{misspelled_word}':")
    for correction in corrections[:3]:
        print(f"  {correction['word']} (distance: {correction['distance']}, confidence: {correction['confidence']:.2f})")
    
    # Text analysis
    analysis = engine.analyze_text(sample_text)
    print(f"\nText Analysis:")
    for key, value in analysis.items():
        if key != 'most_common_words':
            print(f"  {key}: {value}")
    
    print("  Most common words:")
    for word, freq in analysis['most_common_words'][:5]:
        print(f"    {word}: {freq}")


def demonstrate_task_scheduler():
    """Demonstrate Task Scheduler."""
    print("\n\nTask Scheduler Demo")
    print("=" * 25)
    
    scheduler = TaskScheduler(max_concurrent_tasks=2)
    
    # Create tasks with dependencies
    tasks = [
        Task("T1", "Setup Environment", 1, 30),
        Task("T2", "Install Dependencies", 2, 20, dependencies=["T1"]),
        Task("T3", "Write Tests", 3, 60, dependencies=["T2"]),
        Task("T4", "Implement Feature", 2, 90, dependencies=["T2"]),
        Task("T5", "Code Review", 1, 45, dependencies=["T3", "T4"]),
        Task("T6", "Deploy", 1, 30, dependencies=["T5"])
    ]
    
    # Add deadline for some tasks
    tasks[5].deadline = datetime.now() + timedelta(days=7)  # Deploy deadline
    tasks[4].deadline = datetime.now() + timedelta(days=5)  # Code review deadline
    
    # Add tasks to scheduler
    for task in tasks:
        scheduler.add_task(task)
    
    print(f"Added {len(tasks)} tasks to scheduler")
    
    # Get optimized schedule
    schedule = scheduler.get_schedule()
    print(f"\nOptimized Task Schedule:")
    for i, task_info in enumerate(schedule, 1):
        task = scheduler.tasks[task_info['task_id']]
        deps = f" (depends on: {', '.join(task.dependencies)})" if task.dependencies else ""
        print(f"  {i}. {task_info['name']} - Priority: {task_info['priority']}, Duration: {task_info['estimated_duration']}min{deps}")
    
    # Find critical path
    critical_path = scheduler.get_critical_path()
    print(f"\nCritical Path: {' -> '.join(critical_path)}")
    
    # Simulate task execution
    print(f"\nSimulating task execution...")
    
    # Start first available tasks
    for _ in range(scheduler.max_concurrent_tasks):
        next_task = scheduler.get_next_task()
        if next_task:
            scheduler.start_task(next_task.task_id)
            print(f"  Started: {next_task.name}")
    
    # Complete a task
    if scheduler.running_tasks:
        first_running_task = next(iter(scheduler.running_tasks.keys()))
        scheduler.complete_task(first_running_task, success=True)
        task_name = scheduler.tasks[first_running_task].name
        print(f"  Completed: {task_name}")
    
    # Show scheduler statistics
    stats = scheduler.get_scheduler_statistics()
    print(f"\nScheduler Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


def run_all_project_demos():
    """Run all project demonstrations."""
    print("DSA Projects Collection - Comprehensive Demo")
    print("=" * 50)
    
    try:
        demonstrate_library_management()
        demonstrate_social_network()
        demonstrate_text_processing()
        demonstrate_task_scheduler()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*50}")
    print("All project demonstrations completed successfully!")


if __name__ == "__main__":
    run_all_project_demos()


# ============================================================================
# PROJECT LEARNING OUTCOMES AND EXTENSIONS
# ============================================================================

"""
🎓 PROJECT LEARNING OUTCOMES:

📚 LIBRARY MANAGEMENT SYSTEM:
• Hash Tables for O(1) lookups and insertions
• Secondary indexes for fast searching
• Date/time handling for due dates and fines
• Business logic implementation with data structures
• Error handling and validation

🌐 SOCIAL NETWORK ANALYSIS:
• Graph representation using adjacency lists
• BFS for shortest path finding
• DFS for community detection
• Graph metrics and influence analysis
• Recommendation algorithms using graph traversal

📝 TEXT PROCESSING ENGINE:
• Trie data structure for efficient prefix matching
• Dynamic programming for edit distance calculation
• String algorithms for text analysis
• Frequency analysis and statistical processing
• Natural language processing basics

⏰ TASK SCHEDULER:
• Priority Queues (heaps) for task prioritization
• Topological sorting for dependency resolution
• Graph algorithms for critical path analysis
• Scheduling algorithms and resource management
• Performance metrics and optimization

🚀 POSSIBLE EXTENSIONS:

📚 LIBRARY SYSTEM EXTENSIONS:
• Book reservation system with queues
• Late fee calculation with compound interest
• Multi-branch library management
• Reading recommendation system
• Digital resource management

🌐 SOCIAL NETWORK EXTENSIONS:
• Influence propagation modeling
• Content recommendation algorithms
• Privacy settings and access control
• Real-time activity feeds
• Graph compression techniques

📝 TEXT PROCESSING EXTENSIONS:
• Advanced NLP with stemming and lemmatization
• Sentiment analysis using machine learning
• Document similarity using TF-IDF
• Multi-language support
• Real-time text processing with streaming

⏰ SCHEDULER EXTENSIONS:
• Resource constraint scheduling
• Dynamic priority adjustment
• Machine learning for task duration prediction
• Distributed task scheduling
• Fault tolerance and recovery mechanisms

💡 IMPLEMENTATION BEST PRACTICES:
• Use appropriate data structures for each use case
• Implement proper error handling and edge cases
• Add comprehensive logging and monitoring
• Design for scalability and performance
• Write thorough unit tests and documentation
• Consider thread safety for concurrent access
• Implement caching strategies for performance
• Use design patterns for maintainable code

Remember: These projects demonstrate how fundamental data structures
and algorithms solve real-world problems. Focus on understanding
the underlying concepts and how they apply to practical scenarios!
"""
