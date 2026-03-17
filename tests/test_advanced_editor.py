import pytest
import customtkinter as ctk
from app import App
import os

@pytest.fixture
def app():
    state_file = "test_server_state_advanced.json"
    if os.path.exists(state_file):
        os.remove(state_file)
    
    app = App(state_file=state_file)
    yield app
    
    app.destroy()
    if os.path.exists(state_file):
        os.remove(state_file)

def test_advanced_subtab_exists(app):
    # Verify "Advanced" section exists within Configuration
    # This might be implemented as a sub-tabview or just a section
    # Let's assume a sub-tabview for now as per "Advanced section (e.g., a sub-tab...)" in spec
    assert hasattr(app, "config_subtabview")
    tabs = app.config_subtabview._tab_dict.keys()
    assert "Advanced" in tabs

def test_advanced_editor_structure(app):
    app.tabview.set("Configuration")
    app.config_subtabview.set("Advanced")
    
    assert hasattr(app, "raw_ini_textbox")
    assert hasattr(app, "save_advanced_button")

def test_advanced_editor_loads_content(app):
    # Setup some dummy content in INI
    app.ini_manager.save_raw_text("[Section]\nKey=Value\n")
    
    app.tabview.set("Configuration")
    app.config_subtabview.set("Advanced")
    
    # This should trigger loading if we implement it on tab change or init
    content = app.raw_ini_textbox.get("0.0", "end").strip()
    assert "[Section]" in content
    assert "Key=Value" in content
