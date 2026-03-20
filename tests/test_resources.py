import pytest
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
import sys

# Import the resource module to register the icons
import icarus_sentinel.ui.resources_rc

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app

def test_app_icon_resource_is_loadable(qapp):
    """Verifies that the app_icon.png resource can be loaded as a QIcon."""
    icon = QIcon(":/icons/app_icon.png")
    # If the resource is NOT loaded, icon.isNull() should be True
    assert not icon.isNull(), "Icon resource ':/icons/app_icon.png' could not be loaded. Ensure resources_rc is imported."
