import pytest
from PySide6.QtWidgets import QWidget
from icarus_sentinel.ui.dashboard import DashboardView, MetricsWidget, ControlWidget, ConsoleWidget

def test_dashboard_initialization(qtbot):
    """Test that DashboardView initializes with expected components."""
    view = DashboardView()
    qtbot.addWidget(view)
    
    assert hasattr(view, "metrics")
    assert hasattr(view, "control")
    assert hasattr(view, "console")
    assert isinstance(view.metrics, MetricsWidget)
    assert isinstance(view.control, ControlWidget)
    assert isinstance(view.console, ConsoleWidget)

def test_metrics_updates(qtbot):
    """Test that MetricsWidget updates values correctly."""
    metrics = MetricsWidget()
    qtbot.addWidget(metrics)
    
    metrics.update_metrics(cpu=45.5, ram=12.2)
    # Check if labels or internal state updated
    assert "45.5%" in metrics.cpu_label.text()
    assert "12.2GB" in metrics.ram_label.text()

def test_console_append(qtbot):
    """Test that ConsoleWidget appends text correctly."""
    console = ConsoleWidget()
    qtbot.addWidget(console)
    
    console.log("System Check")
    assert "System Check" in console.text_area.toPlainText()

def test_control_button_click(qtbot):
    """Test that ControlWidget button emits signal."""
    control = ControlWidget()
    qtbot.addWidget(control)
    
    with qtbot.waitSignal(control.action_triggered, timeout=1000) as blocker:
        control.launch_btn.click()
    assert blocker.args == [True] # Assuming True for start
