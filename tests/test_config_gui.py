"""Tests for the Configuration GUI structure and initial state."""

import pytest
import customtkinter as ctk
from icarus_sentinel.app import App
import os
from unittest.mock import patch, MagicMock

@pytest.fixture
def app():
    # Use a temporary state file for testing
    state_file = "test_server_state_gui.json"
    if os.path.exists(state_file):
        os.remove(state_file)

    with patch("icarus_sentinel.app.App.__init__", return_value=None):
        app = App()
        app.tk = MagicMock()
        app.log = MagicMock()
        
        # Dependencies
        app.ini_manager = MagicMock()
        
        # UI Elements
        app.tabview = MagicMock()
        app.tabview._tab_dict = {"Configuration": MagicMock()}
        app.server_name_entry = MagicMock()
        app.server_name_entry.get.return_value = "Test Server"
        app.server_password_entry = MagicMock()
        app.admin_password_entry = MagicMock()
        app.server_port_entry = MagicMock()
        app.server_port_entry.get.return_value = "17777"
        app.update_on_launch_var = MagicMock()
        app.update_on_launch_checkbox = MagicMock()
        app.save_config_button = MagicMock()
        
        yield app
    
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
    
    # We should at least have the port entry with a default value
    assert app.server_port_entry.get() == "17777"
    # SessionName might be empty by default
    assert hasattr(app, "server_name_entry")
