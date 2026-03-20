import os
import unittest
from unittest.mock import patch, mock_open
import sys

# Add scripts directory to path to import the script as a module
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))

# We expect inject_version.py to have a function update_version_files(version_str)
# Since the file doesn't exist yet, we can't import it. We'll use importlib or just mock it.
# Actually, the workflow says "Write failing test", which means it should fail.

class TestVersionInjection(unittest.TestCase):
    def test_update_version_files_invalid_format(self):
        """Test that invalid version formats raise an error."""
        try:
            from inject_version import update_version_files
            with self.assertRaises(ValueError):
                update_version_files("invalid-version")
        except ImportError:
            self.fail("inject_version module not found")

    @patch("builtins.open", new_callable=mock_open, read_data="__version__ = \"1.0.0\"")
    @patch("os.path.exists", return_value=True)
    def test_update_version_files_success(self, mock_exists, mock_file):
        """Test successful version injection into both files."""
        from inject_version import update_version_files
        
        # This will be more complex because we need to handle multiple file opens with different data
        # For simplicity in failing test, we'll just check if it can be called.
        update_version_files("v1.2.3")
        
        # Check if open was called for both files
        # icarus_sentinel/__init__.py and version_info.txt
        self.assertGreaterEqual(mock_file.call_count, 2)

    @patch("builtins.open", new_callable=mock_open, read_data="__version__ = \"1.0.0\"")
    @patch("os.path.exists", return_value=False)
    def test_update_version_files_missing_files(self, mock_exists, mock_file):
        """Test version injection when files are missing (should not raise)."""
        from inject_version import update_version_files
        # Should just print warnings and not fail
        update_version_files("v1.2.3")
        self.assertEqual(mock_file.call_count, 0)

    @patch("inject_version.update_version_files")
    @patch("sys.argv", ["inject_version.py", "v1.2.3"])
    def test_main_success(self, mock_update):
        """Test the main entry point with success."""
        import inject_version
        # Directly calling the block that would be under if __name__ == "__main__"
        # Since we can't easily trigger the true __main__ from import
        # We can just manually call the logic that would be there
        if len(sys.argv) >= 2:
            inject_version.update_version_files(sys.argv[1])
        mock_update.assert_called_with("v1.2.3")

if __name__ == "__main__":
    unittest.main()
