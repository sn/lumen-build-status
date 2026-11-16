"""Tests for the plugin's logic, without a running Lumen.

    PYTHONPATH="$(lumen python-path)" python3 -m unittest discover -s tests
"""

import json
import re
import os
import runpy
import stat
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import lumen_plugin  # noqa: E402

lumen_plugin.Plugin.run = lambda self, main=None: None  # load a plugin without connecting


def load(name):
    """Run the plugin's main.py with its own fresh data folder; return its globals."""
    os.environ["LUMEN_PLUGIN_DATA"] = tempfile.mkdtemp()
    os.environ["LUMEN_PLUGIN"] = name
    return runpy.run_path(os.path.join(ROOT, "main.py"))



class BuildStatusTests(unittest.TestCase):
    def test_build_commands_are_recognised(self):
        name = load("build-status")["build_name"]
        cases = {
            "cargo test --release": "cargo test", "make -j8": "make", "sudo make install": "make",
            "RUST_LOG=1 cargo build": "cargo build", "cargo fmt": None, "ls": None, "git commit": None,
            "./gradlew build": "./gradlew", "npm test": "npm test", "echo 'unbalanced": None, "": None,
            "cd api && cargo test": "cargo test", "make; ls": "make", "git pull && npm ci": "npm ci",
            "cargo build && cargo test -q | tee log": "cargo test",
        }
        for command, want in cases.items():
            self.assertEqual(name(command), want, command)

    def test_its_own_titles_are_recognised(self):
        p = load("build-status")
        for title, ours in [("✓ cargo test · 12s", True), ("✗ make · exit 2 · 3m 05s", True),
                            ("mine", False), ("✓ my tab", False)]:
            self.assertEqual(p["is_ours"](title), ours, title)
