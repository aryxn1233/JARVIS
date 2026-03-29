"""
Tests: Permission Manager
Tests for check_permission logic.
"""

import sys
import os
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from permission.permission_manager import check_permission, CRITICAL_INTENTS


class TestCheckPermission(unittest.TestCase):

    def test_non_critical_no_permission_required(self):
        """Non-critical intent with no flag → auto-approved."""
        plan = {"intent": "check_cpu", "requires_permission": False}
        result = check_permission(plan)
        self.assertTrue(result)

    @patch("permission.permission_manager.ask_permission", return_value=True)
    def test_critical_intent_always_prompts(self, mock_ask):
        """Critical intent always requires confirmation, even without flag."""
        for intent in CRITICAL_INTENTS:
            plan = {"intent": intent, "requires_permission": False}
            result = check_permission(plan)
            self.assertTrue(result)

    @patch("permission.permission_manager.ask_permission", return_value=False)
    def test_critical_intent_denied(self, mock_ask):
        """Critical intent denied when user says no."""
        plan = {"intent": "shutdown", "requires_permission": False}
        result = check_permission(plan)
        self.assertFalse(result)

    @patch("permission.permission_manager.ask_permission", return_value=True)
    def test_non_critical_with_flag_prompts(self, mock_ask):
        """Non-critical intent with requires_permission=True → prompts."""
        plan = {"intent": "open_browser", "requires_permission": True}
        result = check_permission(plan)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
