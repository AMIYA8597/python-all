#!/usr/bin/env python3
"""
Hash Table Data Structure Implementation
=======================================

This module provides comprehensive hash table implementations with different
collision resolution strategies, hash functions, and performance analysis.

Hash Table Properties:
- Fast average-case lookup, insertion, and deletion (O(1))
- Key-value storage with dynamic sizing
- Uses hash function to map keys to array indices
- Requires collision resolution strategy

Topics Covered:
- Hash functions and their properties
- Collision resolution strategies
- Load factor and rehashing
- Hash table operations
- Performance analysis and optimization
- Real-world applications

Author: Python DSA Master Course
Version: 1.0
"""

import sys
from typing import Any, List, Tuple, Optional, Dict, Callable, TypeVar, Generic
import time
import random
import string
import math
from enum import Enum

K = TypeVar('K')  # Key type
V = TypeVar('V')  # Value type


# ============================================================================
# SECTION 1: HASH FUNCTIONS
# ============================================================================

class HashFunction:
    """Collection of hash functions for different data types."""
    
    @staticmethod
    def simple_hash(key: Any, table_size: int) -> int:
        """
        Simple hash function for demonstration.
        
        Not suitable for production use due to high collision rate.
        """
        if isinstance(key, int):
            return key % table_size
        elif isinstance(key, str):
            # Sum ASCII values
            total = sum(ord(char) for char in key)
            return total % table_size
        elif hasattr(key, '__hash__'):
            # Use Python's built-in hash
            return abs(hash(key)) % table_size
        else:
            # Convert to string if not hashable
            return HashFunction.simple_hash(str(key), table_size)
    
    @staticmethod
    def djb2_hash(key: str, table_size: int) -> int:
        """
        DJB2 hash function for strings.
        
        A popular string hashing algorithm with good distribution.
        """
        # Convert to string if not already
        key_str = str(key)
        
        # Start with a prime number
        hash_value = 5381
        
        # Update hash for each character
        for char in key_str:
            # hash * 33 + char
            hash_value = ((hash_value << 5) + hash_value) + ord(char)
        
        return abs(hash_value) % table_size
    
    @staticmethod
    def fnv1a_hash(key: str, table_size: int) -> int:
        """
        FNV-1a hash function.
        
        Good for strings with fast computation and low collision rate.
        """
        # Convert to string if not already
        key_str = str(key)
        
        # FNV parameters
        fnv_prime = 16777619
        fnv_offset = 2166136261
        
        # Compute hash
        hash_value = fnv_offset
        for char in key_str:
            hash_value = hash_value ^ ord(char)
            hash_value = (hash_value * fnv_prime) & 0xffffffff
        
        return hash_value % table_size
    
    @staticmethod
    def double_hash(key: Any, table_size: int, attempt: int) -> int:
        """
        Double hashing function for probing.
        
        Uses two hash functions to compute probe sequence.
        """
        # Primary hash function
        h1 = HashFunction.djb2_hash(key, table_size)
        
        # Secondary hash function (must be non-zero)
        h2 = 1 + HashFunction.fnv1a_hash(key, table_size - 1)
        
        # Combine for double hashing
        return (h1 + attempt * h2) % table_size


# ============================================================================
# SECTION 2: COLLISION RESOLUTION STRATEGIES
# ============================================================================

class CollisionStrategy(Enum):
    """Enumeration of collision resolution strategies."""
    CHAINING = 1
    LINEAR_PROBING = 2
    QUADRATIC_PROBING = 3
    DOUBLE_HASHING = 4


class HashTableEntry(Generic[K, V]):
    """Entry in a hash table (for open addressing)."""
    
    def __init__(self, key: K, value: V, is_deleted: bool = False):
        self.key = key
        self.value = value
        self.is_deleted = is_deleted
    
    def __str__(self) -> str:
        status = "DELETED" if self.is_deleted else "ACTIVE"
        return f"({self.key}: {self.value}) [{status}]"


# ============================================================================
# SECTION 3: HASH TABLE WITH CHAINING
# ============================================================================

class HashTableChaining(Generic[K, V]):
    """
    Hash table implementation using separate chaining for collision resolution.
    
    Separate chaining uses linked lists to store multiple entries at the same index.
    """
    
    def __init__(self, initial_capacity: int = 16, load_factor_threshold: float = 0.75):
        """Initialize hash table with separate chaining."""
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor_threshold = load_factor_threshold
        self.buckets: List[List[Tuple[K, V]]] = [[] for _ in range(initial_capacity)]
        self.hash_function = HashFunction.djb2_hash
    
    def _hash(self, key: K) -> int:
        """Generate hash index for a key."""
        return self.hash_function(key, self.capacity)
    
    def _calculate_load_factor(self) -> float:
        """Calculate current load factor."""
        return self.size / self.capacity
    
    def _rehash(self) -> None:
        """
        Resize and rehash the table.
        
        Time Complexity: O(n) where n is number of entries
        """
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        
        # Reinsert all entries
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)
    
    def put(self, key: K, value: V) -> None:
        """
        Insert or update key-value pair.
        
        Time Complexity: 
        - Average case: O(1)
        - Worst case: O(n) if many collisions
        """
        index = self._hash(key)
        
        # Check if key already exists
        for i, (k, _) in enumerate(self.buckets[index]):
            if k == key:
                # Update existing key
                self.buckets[index][i] = (key, value)
                return
        
        # Add new key-value pair
        self.buckets[index].append((key, value))
        self.size += 1
        
        # Check if rehashing is needed
        if self._calculate_load_factor() > self.load_factor_threshold:
            self._rehash()
    
    def get(self, key: K) -> Optional[V]:
        """
        Retrieve value for key.
        
        Time Complexity:
        - Average case: O(1)
        - Worst case: O(n) if many collisions
        """
        index = self._hash(key)
        
        # Search in bucket
        for k, v in self.buckets[index]:
            if k == key:
                return v
        
        return None
    
    def remove(self, key: K) -> bool:
        """
        Remove key-value pair.
        
        Time Complexity: Same as get
        """
        index = self._hash(key)
        
        # Search and remove
        for i, (k, _) in enumerate(self.buckets[index]):
            if k == key:
                self.buckets[index].pop(i)
                self.size -= 1
                return True
        
        return False
    
    def contains(self, key: K) -> bool:
        """Check if key exists."""
        return self.get(key) is not None
    
    def keys(self) -> List[K]:
        """Get all keys."""
        result = []
        for bucket in self.buckets:
            for key, _ in bucket:
                result.append(key)
        return result
    
    def values(self) -> List[V]:
        """Get all values."""
        result = []
        for bucket in self.buckets:
            for _, value in bucket:
                result.append(value)
        return result
    
    def items(self) -> List[Tuple[K, V]]:
        """Get all key-value pairs."""
        result = []
        for bucket in self.buckets:
            result.extend(bucket)
        return result
    
    def clear(self) -> None:
        """Clear hash table."""
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
    
    def __len__(self) -> int:
        """Return number of entries."""
        return self.size
    
    def __contains__(self, key: K) -> bool:
        """Support 'in' operator."""
        return self.contains(key)
    
    def __str__(self) -> str:
        """String representation."""
        items = self.items()
        if not items:
            return "{}"
        
        return "{" + ", ".join(f"{k}: {v}" for k, v in items) + "}"
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about hash table.
        
        Returns information about load factor, collisions, etc.
        """
        stats = {
            "size": self.size,
            "capacity": self.capacity,
            "load_factor": self._calculate_load_factor(),
            "empty_buckets": 0,
            "max_chain_length": 0,
            "avg_chain_length": 0.0,
            "collision_rate": 0.0
        }
        
        # Calculate statistics
        chain_lengths = []
        for bucket in self.buckets:
            length = len(bucket)
            chain_lengths.append(length)
            if length == 0:
                stats["empty_buckets"] += 1
            if length > stats["max_chain_length"]:
                stats["max_chain_length"] = length
        
        # Calculate average chain length for non-empty buckets
        non_empty = self.capacity - stats["empty_buckets"]
        if non_empty > 0:
            stats["avg_chain_length"] = self.size / non_empty
        
        # Calculate collision rate
        if self.size > 0:
            collisions = sum(max(0, length - 1) for length in chain_lengths)
            stats["collision_rate"] = collisions / self.size
        
        return stats


# ============================================================================
# SECTION 4: HASH TABLE WITH OPEN ADDRESSING
# ============================================================================

class HashTableOpenAddressing(Generic[K, V]):
    """
    Hash table implementation using open addressing for collision resolution.
    
    Supports linear probing, quadratic probing, and double hashing.
    """
    
    def __init__(self, 
                initial_capacity: int = 16, 
                load_factor_threshold: float = 0.5,
                strategy: CollisionStrategy = CollisionStrategy.LINEAR_PROBING):
        """Initialize hash table with open addressing."""
        # Ensure capacity is a power of 2 for efficient modulo
        self.capacity = max(2, int(2 ** math.ceil(math.log2(initial_capacity))))
        self.size = 0
        self.deleted_count = 0
        self.load_factor_threshold = load_factor_threshold
        self.strategy = strategy
        self.table: List[Optional[HashTableEntry[K, V]]] = [None] * self.capacity
        self.hash_function = HashFunction.djb2_hash
    
    def _hash(self, key: K) -> int:
        """Generate hash index for a key."""
        return self.hash_function(key, self.capacity)
    
    def _calculate_load_factor(self) -> float:
        """Calculate current load factor (including deleted entries)."""
        return (self.size + self.deleted_count) / self.capacity
    
    def _find_slot(self, key: K, for_insertion: bool = False) -> Tuple[int, bool]:
        """
        Find appropriate slot for a key.
        
        Returns (index, found) where:
        - index is the appropriate slot
        - found is True if key exists
        
        If for_insertion is True, returns the first available slot
        (which could be a deleted slot or empty slot).
        """
        initial_index = self._hash(key)
        deleted_index = -1
        
        for i in range(self.capacity):
            # Compute probe sequence based on strategy
            if self.strategy == CollisionStrategy.LINEAR_PROBING:
                index = (initial_index + i) % self.capacity
            elif self.strategy == CollisionStrategy.QUADRATIC_PROBING:
                # Quadratic probing formula: (hash + i^2) % capacity
                index = (initial_index + i*i) % self.capacity
            elif self.strategy == CollisionStrategy.DOUBLE_HASHING:
                # Use double hashing function
                index = HashFunction.double_hash(key, self.capacity, i)
            else:
                raise ValueError(f"Unsupported strategy: {self.strategy}")
            
            entry = self.table[index]
            
            if entry is None:
                # Empty slot found
                if for_insertion and deleted_index != -1:
                    # Use previously found deleted slot for insertion
                    return deleted_index, False
                return index, False
            
            if entry.is_deleted:
                # Save the first deleted slot we find
                if deleted_index == -1:
                    deleted_index = index
                continue
            
            if entry.key == key:
                # Found the key
                return index, True
        
        # Table is full (should never happen with proper rehashing)
        if for_insertion and deleted_index != -1:
            # Use a deleted slot if available
            return deleted_index, False
        
        raise RuntimeError("Hash table is full and no slot was found")
    
    def _rehash(self) -> None:
        """
        Resize and rehash the table.
        
        Time Complexity: O(n) where n is table capacity
        """
        old_table = self.table
        old_capacity = self.capacity
        
        # Double the capacity
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        self.deleted_count = 0
        
        # Reinsert all active entries
        for i in range(old_capacity):
            entry = old_table[i]
            if entry is not None and not entry.is_deleted:
                self.put(entry.key, entry.value)
    
    def put(self, key: K, value: V) -> None:
        """
        Insert or update key-value pair.
        
        Time Complexity: 
        - Average case: O(1)
        - Worst case: O(n) with poor hash function
        """
        # Check load factor and rehash if needed
        if self._calculate_load_factor() > self.load_factor_threshold:
            self._rehash()
        
        # Find slot for insertion
        index, found = self._find_slot(key, True)
        
        if found:
            # Update existing entry
            self.table[index].value = value
        else:
            # Create new entry
            entry = HashTableEntry(key, value)
            
            # Check if we're replacing a deleted entry
            if self.table[index] is not None and self.table[index].is_deleted:
                self.deleted_count -= 1
            
            self.table[index] = entry
            self.size += 1
    
    def get(self, key: K) -> Optional[V]:
        """
        Retrieve value for key.
        
        Time Complexity:
        - Average case: O(1)
        - Worst case: O(n) with poor hash function
        """
        try:
            index, found = self._find_slot(key)
            if found:
                return self.table[index].value
            return None
        except RuntimeError:
            return None
    
    def remove(self, key: K) -> bool:
        """
        Remove key-value pair.
        
        Uses lazy deletion to mark entries as deleted.
        """
        try:
            index, found = self._find_slot(key)
            if found:
                self.table[index].is_deleted = True
                self.size -= 1
                self.deleted_count += 1
                return True
            return False
        except RuntimeError:
            return False
    
    def contains(self, key: K) -> bool:
        """Check if key exists."""
        return self.get(key) is not None
    
    def keys(self) -> List[K]:
        """Get all keys."""
        result = []
        for entry in self.table:
            if entry is not None and not entry.is_deleted:
                result.append(entry.key)
        return result
    
    def values(self) -> List[V]:
        """Get all values."""
        result = []
        for entry in self.table:
            if entry is not None and not entry.is_deleted:
                result.append(entry.value)
        return result
    
    def items(self) -> List[Tuple[K, V]]:
        """Get all key-value pairs."""
        result = []
        for entry in self.table:
            if entry is not None and not entry.is_deleted:
                result.append((entry.key, entry.value))
        return result
    
    def clear(self) -> None:
        """Clear hash table."""
        self.table = [None] * self.capacity
        self.size = 0
        self.deleted_count = 0
    
    def __len__(self) -> int:
        """Return number of entries."""
        return self.size
    
    def __contains__(self, key: K) -> bool:
        """Support 'in' operator."""
        return self.contains(key)
    
    def __str__(self) -> str:
        """String representation."""
        items = self.items()
        if not items:
            return "{}"
        
        return "{" + ", ".join(f"{k}: {v}" for k, v in items) + "}"
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about hash table.
        
        Returns information about load factor, probes, etc.
        """
        stats = {
            "size": self.size,
            "capacity": self.capacity,
            "deleted_count": self.deleted_count,
            "load_factor": self._calculate_load_factor(),
            "strategy": self.strategy.name,
            "empty_slots": 0,
            "probe_lengths": []
        }
        
        # Calculate statistics
        stats["empty_slots"] = sum(1 for entry in self.table if entry is None)
        
        # Calculate probe lengths (expensive operation)
        probe_lengths = []
        for i, entry in enumerate(self.table):
            if entry is not None and not entry.is_deleted:
                # Calculate how many probes needed to find this entry
                initial_index = self._hash(entry.key)
                if i == initial_index:
                    probes = 1  # No collision
                else:
                    # Determine number of probes by simulating lookup
                    probes = 1
                    test_index = initial_index
                    while test_index != i:
                        probes += 1
                        if self.strategy == CollisionStrategy.LINEAR_PROBING:
                            test_index = (initial_index + probes - 1) % self.capacity
                        elif self.strategy == CollisionStrategy.QUADRATIC_PROBING:
                            test_index = (initial_index + (probes - 1)**2) % self.capacity
                        elif self.strategy == CollisionStrategy.DOUBLE_HASHING:
                            test_index = HashFunction.double_hash(entry.key, self.capacity, probes - 1)
                
                probe_lengths.append(probes)
        
        stats["probe_lengths"] = probe_lengths
        stats["avg_probe_length"] = sum(probe_lengths) / len(probe_lengths) if probe_lengths else 0
        stats["max_probe_length"] = max(probe_lengths) if probe_lengths else 0
        
        return stats


# ============================================================================
# SECTION 5: PERFORMANCE COMPARISON
# ============================================================================

def benchmark_hash_tables():
    """Compare performance of different hash table implementations."""
    print("\n=== HASH TABLE PERFORMANCE COMPARISON ===")
    
    # Hash table implementations to test
    hash_tables = {
        "Chaining": HashTableChaining(initial_capacity=1024),
        "Linear Probing": HashTableOpenAddressing(initial_capacity=1024, strategy=CollisionStrategy.LINEAR_PROBING),
        "Quadratic Probing": HashTableOpenAddressing(initial_capacity=1024, strategy=CollisionStrategy.QUADRATIC_PROBING),
        "Double Hashing": HashTableOpenAddressing(initial_capacity=1024, strategy=CollisionStrategy.DOUBLE_HASHING)
    }
    
    # Test data sizes
    sizes = [1000, 10000, 50000]
    
    # Generate random keys
    def generate_random_keys(count: int, key_length: int = 10) -> List[str]:
        """Generate random string keys."""
        return [''.join(random.choices(string.ascii_letters + string.digits, k=key_length)) 
                for _ in range(count)]
    
    for size in sizes:
        print(f"\nBenchmarking with {size} entries:")
        
        # Generate random keys and values
        keys = generate_random_keys(size)
        values = list(range(size))
        
        for name, ht in hash_tables.items():
            # Clear previous data
            ht.clear()
            
            # Benchmark insertion
            start = time.perf_counter()
            for i in range(size):
                ht.put(keys[i], values[i])
            insert_time = time.perf_counter() - start
            
            # Benchmark lookup (successful)
            start = time.perf_counter()
            for i in range(size):
                ht.get(keys[i])
            lookup_time = time.perf_counter() - start
            
            # Benchmark lookup (unsuccessful)
            missing_keys = generate_random_keys(1000, key_length=15)  # Different length to avoid collisions
            start = time.perf_counter()
            for key in missing_keys:
                ht.get(key)
            miss_time = time.perf_counter() - start
            
            # Get stats
            stats = ht.get_stats()
            
            print(f"  {name}:")
            print(f"    Insert time: {insert_time:.6f}s")
            print(f"    Lookup time: {lookup_time:.6f}s")
            print(f"    Miss lookup time: {miss_time:.6f}s")
            print(f"    Load factor: {stats['load_factor']:.3f}")
            
            if 'collision_rate' in stats:
                print(f"    Collision rate: {stats['collision_rate']:.3f}")
            if 'avg_chain_length' in stats:
                print(f"    Avg chain length: {stats['avg_chain_length']:.2f}")
            if 'avg_probe_length' in stats:
                print(f"    Avg probe length: {stats['avg_probe_length']:.2f}")


# ============================================================================
# SECTION 6: REAL-WORLD APPLICATIONS
# ============================================================================

class SimpleLRUCache:
    """
    Simple LRU (Least Recently Used) Cache implementation using hash table.
    
    Uses hash table for O(1) lookups and tracks access order.
    """
    
    def __init__(self, capacity: int = 128):
        """Initialize LRU cache with given capacity."""
        self.capacity = max(1, capacity)
        self.hash_table = HashTableChaining(initial_capacity=capacity * 2)
        self.access_order: List[K] = []  # Most recently used at the end
    
    def get(self, key: K) -> Optional[V]:
        """
        Get value for key and update access order.
        
        Time Complexity: O(1) average case
        """
        value = self.hash_table.get(key)
        if value is not None:
            # Update access order (move to end)
            self.access_order.remove(key)
            self.access_order.append(key)
        return value
    
    def put(self, key: K, value: V) -> None:
        """
        Insert or update key-value pair.
        
        Evicts least recently used item if at capacity.
        """
        if key in self.hash_table:
            # Update existing entry
            self.hash_table.put(key, value)
            # Update access order
            self.access_order.remove(key)
            self.access_order.append(key)
        else:
            # Check if we need to evict
            if len(self.hash_table) >= self.capacity:
                # Evict least recently used
                lru_key = self.access_order.pop(0)
                self.hash_table.remove(lru_key)
            
            # Add new entry
            self.hash_table.put(key, value)
            self.access_order.append(key)
    
    def contains(self, key: K) -> bool:
        """Check if key exists in cache."""
        return key in self.hash_table
    
    def clear(self) -> None:
        """Clear the cache."""
        self.hash_table.clear()
        self.access_order.clear()
    
    def __len__(self) -> int:
        """Return number of entries in cache."""
        return len(self.hash_table)
    
    def __contains__(self, key: K) -> bool:
        """Support 'in' operator."""
        return self.contains(key)
    
    def __str__(self) -> str:
        """String representation of cache."""
        return str(self.hash_table)


class SimpleSpellChecker:
    """
    Simple spell checker using hash table as dictionary.
    
    Demonstrates efficient lookups for text processing.
    """
    
    def __init__(self, words: List[str] = None):
        """Initialize spell checker with dictionary."""
        self.dictionary = HashTableOpenAddressing(strategy=CollisionStrategy.LINEAR_PROBING)
        if words:
            for word in words:
                self.add_word(word)
    
    def add_word(self, word: str) -> None:
        """Add word to dictionary."""
        self.dictionary.put(word.lower(), True)
    
    def is_word(self, word: str) -> bool:
        """Check if word exists in dictionary."""
        return self.dictionary.contains(word.lower())
    
    def suggest_corrections(self, word: str, max_suggestions: int = 5) -> List[str]:
        """
        Suggest spelling corrections.
        
        Simple implementation that tries:
        1. Deleting one character
        2. Swapping adjacent characters
        3. Replacing one character
        """
        word = word.lower()
        if self.is_word(word):
            return [word]
        
        suggestions = []
        
        # Try deleting one character
        for i in range(len(word)):
            candidate = word[:i] + word[i+1:]
            if self.is_word(candidate) and candidate not in suggestions:
                suggestions.append(candidate)
                if len(suggestions) >= max_suggestions:
                    return suggestions
        
        # Try swapping adjacent characters
        for i in range(len(word) - 1):
            candidate = word[:i] + word[i+1] + word[i] + word[i+2:]
            if self.is_word(candidate) and candidate not in suggestions:
                suggestions.append(candidate)
                if len(suggestions) >= max_suggestions:
                    return suggestions
        
        # Try replacing one character
        for i in range(len(word)):
            for c in string.ascii_lowercase:
                candidate = word[:i] + c + word[i+1:]
                if candidate != word and self.is_word(candidate) and candidate not in suggestions:
                    suggestions.append(candidate)
                    if len(suggestions) >= max_suggestions:
                        return suggestions
        
        return suggestions


def demonstrate_applications():
    """Demonstrate real-world hash table applications."""
    print("\n=== REAL-WORLD APPLICATIONS ===")
    
    # Demonstrate LRU Cache
    print("\n1. LRU Cache Example:")
    cache = SimpleLRUCache(capacity=5)
    
    # Add some entries
    cache.put("key1", "value1")
    cache.put("key2", "value2")
    cache.put("key3", "value3")
    cache.put("key4", "value4")
    cache.put("key5", "value5")
    
    print(f"  Initial cache: {cache}")
    
    # Access some entries to change order
    print(f"  Access key2: {cache.get('key2')}")
    print(f"  Access key4: {cache.get('key4')}")
    
    # Add another entry to cause eviction
    print("  Adding key6 (should evict key1)")
    cache.put("key6", "value6")
    print(f"  Cache after eviction: {cache}")
    print(f"  key1 in cache: {cache.contains('key1')}")
    
    # Demonstrate Spell Checker
    print("\n2. Spell Checker Example:")
    dictionary = [
        "apple", "banana", "orange", "pear", "grape", "strawberry",
        "python", "java", "javascript", "programming", "algorithm",
        "data", "structure", "computer", "science", "machine", "learning"
    ]
    
    spell_checker = SimpleSpellChecker(dictionary)
    
    test_words = ["python", "algorthm", "strcture", "learing", "javscript"]
    
    for word in test_words:
        correct = spell_checker.is_word(word)
        print(f"  '{word}': {'Correct' if correct else 'Incorrect'}")
        
        if not correct:
            suggestions = spell_checker.suggest_corrections(word)
            if suggestions:
                print(f"    Suggestions: {', '.join(suggestions)}")
            else:
                print(f"    No suggestions found")


# ============================================================================
# SECTION 7: TESTING AND VALIDATION
# ============================================================================

def test_hash_table_operations():
    """Comprehensive testing of hash table implementations."""
    print("\n=== TESTING HASH TABLE OPERATIONS ===")
    
    # Test HashTableChaining
    print("Testing HashTableChaining:")
    ht_chaining = HashTableChaining(initial_capacity=16)
    
    # Test basic operations
    assert len(ht_chaining) == 0, "New hash table should be empty"
    
    # Test insertions
    ht_chaining.put("key1", "value1")
    ht_chaining.put("key2", "value2")
    ht_chaining.put("key3", "value3")
    
    assert len(ht_chaining) == 3, "Should have 3 entries"
    assert ht_chaining.get("key1") == "value1", "Should retrieve correct value"
    assert ht_chaining.get("nonexistent") is None, "Should return None for missing key"
    assert "key2" in ht_chaining, "Should support 'in' operator"
    
    # Test update
    ht_chaining.put("key1", "updated_value")
    assert ht_chaining.get("key1") == "updated_value", "Should update value"
    
    # Test removal
    assert ht_chaining.remove("key2"), "Should remove existing key"
    assert ht_chaining.get("key2") is None, "Should not find removed key"
    assert not ht_chaining.remove("nonexistent"), "Should return False for missing key"
    
    # Test keys/values/items
    assert set(ht_chaining.keys()) == {"key1", "key3"}, "Should return all keys"
    assert set(ht_chaining.values()) == {"updated_value", "value3"}, "Should return all values"
    assert set(ht_chaining.items()) == {("key1", "updated_value"), ("key3", "value3")}, "Should return all items"
    
    # Test clear
    ht_chaining.clear()
    assert len(ht_chaining) == 0, "Clear should remove all entries"
    
    print("  HashTableChaining: All tests passed!")
    
    # Test HashTableOpenAddressing
    print("Testing HashTableOpenAddressing (Linear Probing):")
    ht_linear = HashTableOpenAddressing(strategy=CollisionStrategy.LINEAR_PROBING)
    
    # Test basic operations
    assert len(ht_linear) == 0, "New hash table should be empty"
    
    # Test insertions
    ht_linear.put("key1", "value1")
    ht_linear.put("key2", "value2")
    ht_linear.put("key3", "value3")
    
    assert len(ht_linear) == 3, "Should have 3 entries"
    assert ht_linear.get("key1") == "value1", "Should retrieve correct value"
    assert ht_linear.get("nonexistent") is None, "Should return None for missing key"
    assert "key2" in ht_linear, "Should support 'in' operator"
    
    # Test update
    ht_linear.put("key1", "updated_value")
    assert ht_linear.get("key1") == "updated_value", "Should update value"
    
    # Test removal
    assert ht_linear.remove("key2"), "Should remove existing key"
    assert ht_linear.get("key2") is None, "Should not find removed key"
    assert not ht_linear.remove("nonexistent"), "Should return False for missing key"
    
    # Test re-insertion after removal
    ht_linear.put("key4", "value4")
    assert ht_linear.get("key4") == "value4", "Should insert after removal"
    
    # Test other collision strategies
    print("Testing Other Collision Strategies:")
    
    strategies = [
        CollisionStrategy.QUADRATIC_PROBING,
        CollisionStrategy.DOUBLE_HASHING
    ]
    
    for strategy in strategies:
        ht = HashTableOpenAddressing(strategy=strategy)
        
        # Insert many values to test collision handling
        for i in range(20):
            ht.put(f"key{i}", f"value{i}")
        
        # Verify all values can be retrieved
        for i in range(20):
            assert ht.get(f"key{i}") == f"value{i}", f"Strategy {strategy.name} failed to retrieve key{i}"
    
    print("  HashTableOpenAddressing: All tests passed!")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main function to run all demonstrations."""
    print("Hash Table Data Structure Implementation")
    print("=" * 55)
    
    try:
        # Basic hash table demonstrations
        print("=== BASIC HASH TABLE DEMONSTRATIONS ===")
        
        # HashTableChaining
        print("\n1. Hash Table with Chaining:")
        ht_chaining = HashTableChaining(initial_capacity=8)
        
        # Add some entries
        entries = [
            ("name", "John Smith"),
            ("age", 30),
            ("email", "john@example.com"),
            ("occupation", "Software Engineer"),
            ("location", "New York")
        ]
        
        for key, value in entries:
            ht_chaining.put(key, value)
        
        print(f"  Hash table contents: {ht_chaining}")
        print(f"  Get 'name': {ht_chaining.get('name')}")
        print(f"  Get 'phone': {ht_chaining.get('phone')}")
        print(f"  Size: {len(ht_chaining)}")
        
        # Display stats
        stats = ht_chaining.get_stats()
        print(f"  Statistics:")
        print(f"    Capacity: {stats['capacity']}")
        print(f"    Load factor: {stats['load_factor']:.3f}")
        print(f"    Collision rate: {stats['collision_rate']:.3f}")
        print(f"    Average chain length: {stats['avg_chain_length']:.2f}")
        
        # HashTableOpenAddressing
        print("\n2. Hash Table with Open Addressing:")
        ht_open = HashTableOpenAddressing(initial_capacity=8, strategy=CollisionStrategy.LINEAR_PROBING)
        
        # Add same entries
        for key, value in entries:
            ht_open.put(key, value)
        
        print(f"  Hash table contents: {ht_open}")
        print(f"  Get 'email': {ht_open.get('email')}")
        print(f"  Get 'phone': {ht_open.get('phone')}")
        print(f"  Size: {len(ht_open)}")
        
        # Display stats
        stats = ht_open.get_stats()
        print(f"  Statistics:")
        print(f"    Capacity: {stats['capacity']}")
        print(f"    Load factor: {stats['load_factor']:.3f}")
        print(f"    Strategy: {stats['strategy']}")
        if 'avg_probe_length' in stats:
            print(f"    Average probe length: {stats['avg_probe_length']:.2f}")
        
        # Run performance comparisons
        benchmark_hash_tables()
        
        # Show real-world applications
        demonstrate_applications()
        
        # Run tests
        test_hash_table_operations()
        
    except Exception as e:
        print(f"Error during execution: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print(f"\n{'=' * 55}")
        print("Hash table implementation demonstration complete!")
        print(f"Python version: {sys.version}")


if __name__ == "__main__":
    main()


# ============================================================================
# PRACTICE EXERCISES
# ============================================================================

"""
PRACTICE EXERCISES:

1. Implement a hash table that supports iterating through entries in insertion order.

2. Create a perfect hash function for a fixed set of keys.

3. Implement a consistent hashing scheme for distributed systems.

4. Create a cuckoo hashing implementation.

5. Build a hash table that supports versioning (keeps history of values).

6. Implement a concurrent hash table with thread safety.

7. Create a hash table with custom equality comparators for keys.

8. Build a memory-efficient hash table for small integer keys.

9. Implement a Robin Hood hashing strategy.

10. Create a hash table that efficiently handles large string keys.

ADVANCED CHALLENGES:

1. Implement bloom filter for membership queries
2. Create count-min sketch for frequency estimation
3. Build HyperLogLog for cardinality estimation
4. Implement minimal perfect hash function generator
5. Create consistent hashing with bounded loads
6. Build distributed hash table (DHT)
7. Implement extendible hashing for database index
8. Create locality-sensitive hashing for similarity search
9. Build cryptographic hash functions
10. Implement probabilistic data structures (e.g., quotient filter)

ALGORITHM APPLICATIONS:

1. De-duplication of large datasets
2. Fast substring search with Rabin-Karp
3. Implement hash-based authentication (HMAC)
4. Build symbol table for compiler
5. Create file/document checksumming system
6. Implement hash-based content addressable storage
7. Build network packet filtering
8. Create password hashing with salt and pepper
9. Implement distributed cache with consistent hashing
10. Build hash-based index for database

SYSTEM DESIGN:

1. Design distributed key-value store
2. Build content delivery network (CDN) caching system
3. Create large-scale web caching system
4. Implement sharded database system
5. Build URL shortener service
"""
