import pytest
from unittest.mock import MagicMock, patch
import sys
import os

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
    def grid_columnconfigure(self, *args, **kwargs):
        pass
    def grid_rowconfigure(self, *args, **kwargs):
        pass
    def after(self, ms, func, *args):
        # Immediately call the func to simulate it being called
        func(*args)
    def configure(self, *args, **kwargs):
        pass
    def grid(self, *args, **kwargs):
        pass

class MockCTkFrame(MockCTk):
    pass

# Mock the entire customtkinter module
customtkinter = MagicMock()
customtkinter.CTk = MockCTk
customtkinter.CTkFrame = MockCTkFrame
customtkinter.CTkButton = MagicMock()
customtkinter.CTkTextbox = MagicMock()
customtkinter.CTkLabel = MagicMock()
customtkinter.CTkEntry = MagicMock()
sys.modules["customtkinter"] = customtkinter

# Mock steam_manager and server_manager
sys.modules["steam_manager"] = MagicMock()
sys.modules["server_manager"] = MagicMock()

import app
from app import App

@pytest.fixture
def app_instance():
    with patch("app.ctk.CTk.title"), \
         patch("app.ctk.CTk.geometry"):
        return App()

def test_ui_has_server_mgmt_buttons(app_instance):
    assert hasattr(app_instance, "start_button")
    assert hasattr(app_instance, "stop_button")
    assert hasattr(app_instance, "restart_button")
    assert hasattr(app_instance, "cpu_label")
    assert hasattr(app_instance, "ram_label")
