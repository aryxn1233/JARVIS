"""
Tests: Command Executor
Tests for execute_command and safety filter.
"""

import sys
import os
import unittest

# Allow imports from parent directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from executor.command_executor import is_dangerous, handle_direct_intent


class TestIsDangerous(unittest.TestCase):

    def test_blocks_rm_rf(self):
        self.assertTrue(is_dangerous("rm -rf /"))

    def test_blocks_uppercase_bypass(self):
        self.assertTrue(is_dangerous("RM -RF /"))

    def test_blocks_windows_format(self):
        self.assertTrue(is_dangerous("format C:"))

    def test_blocks_fork_bomb(self):
        self.assertTrue(is_dangerous(":(){ :|:& };:"))

    def test_allows_safe_code(self):
        self.assertFalse(is_dangerous("print('hello world')"))

    def test_allows_psutil_code(self):
        self.assertFalse(is_dangerous("import psutil; print(psutil.cpu_percent())"))


class TestHandleDirectIntent(unittest.TestCase):

    def test_unknown_intent(self):
        result = handle_direct_intent("nonexistent_intent")
        self.assertIn("No direct handler", result)

    def test_check_cpu(self):
        result = handle_direct_intent("check_cpu")
        self.assertIn("CPU", result)

    def test_check_ram(self):
        result = handle_direct_intent("check_ram")
        self.assertIn("RAM", result)

    def test_check_disk(self):
        result = handle_direct_intent("check_disk")
        self.assertIn("Disk", result)


if __name__ == "__main__":
    unittest.main()
