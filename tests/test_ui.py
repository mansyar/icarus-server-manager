import pytest
from unittest.mock import MagicMock, patch
import sys

# Define a mock base class
class MockCTk:
    def __init__(self, *args, **kwargs):
        pass
    def title(self, title):
        pass
    def geometry(self, geometry):
        pass
    def mainloop(self):
        pass

# Mock the entire customtkinter module
customtkinter = MagicMock()
customtkinter.CTk = MockCTk
sys.modules["customtkinter"] = customtkinter

import app
from app import App

def test_app_initialization():
    with patch.object(App, "title") as mock_title, \
         patch.object(App, "geometry") as mock_geometry:
        a = App()
        mock_title.assert_called_with("Icarus Sentinel")
        mock_geometry.assert_called_with("800x600")

def test_main():
    with patch("app.App") as MockApp:
        instance = MockApp.return_value
        app.main()
        MockApp.assert_called_once()
        instance.mainloop.assert_called_once()
