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
        app.select_all_cb = MagicMock()
        app.select_all_var = MagicMock()
        
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
    assert hasattr(app_instance, "select_all_cb")

def test_refresh_mod_list_creates_checkboxes(app_instance):
    from icarus_sentinel.app import App
    app_instance.mod_list = MagicMock()
    # Mock winfo_children to simulate clearing the list
    app_instance.mod_list.winfo_children.return_value = []
    
    app_instance.mod_manager.list_mods.return_value = ["mod1.pak", "mod2.pak"]
    
    app_instance.refresh_mod_list = lambda: App.refresh_mod_list(app_instance)
    
    # We need to mock CTkCheckBox because refresh_mod_list will try to instantiate it
    with patch("customtkinter.CTkCheckBox") as mock_checkbox:
        app_instance.refresh_mod_list()
        
        # Should be called twice, once for each mod
        assert mock_checkbox.call_count == 2
        # Use any_call because the first argument is app_instance.mod_list
        mock_checkbox.assert_any_call(app_instance.mod_list, text="mod1.pak")
        mock_checkbox.assert_any_call(app_instance.mod_list, text="mod2.pak")

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

def test_remove_multiple_mods_flow(app_instance):
    from icarus_sentinel.app import App
    app_instance.mod_list = MagicMock()
    
    # Mock checkboxes
    cb1 = MagicMock()
    cb1.get.return_value = 1
    cb1.cget.return_value = "mod1.pak"
    
    cb2 = MagicMock()
    cb2.get.return_value = 0 # Not checked
    cb2.cget.return_value = "mod2.pak"
    
    cb3 = MagicMock()
    cb3.get.return_value = 1
    cb3.cget.return_value = "mod3.pak"
    
    app_instance.mod_list.winfo_children.return_value = [cb1, cb2, cb3]
    
    app_instance.remove_mod_ui = lambda: App.remove_mod_ui(app_instance)
    app_instance.refresh_mod_list = MagicMock()
    
    # Mock messagebox
    with patch("icarus_sentinel.app.messagebox.askyesno", return_value=True):
        app_instance.remove_mod_ui()
    
    # Should call remove_mod for cb1 and cb3
    assert app_instance.mod_manager.remove_mod.call_count == 2
    app_instance.mod_manager.remove_mod.assert_any_call("mod1.pak")
    app_instance.mod_manager.remove_mod.assert_any_call("mod3.pak")
    app_instance.refresh_mod_list.assert_called_once()
