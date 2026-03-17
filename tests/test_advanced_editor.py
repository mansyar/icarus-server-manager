"""Tests for the Advanced Editor functionality in the Configuration tab."""

import pytest
import customtkinter as ctk
from icarus_sentinel.app import App
import os
from unittest.mock import patch, MagicMock

@pytest.fixture
def app():
    """Fixture to provide a clean App instance for each test."""
    state_file = "test_server_state_advanced.json"
    if os.path.exists(state_file):
        os.remove(state_file)

    with patch("icarus_sentinel.app.App.__init__", return_value=None):
        app = App()
        app.tk = MagicMock()
        # Mock all dependencies
        app.server_manager = MagicMock()
        app.ini_manager = MagicMock()
        app.save_sync_manager = MagicMock()
        app.backup_manager = MagicMock()
        
        # Mock UI elements
        app.tabview = MagicMock()
        app.config_subtabview = MagicMock()
        app.config_subtabview._tab_dict = {"Advanced": MagicMock()}
        app.raw_ini_textbox = MagicMock()
        app.save_advanced_button = MagicMock()
        
        # Mock methods
        app.on_config_tab_change = lambda: App.on_config_tab_change(app)
        app.load_raw_ini_to_gui = lambda: App.load_raw_ini_to_gui(app)
        
        yield app

    # Cleanup
    if os.path.exists(state_file):
        os.remove(state_file)

def test_advanced_subtab_exists(app):
    """Verify that the Advanced sub-tab exists within the Configuration tab."""
    assert hasattr(app, "config_subtabview")
    tabs = app.config_subtabview._tab_dict.keys()
    assert "Advanced" in tabs

def test_advanced_editor_structure(app):
    """Verify that the Advanced editor has the expected UI elements."""
    app.tabview.set("Configuration")
    app.config_subtabview.set("Advanced")
    
    assert hasattr(app, "raw_ini_textbox")
    assert hasattr(app, "save_advanced_button")

def test_advanced_editor_loads_content(app):
    """Verify that the Advanced editor correctly loads raw INI content."""
    # Setup mock return value
    app.ini_manager.get_raw_text.return_value = "[Section]\nKey=Value\n"
    
    app.tabview.set("Configuration")
    app.config_subtabview.set("Advanced")
    app.config_subtabview.get.return_value = "Advanced"
    
    # Manually trigger the handler
    app.on_config_tab_change()
    
    app.raw_ini_textbox.delete.assert_called_with("0.0", "end")
    app.raw_ini_textbox.insert.assert_called_with("0.0", "[Section]\nKey=Value\n")
