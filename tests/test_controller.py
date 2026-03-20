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

    @patch("icarus_sentinel.controller.QThread")
    @patch("icarus_sentinel.controller.InstallWorker")
    def test_run_install_starts_thread(self, mock_worker, mock_qthread):
        # Mock worker to avoid signal connection errors with MagicMock
        mock_worker_instance = MagicMock()
        mock_worker.return_value = mock_worker_instance
        
        # We need to mock the signals as well to avoid Shiboken errors
        mock_worker_instance.finished = MagicMock()
        mock_worker_instance.error = MagicMock()
        mock_worker_instance.progress = MagicMock()
        mock_worker_instance.progress_source = MagicMock()
        
        self.controller.run_install("C:/test")
        
        mock_qthread.return_value.start.assert_called_once()
        mock_worker.assert_called_once()

if __name__ == "__main__":
    unittest.main()
