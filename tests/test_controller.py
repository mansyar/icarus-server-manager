import unittest
from unittest.mock import MagicMock, patch
import os
from icarus_sentinel.controller import Controller

class TestController(unittest.TestCase):
    def setUp(self):
        self.mock_app = MagicMock()
        self.controller = Controller(self.mock_app)

    def test_get_server_executable_finds_shipping(self):
        with patch("os.path.exists", side_effect=lambda p: "Shipping.exe" in p):
            exe = self.controller.get_server_executable("C:/test")
            self.assertIn("Shipping.exe", exe)

    def test_get_server_executable_finds_root(self):
        with patch("os.path.exists", side_effect=lambda p: "IcarusServer.exe" in p and "Binaries" not in p):
            exe = self.controller.get_server_executable("C:/test")
            self.assertIn("IcarusServer.exe", exe)
            self.assertNotIn("Binaries", exe)

    def test_get_server_executable_returns_none_if_missing(self):
        with patch("os.path.exists", return_value=False):
            exe = self.controller.get_server_executable("C:/test")
            self.assertIsNone(exe)

    @patch("threading.Thread")
    def test_run_install_starts_thread(self, mock_thread):
        self.controller.run_install("C:/test")
        mock_thread.assert_called_once()
        self.assertTrue(mock_thread.return_value.daemon)

if __name__ == "__main__":
    unittest.main()
