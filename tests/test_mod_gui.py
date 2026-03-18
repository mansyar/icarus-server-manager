import pytest
from unittest.mock import MagicMock, patch
import os

@pytest.fixture
def app_instance():
    from icarus_sentinel.app import App
    with patch("icarus_sentinel.app.App.__init__", return_value=None):
        app = App()
        app.tabview = MagicMock()
        app.tabview.add = MagicMock()
        
        # Mock dependencies
        app.mod_manager = MagicMock()
        app.console_output = MagicMock()
        
        # Mock methods that might be called during init_mods_tab
        app.refresh_mod_list = MagicMock()
        
        yield app

def test_init_mods_tab_creates_widgets(app_instance):
    from icarus_sentinel.app import App
    app_instance.mods_tab = MagicMock()
    
    # Inject the method to test
    app_instance.init_mods_tab = lambda: App.init_mods_tab(app_instance)
    
    app_instance.init_mods_tab()
    
    # Verify widgets are created
    assert hasattr(app_instance, "mod_list")
    assert hasattr(app_instance, "install_mod_btn")
    assert hasattr(app_instance, "remove_mod_btn")
    assert hasattr(app_instance, "sync_warning_label")

def test_refresh_mod_list(app_instance):
    from icarus_sentinel.app import App
    app_instance.mod_list = MagicMock()
    app_instance.mod_manager.list_mods.return_value = ["mod1.pak", "mod2.pak"]
    
    app_instance.refresh_mod_list = lambda: App.refresh_mod_list(app_instance)
    app_instance.refresh_mod_list()
    
    app_instance.mod_manager.list_mods.assert_called_once()
    # Depending on implementation, it might insert into a textbox or listbox
    # I'll check for insert calls
    assert app_instance.mod_list.insert.called

@patch("icarus_sentinel.app.filedialog.askopenfilenames")
def test_install_mod_flow_single(mock_askopen, app_instance):
    from icarus_sentinel.app import App
    mock_askopen.return_value = ["C:/downloads/awesome_mod.pak"]
    
    app_instance.install_mod_ui = lambda: App.install_mod_ui(app_instance)
    app_instance.refresh_mod_list = MagicMock()
    
    app_instance.install_mod_ui()
    
    app_instance.mod_manager.install_mod.assert_called_with("C:/downloads/awesome_mod.pak")
    app_instance.refresh_mod_list.assert_called_once()

@patch("icarus_sentinel.app.filedialog.askopenfilenames")
def test_install_multiple_mods_flow(mock_askopen, app_instance):
    from icarus_sentinel.app import App
    mock_askopen.return_value = ["C:/downloads/mod1.pak", "C:/downloads/mod2.zip"]
    
    app_instance.install_mod_ui = lambda: App.install_mod_ui(app_instance)
    app_instance.refresh_mod_list = MagicMock()
    
    app_instance.install_mod_ui()
    
    assert app_instance.mod_manager.install_mod.call_count == 2
    app_instance.mod_manager.install_mod.assert_any_call("C:/downloads/mod1.pak")
    app_instance.mod_manager.install_mod.assert_any_call("C:/downloads/mod2.zip")
    app_instance.refresh_mod_list.assert_called()
