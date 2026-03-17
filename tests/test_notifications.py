import pytest
from unittest.mock import patch, MagicMock

from icarus_sentinel.notification_manager import NotificationManager

@patch("icarus_sentinel.notification_manager.Notification")
def test_notify_calls_winotify(mock_notification_class):
    mock_notification_instance = mock_notification_class.return_value
    manager = NotificationManager()
    
    manager.notify("Alert", "Test Message")
    
    mock_notification_class.assert_called_once_with(
        app_id="Icarus Sentinel",
        title="Alert",
        msg="Test Message"
    )
    mock_notification_instance.show.assert_called_once()
