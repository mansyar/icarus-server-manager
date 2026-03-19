import pytest
from PySide6.QtWidgets import QWidget
from icarus_sentinel.ui.sidebar import SidebarWidget

def test_sidebar_initialization(qtbot):
    """Test that SidebarWidget initializes with expected buttons."""
    sidebar = SidebarWidget()
    qtbot.addWidget(sidebar)
    
    assert hasattr(sidebar, "dashboard_btn")
    assert hasattr(sidebar, "settings_btn")
    assert hasattr(sidebar, "backups_btn")
    assert hasattr(sidebar, "sync_btn")
    assert hasattr(sidebar, "mods_btn")
    assert hasattr(sidebar, "about_btn")

def test_sidebar_navigation_signals(qtbot):
    """Test that sidebar buttons emit signals when clicked."""
    sidebar = SidebarWidget()
    qtbot.addWidget(sidebar)
    
    with qtbot.waitSignal(sidebar.nav_requested, timeout=1000) as blocker:
        sidebar.dashboard_btn.click()
    assert blocker.args == ["dashboard"]
    
    with qtbot.waitSignal(sidebar.nav_requested, timeout=1000) as blocker:
        sidebar.settings_btn.click()
    assert blocker.args == ["settings"]
    
    with qtbot.waitSignal(sidebar.nav_requested, timeout=1000) as blocker:
        sidebar.about_btn.click()
    assert blocker.args == ["about"]
