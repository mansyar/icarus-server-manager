import pytest
from unittest.mock import MagicMock, patch
import sys

# Define a mock base class for CustomTkinter
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
        # Call immediately if ms is 0 (UI update), but not for long waits (monitoring loop)
        if ms == 0:
            func(*args)
    def configure(self, *args, **kwargs):
        pass
    def grid(self, *args, **kwargs):
        pass
    def destroy(self):
        pass

class MockCTkFrame(MockCTk):
    pass

@pytest.fixture(autouse=True)
def mock_ui_dependencies(request):
    """Automatically mocks UI dependencies only for UI-related tests."""
    # Only apply these mocks to files that start with 'test_ui' or 'test_server_mgmt_ui'
    if "test_ui" in request.node.fspath.strpath or "test_server_mgmt_ui" in request.node.fspath.strpath or "test_mod_gui" in request.node.fspath.strpath:
        # Mock the entire customtkinter module
        customtkinter = MagicMock()
        customtkinter.CTk = MockCTk
        customtkinter.CTkFrame = MockCTkFrame
        customtkinter.CTkButton = MagicMock()
        customtkinter.CTkTextbox = MagicMock()
        customtkinter.CTkLabel = MagicMock()
        customtkinter.CTkEntry = MagicMock()
        
        # Configure server_manager mock
        server_mgr_mock = MagicMock()
        server_mgr_mock.ServerProcessManager.return_value.state = {"pid": None, "status": "stopped"}
        
        # Use patch.dict to safely mock sys.modules for the duration of the test
        with patch.dict("sys.modules", {
            "customtkinter": customtkinter,
            "steam_manager": MagicMock(),
            "server_manager": server_mgr_mock
        }):
            # Ensure 'app' is reloaded with the mocked dependencies if it was already imported
            # and it's NOT already using our mock (to avoid redundant reloads/hangs)
            if "icarus_sentinel.app" in sys.modules:
                import importlib
                app_module = sys.modules["icarus_sentinel.app"]
                if not isinstance(app_module.ctk, MagicMock):
                    importlib.reload(app_module)
            yield
    else:
        yield
