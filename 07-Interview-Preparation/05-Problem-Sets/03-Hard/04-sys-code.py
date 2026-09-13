"""
System Design / Machine Coding - Interview Preparation

Learning Objectives:
1. Model real-world systems with OOP principles.
2. Implement concurrent or scalable mechanisms (conceptually).
3. Handle design patterns like Singleton, Factory, and Observer.

This module provides a basic template for a machine coding round (e.g., designing an In-Memory File System).
"""

from typing import List, Dict
import collections

# 1. In-Memory File System
class File:
    def __init__(self, name: str, is_dir: bool):
        self.name = name
        self.is_dir = is_dir
        self.content = ""
        self.children: Dict[str, 'File'] = {}

class FileSystem:
    def __init__(self):
        self.root = File("/", True)

    def ls(self, path: str) -> List[str]:
        node = self._traverse(path)
        if not node.is_dir:
            return [node.name]
        return sorted(node.children.keys())

    def mkdir(self, path: str) -> None:
        self._traverse(path, create=True)

    def addContentToFile(self, filePath: str, content: str) -> None:
        node = self._traverse(filePath, create=True)
        node.is_dir = False
        node.content += content

    def readContentFromFile(self, filePath: str) -> str:
        node = self._traverse(filePath)
        return node.content

    def _traverse(self, path: str, create: bool = False) -> File:
        if path == "/":
            return self.root
        
        parts = path.split("/")[1:]
        curr = self.root
        
        for part in parts:
            if part not in curr.children:
                if create:
                    curr.children[part] = File(part, True)
                else:
                    raise ValueError(f"Path not found: {path}")
            curr = curr.children[part]
            
        return curr

def test_machine_coding():
    print("Testing In-Memory File System:")
    fs = FileSystem()
    assert fs.ls("/") == []
    fs.mkdir("/a/b/c")
    fs.addContentToFile("/a/b/c/d", "hello")
    assert fs.ls("/") == ["a"]
    assert fs.readContentFromFile("/a/b/c/d") == "hello"
    fs.addContentToFile("/a/b/c/d", " world")
    assert fs.readContentFromFile("/a/b/c/d") == "hello world"
    print("File System tests passed!")

if __name__ == "__main__":
    test_machine_coding()
