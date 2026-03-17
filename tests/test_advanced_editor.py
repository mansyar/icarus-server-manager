"""Tests for the Advanced Editor functionality in the Configuration tab."""

import pytest
import customtkinter as ctk
from app import App
import os

@pytest.fixture
def app():
    """Fixture to provide a clean App instance for each test."""
    state_file = "test_server_state_advanced.json"
    if os.path.exists(state_file):
        os.remove(state_file)
    
    app = App(state_file=state_file)
    yield app
    
    app.destroy()
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
    # Setup some dummy content in INI
    app.ini_manager.save_raw_text("[Section]\nKey=Value\n")
    
    app.tabview.set("Configuration")
    app.config_subtabview.set("Advanced")
    # Manually trigger the handler as .set() might not trigger it in all environments/versions
    app.on_config_tab_change()
    
    content = app.raw_ini_textbox.get("0.0", "end").strip()
    assert "[Section]" in content
    assert "Key=Value" in content
