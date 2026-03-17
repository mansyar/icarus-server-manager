"""Module for handling Windows system notifications.
"""

from winotify import Notification

class NotificationManager:
    """Handles sending desktop notifications to the user.
    """

    def __init__(self, app_id="Icarus Sentinel"):
        """Initializes the NotificationManager.

        Args:
            app_id (str): The application name to display in notifications.
        """
        self.app_id = app_id

    def notify(self, title, message):
        """Sends a Windows toast notification.

        Args:
            title (str): The notification title.
            message (str): The notification message body.
        """
        toast = Notification(
            app_id=self.app_id,
            title=title,
            msg=message
        )
        toast.show()
