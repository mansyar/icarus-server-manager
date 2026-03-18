import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Define a mock base class for CustomTkinter
class MockCTk:
    def __init__(self, *args, **kwargs):
        self.tk = MagicMock()
        self.grid = MagicMock()
        self.pack = MagicMock()
        self.pack_forget = MagicMock()
        self.grid_columnconfigure = MagicMock()
        self.grid_rowconfigure = MagicMock()
        self.configure = MagicMock()
        self.title = MagicMock()
        self.geometry = MagicMock()
        self.see = MagicMock()
        self.insert = MagicMock()
        self.delete = MagicMock()
        self.set = MagicMock()
        self.select = MagicMock()
        self.deselect = MagicMock()
        self.get = MagicMock(return_value="")
        self.cget = MagicMock(return_value=None)
        self.destroy = MagicMock()
        self.winfo_children = MagicMock(return_value=[])

    def after(self, ms, func, *args):
        if ms == 0: func(*args)
    def add(self, *args, **kwargs): return MockCTk()

class MockCTkFrame(MockCTk): pass
class MockCTkTextbox(MockCTk): pass
class MockCTkLabel(MockCTk): pass
class MockCTkButton(MockCTk): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._command = kwargs.get("command")
        self.invoke = MagicMock(side_effect=self._run_command)
    
    def _run_command(self):
        if self._command: self._command()

@pytest.fixture(autouse=True)
def mock_ui_dependencies(request):
    """Automatically mocks UI dependencies for all UI tests."""
    ui_test_files = [
        "test_ui", "test_server_mgmt_ui", "test_mod_gui", 
        "test_new_app", "test_sidebar", "test_metrics", 
        "test_console", "test_server_control", "test_style_config"
    ]
    
    is_ui_test = any(name in request.node.fspath.strpath for name in ui_test_files)
    
    if is_ui_test:
        # Mock the entire customtkinter module
        ctk = MagicMock()
        ctk.CTk = MockCTk
        ctk.CTkFrame = MockCTkFrame
        ctk.CTkTextbox = MockCTkTextbox
        ctk.CTkLabel = MockCTkLabel
        ctk.CTkButton = MockCTkButton
        ctk.CTkProgressBar = MockCTk
        ctk.CTkScrollableFrame = MockCTk
        ctk.CTkTabview = MockCTk
        ctk.CTkEntry = MockCTk
        ctk.CTkSwitch = MockCTk
        ctk.CTkCheckBox = MockCTk
        ctk.CTkOptionMenu = MockCTk
        ctk.set_appearance_mode = MagicMock()
        ctk.set_default_color_theme = MagicMock()
        ctk.StringVar.return_value = MagicMock()
        ctk.BooleanVar.return_value = MagicMock()
        ctk.IntVar.return_value = MagicMock()
        ctk.DoubleVar.return_value = MagicMock()
        
        # Use patch.dict to safely mock sys.modules
        with patch.dict("sys.modules", {"customtkinter": ctk}):
            # Ensure 'app' is reloaded with the mocked dependencies
            if "icarus_sentinel.app" in sys.modules:
                import importlib
                importlib.reload(sys.modules["icarus_sentinel.app"])
            yield
    else:
        yield
