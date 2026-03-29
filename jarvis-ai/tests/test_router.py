"""
Tests: Router
Tests for route_command and prompt builders.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.router import build_reasoning_prompt, build_coding_prompt, route_command


class TestPromptBuilders(unittest.TestCase):

    def test_reasoning_prompt_contains_input(self):
        prompt = build_reasoning_prompt("check cpu usage")
        self.assertIn("check cpu usage", prompt)
        self.assertIn("intent", prompt)
        self.assertIn("requires_code", prompt)

    def test_coding_prompt_contains_input(self):
        prompt = build_coding_prompt("list all files", {})
        self.assertIn("list all files", prompt)
        self.assertIn("Python", prompt)


class TestRouteCommand(unittest.TestCase):

    @patch("core.router.ollama")
    def test_returns_none_on_model_failure(self, mock_ollama):
        mock_ollama.generate_json.return_value = None
        result = route_command("do something")
        self.assertIsNone(result)

    @patch("core.router.ollama")
    def test_direct_execution_type(self, mock_ollama):
        mock_ollama.generate_json.return_value = {
            "intent": "check_cpu",
            "requires_permission": False,
            "requires_code": False,
            "description": "Check CPU usage"
        }
        result = route_command("check cpu")
        self.assertEqual(result["execution_type"], "direct")
        self.assertEqual(result["intent"], "check_cpu")

    @patch("core.router.ollama")
    def test_script_execution_type(self, mock_ollama):
        mock_ollama.generate_json.return_value = {
            "intent": "custom_task",
            "requires_permission": False,
            "requires_code": True,
            "description": "Custom task"
        }
        mock_ollama.generate.return_value = "print('hello')"
        result = route_command("write me a script")
        self.assertEqual(result["execution_type"], "script")
        self.assertIn("generated_code", result)


if __name__ == "__main__":
    unittest.main()
