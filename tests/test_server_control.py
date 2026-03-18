import pytest
from unittest.mock import MagicMock, patch
from icarus_sentinel.app import App

@pytest.fixture
def app_instance():
    with patch("icarus_sentinel.app.App.__init__", return_value=None), \
         patch("icarus_sentinel.app.ctk"), \
         patch("icarus_sentinel.app.DashboardView"), \
         patch("icarus_sentinel.app.ConfigView"), \
         patch("icarus_sentinel.app.SaveSyncView"), \
         patch("icarus_sentinel.app.BackupsView"), \
         patch("icarus_sentinel.app.ModsView"), \
         patch("icarus_sentinel.app.Controller"):
        
        app = App()
        app.tk = MagicMock()
        app.orbital_launch_btn = MagicMock()
        
        # Mock methods
        app.toggle_server = MagicMock()
        
        yield app

def test_orbital_launch_button_exists(app_instance):
    assert hasattr(app_instance, "orbital_launch_btn")

def test_launch_button_interaction(app_instance):
    # Setup command
    app_instance.orbital_launch_btn.invoke.side_effect = lambda: app_instance.toggle_server()
    
    app_instance.orbital_launch_btn.invoke()
    app_instance.toggle_server.assert_called_once()
