import pytest
import customtkinter as ctk
from app import App
import os

@pytest.fixture
def app():
    # Use a temporary state file for testing
    state_file = "test_server_state_gui.json"
    if os.path.exists(state_file):
        os.remove(state_file)
    
    app = App(state_file=state_file)
    yield app
    
    # Cleanup
    app.destroy()
    if os.path.exists(state_file):
        os.remove(state_file)

def test_configuration_tab_exists(app):
    # Verify "Configuration" tab is in the tabview
    # By default it's not there yet, so this should fail
    tabs = app.tabview._tab_dict.keys()
    assert "Configuration" in tabs

def test_configuration_tab_structure(app):
    # This test will only pass after the tab is created
    # Check for fields in the "Configuration" tab
    app.tabview.set("Configuration")
    config_tab = app.tabview.tab("Configuration")
    
    # We expect these attributes to be created on the app or within the tab
    assert hasattr(app, "server_name_entry")
    assert hasattr(app, "server_password_entry")
    assert hasattr(app, "admin_password_entry")
    assert hasattr(app, "server_port_entry")
    assert hasattr(app, "update_on_launch_var")
    assert hasattr(app, "update_on_launch_checkbox")
    assert hasattr(app, "save_config_button")

def test_configuration_fields_initial_state(app):
    # Verify fields are populated from ini_manager (which should be initialized)
    app.tabview.set("Configuration")
    
    # Assuming ini_manager has some defaults or is loaded from a mock/temp file
    # This might require mocking ini_manager or setting up a temp INI file
    assert app.server_name_entry.get() != ""
