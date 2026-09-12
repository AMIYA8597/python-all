"""
Advanced File Manager Implementation

This module provides an object-oriented file manager utility using modern Python
features, specifically `pathlib` for robust cross-platform path handling, and 
`shutil` for high-level file operations.

# Educational Content
See the README.md for a full architectural breakdown, interview questions, and 
practical exercises related to this project.
"""

import os
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Union, Optional
import unittest
import tempfile

# Configure standard logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('FileManager')


class FileManagerError(Exception):
    """Base exception class for FileManager errors."""
    pass


class FileManager:
    """
    A robust, object-oriented file manager.
    Maintains a 'current working directory' state.
    """

    def __init__(self, initial_dir: Union[str, Path, None] = None):
        """
        Initializes the file manager.
        
        Args:
            initial_dir: The starting directory. Defaults to the current working directory.
        """
        if initial_dir is None:
            self.current_dir = Path.cwd()
        else:
            self.current_dir = Path(initial_dir).resolve()
            
        if not self.current_dir.is_dir():
            raise FileManagerError(f"Initialization failed. Not a directory: {self.current_dir}")
        
        logger.info(f"FileManager initialized at: {self.current_dir}")

    def _resolve_path(self, target_path: Union[str, Path]) -> Path:
        """
        Safely resolves a path string or Path object against the current directory.
        This handles both relative paths ('../folder') and absolute paths ('/etc').
        """
        path = Path(target_path)
        if not path.is_absolute():
            path = (self.current_dir / path)
        return path.resolve()

    def change_directory(self, target_dir: Union[str, Path]) -> bool:
        """
        Changes the current working directory.
        
        Args:
            target_dir: The path to change to.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            new_dir = self._resolve_path(target_dir)
            if new_dir.is_dir():
                self.current_dir = new_dir
                logger.info(f"Changed directory to: {self.current_dir}")
                return True
            else:
                logger.error(f"Cannot change directory. Target is not a directory: {new_dir}")
                return False
        except PermissionError:
             logger.error(f"Permission denied: {target_dir}")
             return False
        except Exception as e:
            logger.error(f"Error changing directory to {target_dir}: {e}")
            return False

    def list_directory(self) -> List[Dict]:
        """
        Lists contents of the current directory, returning structured metadata.
        
        Returns:
            List of dictionaries containing item metadata.
        """
        contents = []
        try:
            # Using iterdir() is memory efficient
            for item in self.current_dir.iterdir():
                stat_info = item.stat()
                contents.append({
                    'name': item.name,
                    'is_dir': item.is_dir(),
                    'size_bytes': stat_info.st_size,
                    'modified_time': datetime.fromtimestamp(stat_info.st_mtime).isoformat()
                })
            logger.info(f"Listed {len(contents)} items in {self.current_dir}")
        except PermissionError:
             logger.error(f"Permission denied accessing directory: {self.current_dir}")
        except Exception as e:
            logger.error(f"Error listing directory {self.current_dir}: {e}")
            
        return contents

    def create_directory(self, dir_name: str) -> bool:
        """Creates a new directory within the current directory."""
        target = self._resolve_path(dir_name)
        try:
            target.mkdir(parents=True, exist_ok=False)
            logger.info(f"Created directory: {target}")
            return True
        except FileExistsError:
            logger.warning(f"Directory already exists: {target}")
            return False
        except Exception as e:
            logger.error(f"Failed to create directory {target}: {e}")
            return False

    def copy_item(self, source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """
        Copies a file or an entire directory tree.
        """
        src_path = self._resolve_path(source)
        dest_path = self._resolve_path(destination)

        if not src_path.exists():
            logger.error(f"Source does not exist: {src_path}")
            return False

        try:
            if src_path.is_file():
                shutil.copy2(src_path, dest_path)
                logger.info(f"Copied file {src_path} -> {dest_path}")
            elif src_path.is_dir():
                shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
                logger.info(f"Copied directory tree {src_path} -> {dest_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to copy {src_path} to {dest_path}: {e}")
            return False

    def delete_item(self, target: Union[str, Path], recursive: bool = False) -> bool:
        """
        Deletes a file or directory.
        
        Args:
            target: The path to delete.
            recursive: Must be True to delete a non-empty directory.
        """
        target_path = self._resolve_path(target)
        
        if not target_path.exists():
             logger.warning(f"Item does not exist, nothing to delete: {target_path}")
             return False
             
        try:
            if target_path.is_file() or target_path.is_symlink():
                target_path.unlink()
                logger.info(f"Deleted file/symlink: {target_path}")
            elif target_path.is_dir():
                if recursive:
                    shutil.rmtree(target_path)
                    logger.info(f"Deleted directory tree recursively: {target_path}")
                else:
                    target_path.rmdir() # Fails if not empty
                    logger.info(f"Deleted empty directory: {target_path}")
            return True
        except OSError as e:
             logger.error(f"Failed to delete {target_path}. Error: {e}. (If directory is not empty, set recursive=True)")
             return False
        except Exception as e:
             logger.error(f"Unexpected error deleting {target_path}: {e}")
             return False
             
    def find_files(self, pattern: str) -> List[Path]:
        """
        Recursively searches for files matching a glob pattern from the current directory.
        
        Args:
            pattern: Glob pattern, e.g., '*.txt' or '**/*.py'
        """
        try:
             results = list(self.current_dir.rglob(pattern))
             logger.info(f"Found {len(results)} matches for pattern '{pattern}'")
             return results
        except Exception as e:
             logger.error(f"Error searching for {pattern}: {e}")
             return []


# --- Unit Tests ---

class TestFileManager(unittest.TestCase):
    """Unit test suite for the FileManager."""
    
    def setUp(self):
        """Create a temporary directory structure for isolated testing."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.test_dir.name)
        
        # Setup initial test files
        (self.base_path / "file1.txt").write_text("Hello World")
        (self.base_path / "folderA").mkdir()
        (self.base_path / "folderA" / "file2.log").write_text("Log data")
        
        # Initialize FileManager pointing to the temp directory
        self.fm = FileManager(initial_dir=self.base_path)

    def tearDown(self):
        """Clean up the temporary directory."""
        self.test_dir.cleanup()

    def test_initialization(self):
        self.assertEqual(self.fm.current_dir, self.base_path)

    def test_change_directory(self):
        target = self.base_path / "folderA"
        success = self.fm.change_directory("folderA")
        self.assertTrue(success)
        self.assertEqual(self.fm.current_dir, target)
        
        # Test going up a directory
        self.fm.change_directory("..")
        self.assertEqual(self.fm.current_dir, self.base_path)

    def test_change_directory_invalid(self):
        success = self.fm.change_directory("does_not_exist")
        self.assertFalse(success)
        # Should remain at the old directory
        self.assertEqual(self.fm.current_dir, self.base_path)

    def test_list_directory(self):
        contents = self.fm.list_directory()
        names = [item['name'] for item in contents]
        self.assertIn("file1.txt", names)
        self.assertIn("folderA", names)
        self.assertEqual(len(contents), 2)

    def test_create_directory(self):
        self.fm.create_directory("folderB/subfolder")
        expected_path = self.base_path / "folderB" / "subfolder"
        self.assertTrue(expected_path.is_dir())

    def test_copy_file(self):
        self.fm.copy_item("file1.txt", "file1_copy.txt")
        self.assertTrue((self.base_path / "file1_copy.txt").exists())
        self.assertEqual((self.base_path / "file1_copy.txt").read_text(), "Hello World")

    def test_copy_directory(self):
        self.fm.copy_item("folderA", "folderA_backup")
        self.assertTrue((self.base_path / "folderA_backup" / "file2.log").exists())

    def test_delete_file(self):
        self.fm.delete_item("file1.txt")
        self.assertFalse((self.base_path / "file1.txt").exists())

    def test_delete_directory_recursive(self):
        self.fm.delete_item("folderA", recursive=True)
        self.assertFalse((self.base_path / "folderA").exists())
        
    def test_find_files(self):
        results = self.fm.find_files("*.log")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "file2.log")

if __name__ == '__main__':
    # Disable logging output during tests for cleaner console
    logging.disable(logging.CRITICAL)
    unittest.main()
