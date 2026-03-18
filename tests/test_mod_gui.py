import pytest
from unittest.mock import MagicMock, patch
import os
from icarus_sentinel.app import App

@pytest.fixture
def app_instance():
    # Define a real class for CTkCheckBox mock to satisfy isinstance
    class MockCTkCheckBox(MagicMock): pass

    with patch("icarus_sentinel.app.App.__init__", return_value=None), \
         patch("icarus_sentinel.app.ctk") as mock_ctk, \
         patch("icarus_sentinel.app.DashboardView"), \
         patch("icarus_sentinel.app.ConfigView"), \
         patch("icarus_sentinel.app.SaveSyncView"), \
         patch("icarus_sentinel.app.BackupsView"), \
         patch("icarus_sentinel.app.ModsView"):
        
        mock_ctk.CTkCheckBox = MockCTkCheckBox
        
        app = App()
        app.tk = MagicMock()
        app.main_content_frame = MagicMock()
        app.controller = MagicMock()
        
        # Mock dependencies
        app.mod_manager = MagicMock()
        app.console_output = MagicMock()
        
        # UI Elements that would be created by ModsView
        app.mod_list = MagicMock()
        app.select_all_cb = MagicMock()
        app.select_all_var = MagicMock()
        
        # Mock methods
        app.refresh_mod_list = lambda: App.refresh_mod_list(app)
        app.install_mod_ui = lambda: App.install_mod_ui(app)
        app.remove_mod_ui = lambda: App.remove_mod_ui(app)
        app.toggle_select_all_mods = lambda: App.toggle_select_all_mods(app)
        app.log = MagicMock()
        
        yield app

def test_refresh_mod_list_creates_checkboxes(app_instance):
    app_instance.mod_list.winfo_children.return_value = []
    app_instance.mod_manager.list_mods.return_value = ["mod1.pak", "mod2.pak"]
    
    from icarus_sentinel.app import ctk
    with patch.object(ctk, "CTkCheckBox") as mock_checkbox:
        app_instance.refresh_mod_list()
        
        assert mock_checkbox.call_count == 2
        mock_checkbox.assert_any_call(app_instance.mod_list, text="mod1.pak")
        mock_checkbox.assert_any_call(app_instance.mod_list, text="mod2.pak")

@patch("icarus_sentinel.app.filedialog.askopenfilenames")
def test_install_mod_flow_single(mock_askopen, app_instance):
    mock_askopen.return_value = ["C:/downloads/awesome_mod.pak"]
    
    app_instance.install_mod_ui()
    
    app_instance.mod_manager.install_mod.assert_called_with("C:/downloads/awesome_mod.pak")

@patch("icarus_sentinel.app.filedialog.askopenfilenames")
def test_install_multiple_mods_flow(mock_askopen, app_instance):
    mock_askopen.return_value = ["C:/downloads/mod1.pak", "C:/downloads/mod2.zip"]
    
    app_instance.install_mod_ui()
    
    assert app_instance.mod_manager.install_mod.call_count == 2
    app_instance.mod_manager.install_mod.assert_any_call("C:/downloads/mod1.pak")
    app_instance.mod_manager.install_mod.assert_any_call("C:/downloads/mod2.zip")

def test_remove_multiple_mods_flow(app_instance):
    from icarus_sentinel.app import ctk
    # Mock checkboxes using the class that satisfies isinstance
    cb1 = ctk.CTkCheckBox()
    cb1.get.return_value = 1
    cb1.cget.return_value = "mod1.pak"
    
    cb2 = MagicMock() # This one will fail isinstance if we wanted it to, but let's be consistent
    cb2 = ctk.CTkCheckBox()
    cb2.get.return_value = 0 # Not checked
    cb2.cget.return_value = "mod2.pak"
    
    cb3 = ctk.CTkCheckBox()
    cb3.get.return_value = 1
    cb3.cget.return_value = "mod3.pak"
    
    app_instance.mod_list.winfo_children.return_value = [cb1, cb2, cb3]
    
    # Mock messagebox
    with patch("icarus_sentinel.app.messagebox.askyesno", return_value=True):
        app_instance.remove_mod_ui()
    
    # Should call remove_mod for cb1 and cb3
    assert app_instance.mod_manager.remove_mod.call_count == 2
    app_instance.mod_manager.remove_mod.assert_any_call("mod1.pak")
    app_instance.mod_manager.remove_mod.assert_any_call("mod3.pak")
