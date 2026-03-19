import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from icarus_sentinel.ui.main_window import MainWindow
from icarus_sentinel.ui.sidebar import SidebarWidget
from PySide6.QtWidgets import QFrame

class DummySidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nav_requested = MagicMock()
        self.players_btn = MagicMock()
        self.dashboard_btn = MagicMock()

def test_sidebar_has_players_button(qtbot):
    sidebar = SidebarWidget()
    qtbot.addWidget(sidebar)
    
    # Check if players button exists
    assert hasattr(sidebar, "players_btn")
    assert sidebar.players_btn.text() == "Players"

@patch("icarus_sentinel.ui.main_window.A2SQueryService")
@patch("icarus_sentinel.ui.main_window.MainWindow.setup_a2s_monitoring")
@patch("icarus_sentinel.ui.main_window.Controller")
@patch("icarus_sentinel.ui.main_window.SidebarWidget")
@patch("icarus_sentinel.ui.main_window.DashboardView")
@patch("icarus_sentinel.ui.main_window.ConfigView")
@patch("icarus_sentinel.ui.main_window.BackupsView")
@patch("icarus_sentinel.ui.main_window.SaveSyncView")
@patch("icarus_sentinel.ui.main_window.ModsView")
@patch("icarus_sentinel.ui.main_window.AboutView")
@patch("icarus_sentinel.ui.main_window.ConsoleWidget")
def test_main_window_has_players_tab(mock_console, mock_about, mock_mods, mock_sync, 
                                     mock_backups, mock_config, mock_dashboard, 
                                     mock_sidebar, mock_controller, mock_setup, 
                                     mock_service, qtbot):
    # Configure mock controller
    mock_controller.return_value.server_started = MagicMock()
    
    # Use dummy widget for sidebar
    sidebar = DummySidebar()
    mock_sidebar.return_value = sidebar
    
    # Configure mock views to be QWidgets
    from PySide6.QtWidgets import QWidget
    for m in [mock_dashboard, mock_config, mock_backups, mock_sync, mock_mods, mock_about, mock_console]:
        inst = QWidget()
        m.return_value = inst
        if m == mock_dashboard:
            inst.control = MagicMock()
            inst.control.action_triggered = MagicMock()
            
    window = MainWindow()
    qtbot.addWidget(window)
    
    # In this case we are checking navigation via the mock
    window._on_nav_requested("players")
    
    assert window.content_stack.currentWidget().objectName() == "PlayersView"
    
    window.close()
