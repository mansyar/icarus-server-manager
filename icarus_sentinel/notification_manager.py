import os
from winotify import Notification
from icarus_sentinel import constants

class NotificationManager:
    """Handles sending desktop notifications to the user.
    """

    def __init__(self, app_id="Icarus Sentinel"):
        """Initializes the NotificationManager.

        Args:
            app_id (str): The application name to display in notifications.
        """
        self.app_id = app_id
        self.icon_path = constants.get_resource_path(os.path.join("assets", "rocket.PNG"))

    def notify(self, title, message):
        """Sends a Windows toast notification.

        Args:
            title (str): The notification title.
            message (str): The notification message body.
        """
        try:
            toast = Notification(
                app_id=self.app_id,
                title=title,
                msg=message,
                duration="short",
                icon=self.icon_path if os.path.exists(self.icon_path) else None
            )
            toast.show()
        except Exception as e:
            # Use print for background thread logging if needed, or rely on caller callback
            print(f"DEBUG: Notification failed: {e}")
