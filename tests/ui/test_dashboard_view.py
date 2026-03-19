import pytest
from PySide6.QtWidgets import QWidget
from icarus_sentinel.ui.dashboard import DashboardView, MetricsWidget, ControlWidget, ConsoleWidget

def test_dashboard_initialization(qtbot):
    """Test that DashboardView initializes with expected components."""
    view = DashboardView()
    qtbot.addWidget(view)
    
    assert hasattr(view, "cpu_metrics")
    assert hasattr(view, "ram_metrics")
    assert hasattr(view, "control")
    # Console was moved to MainWindow
    assert not hasattr(view, "console")
    assert isinstance(view.cpu_metrics, MetricsWidget)
    assert isinstance(view.ram_metrics, MetricsWidget)
    assert isinstance(view.control, ControlWidget)

def test_metrics_updates(qtbot):
    """Test that MetricsWidget updates values correctly."""
    metrics = MetricsWidget("CPU LOAD")
    qtbot.addWidget(metrics)
    
    metrics.update_value(45.5, "45.5% LOAD")
    assert metrics.bar.value() == 45
    assert "45.5% LOAD" in metrics.status_label.text()

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
    assert blocker.args == [True] # Assuming starts with False, toggles to True
