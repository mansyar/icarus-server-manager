import pytest
from PySide6.QtCore import Qt
from icarus_sentinel.ui.components import ToggleSwitch

def test_toggle_switch_initial_state(qtbot):
    toggle = ToggleSwitch()
    qtbot.addWidget(toggle)
    
    assert toggle.isChecked() is False
    assert toggle.isCheckable() is True

def test_toggle_switch_click(qtbot):
    toggle = ToggleSwitch()
    qtbot.addWidget(toggle)
    
    qtbot.mouseClick(toggle, Qt.LeftButton)
    assert toggle.isChecked() is True
    
    qtbot.mouseClick(toggle, Qt.LeftButton)
    assert toggle.isChecked() is False

def test_toggle_switch_set_checked(qtbot):
    toggle = ToggleSwitch()
    qtbot.addWidget(toggle)
    
    toggle.setChecked(True)
    assert toggle.isChecked() is True
    
    toggle.setChecked(False)
    assert toggle.isChecked() is False
