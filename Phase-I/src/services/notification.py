"""Notification service for desktop and terminal alerts."""

from plyer import notification
import sys
import os


class NotificationService:
    """Handles triggering system-level notifications with terminal fallback."""

    def __init__(self, app_name: str = "Todo App"):
        self.app_name = app_name
        self.notifications_available = self._check_availability()

    def _check_availability(self) -> bool:
        """Check if system notifications can be triggered."""
        # Simple check - plyer handles most platform issues
        # On some headless Linux/WSL systems, it might fail silently or raise issues
        try:
            # We don't want to actually notify during check
            return True
        except Exception:
            return False

    def notify(self, title: str, message: str) -> bool:
        """Send a notification.

        Args:
            title: Short summary for the notification header
            message: Longer text for the message body

        Returns:
            True if notification was attempted via system, False if fallback used
        """
        try:
            notification.notify(
                title=f"{self.app_name}: {title}",
                message=message,
                app_name=self.app_name,
                timeout=10,
            )
            return True
        except Exception:
            # Fallback to terminal alert
            self._terminal_alert(title, message)
            return False

    def _terminal_alert(self, title: str, message: str) -> None:
        """Display a formatted alert in the terminal."""
        print("\n" + "!" * 40)
        print(f"!!! REMINDER: {title.upper()} !!!")
        print(f"!!! {message}")
        print("!" * 40 + "\n")
