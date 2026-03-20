import pytest
from unittest.mock import patch, MagicMock

from icarus_sentinel.notification_manager import NotificationManager

@patch("icarus_sentinel.notification_manager.Notification")
@patch("os.path.exists", return_value=True)
@patch("icarus_sentinel.constants.get_resource_path", return_value="C:/path/to/icon.png")
def test_notify_calls_winotify(mock_get_path, mock_exists, mock_notification_class):
    mock_notification_instance = mock_notification_class.return_value
    manager = NotificationManager()

    manager.notify("Alert", "Test Message")

    mock_notification_class.assert_called_once_with(
        app_id="Icarus Sentinel",
        title="Alert",
        msg="Test Message",
        duration="short",
        icon="C:/path/to/icon.png"
    )
    mock_notification_instance.show.assert_called_once()
