import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Base class for all mock widgets to avoid MagicMock inheritance issues
class MockBase:
    def __init__(self, *args, **kwargs):
        self.master = kwargs.get("master")
        self._last_child_ids = None
        self._w = "mock_w"
        self.tk = MagicMock()
        self.grid = MagicMock()
        self.pack = MagicMock()
        self.grid_columnconfigure = MagicMock()
        self.grid_rowconfigure = MagicMock()
        self.grid_forget = MagicMock()
        self.pack_forget = MagicMock()
        self.destroy = MagicMock()
        self.configure = MagicMock()
        self.winfo_children = MagicMock(return_value=[])
        self.get = MagicMock(return_value="")
        self.cget = MagicMock(return_value="")
        self.set = MagicMock()
        self.bind = MagicMock()
        self.unbind = MagicMock()
        self.after = MagicMock(side_effect=lambda ms, f, *a: f(*a) if ms == 0 else None)
        self.mainloop = MagicMock()
        if "command" in kwargs:
            self.invoke = MagicMock(side_effect=kwargs["command"])
        else:
            self.invoke = MagicMock()

    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)
        return MagicMock()

# Create the mock module
mock_ctk = MagicMock()
mock_ctk.CTk = MockBase
mock_ctk.CTkFrame = MockBase
mock_ctk.CTkTextbox = MockBase
mock_ctk.CTkLabel = MockBase
mock_ctk.CTkButton = MockBase
mock_ctk.CTkProgressBar = MockBase
mock_ctk.CTkScrollableFrame = MockBase
mock_ctk.CTkTabview = MockBase
mock_ctk.CTkEntry = MockBase
mock_ctk.CTkSwitch = MockBase
mock_ctk.CTkCheckBox = MockBase
mock_ctk.CTkOptionMenu = MockBase
mock_ctk.set_appearance_mode = MagicMock()
mock_ctk.set_default_color_theme = MagicMock()
mock_ctk.StringVar = MagicMock
mock_ctk.BooleanVar = MagicMock
mock_ctk.IntVar = MagicMock
mock_ctk.DoubleVar = MagicMock

# Apply the mock to sys.modules
sys.modules["customtkinter"] = mock_ctk

@pytest.fixture(autouse=True)
def mock_ui_dependencies(request):
    """Automatically mocks UI dependencies for all UI tests."""
    ui_test_files = [
        "test_ui", "test_server_mgmt_ui", "test_mod_gui", 
        "test_new_app", "test_sidebar", "test_metrics", 
        "test_console", "test_server_control", "test_style_config",
        "test_responsive", "test_ui_thresholds", "test_server_launch"
    ]
    
    is_ui_test = any(name in request.node.fspath.strpath for name in ui_test_files)
    
    if is_ui_test:
        with patch("tkinter.Tk", MockBase), \
             patch("tkinter.Label", MockBase), \
             patch("tkinter.Frame", MockBase), \
             patch("tkinter.Canvas", MockBase):
            yield
    else:
        yield
