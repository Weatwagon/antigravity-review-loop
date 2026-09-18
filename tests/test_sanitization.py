#!/usr/bin/env python3
"""
test_sanitization.py - Validates that the distribution package is completely free of personal identifiers.
"""

import unittest
import os
import re
from pathlib import Path

# Terms that MUST NEVER appear in the public release
FORBIDDEN_PATTERNS = [
    re.compile(r"\bzack\b", re.IGNORECASE),
    re.compile(r"C:\\Users\\", re.IGNORECASE),
    re.compile(r"/home/zack", re.IGNORECASE),
    re.compile(r"/Users/zack", re.IGNORECASE),
    re.compile(r"D:\\Sources\\repos", re.IGNORECASE),
]

# Extensions to scan
TEXT_EXTENSIONS = {".py", ".md", ".json", ".sh", ".ps1", ".txt", ".yml", ".yaml"}


class TestSanitization(unittest.TestCase):

    def test_zero_personal_information_leaks(self):
        """Ensure all distribution files contain zero personal or machine-specific identifiers."""
        dist_root = Path(__file__).parent.parent
        violations = []

        for root, dirs, files in os.walk(dist_root):
            # Skip hidden directories and git folders
            dirs[:] = [d for d in dirs if not d.startswith((".", "__"))]
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in TEXT_EXTENSIONS:
                    file_path = Path(root) / file
                    # Skip this test file itself so it doesn't match its own forbidden patterns
                    if file_path.name == "test_sanitization.py":
                        continue
                    try:
                        content = file_path.read_text(encoding="utf-8", errors="replace")
                        for line_no, line in enumerate(content.splitlines(), start=1):
                            for pattern in FORBIDDEN_PATTERNS:
                                if pattern.search(line):
                                    rel_path = file_path.relative_to(dist_root)
                                    violations.append(
                                        f"File: {rel_path}:L{line_no} matches '{pattern.pattern}' -> {line.strip()}"
                                    )
                    except Exception as e:
                        violations.append(f"Failed to read {file_path}: {e}")

        if violations:
            msg = "\nPersonal Information Leak Detected:\n" + "\n".join(violations)
            self.fail(msg)


if __name__ == "__main__":
    unittest.main()
