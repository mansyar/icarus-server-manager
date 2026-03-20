import pytest
from PySide6.QtWidgets import QTextEdit
from icarus_sentinel.ui.dashboard import ConsoleWidget
from icarus_sentinel import style_config

def test_console_log_html_injection(qtbot):
    """Verify that log messages are injected as HTML with correct colors."""
    widget = ConsoleWidget()
    qtbot.addWidget(widget)
    
    # Test Sentinel log (Blue)
    widget.log("Sentinel message", source="sentinel")
    html = widget.text_area.toHtml()
    assert style_config.COLOR_SENTINEL.lower() in html.lower()
    assert "Sentinel message" in widget.text_area.toPlainText()
    
    # Test Server log (Orange)
    widget.log("Server message", source="server")
    html = widget.text_area.toHtml()
    assert style_config.COLOR_SERVER.lower() in html.lower()
    assert "Server message" in widget.text_area.toPlainText()

def test_console_auto_scroll(qtbot):
    """Verify that console auto-scrolls to bottom on new log."""
    widget = ConsoleWidget()
    widget.setFixedHeight(100) # Small height to force scroll
    qtbot.addWidget(widget)
    
    # Add many lines
    for i in range(50):
        widget.log(f"Line {i}")
        
    scrollbar = widget.text_area.verticalScrollBar()
    assert scrollbar.value() == scrollbar.maximum()
