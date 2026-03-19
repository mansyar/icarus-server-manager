import pytest
from PySide6.QtWidgets import QApplication
from icarus_sentinel.ui.main_window import MainWindow
from icarus_sentinel.ui.sidebar import SidebarWidget

def test_sidebar_has_players_button(qtbot):
    sidebar = SidebarWidget()
    qtbot.addWidget(sidebar)
    
    # Check if players button exists
    assert hasattr(sidebar, "players_btn")
    assert sidebar.players_btn.text() == "Players"

def test_main_window_has_players_tab(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Check if players view exists in stacked widget
    # We need to find the stacked widget first
    from PySide6.QtWidgets import QStackedWidget
    stacked = window.findChild(QStackedWidget)
    
    # Check if any child of stacked is a PlayersView (once we define it)
    # For now, let's just check if we can navigate to 'players'
    with qtbot.waitSignal(window.sidebar.nav_requested, timeout=1000) as blocker:
        window.sidebar.players_btn.click()
        
    assert blocker.args == ["players"]
    assert window.content_stack.currentWidget().objectName() == "PlayersView"
