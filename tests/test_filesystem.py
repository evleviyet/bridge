"""
Dosya sistemi testleri
"""
import unittest
import os
import shutil
from src.core.filesystem import BoltFileSystem

class TestBoltFileSystem(unittest.TestCase):
    def setUp(self):
        self.test_base = "test_filesystem"
        self.fs = BoltFileSystem(self.test_base)
        
    def tearDown(self):
        if os.path.exists(self.test_base):
            shutil.rmtree(self.test_base)
            
    def test_create_project(self):
        self.assertTrue(self.fs.create_project("test_project"))
        self.assertTrue(os.path.exists(os.path.join(self.test_base, "test_project")))
        
    def test_write_and_read_file(self):
        self.fs.create_project("test_project")
        content = "test content"
        self.assertTrue(self.fs.write_file("test_project", "test.txt", content, "user1"))
        self.assertEqual(self.fs.read_file("test_project", "test.txt"), content)
        
    def test_file_locking(self):
        self.fs.create_project("test_project")
        self.assertTrue(self.fs.lock_file("test_project", "test.txt", "user1"))
        self.assertFalse(self.fs.lock_file("test_project", "test.txt", "user2"))
        self.assertTrue(self.fs.unlock_file("test_project", "test.txt", "user1"))

if __name__ == '__main__':
    unittest.main()