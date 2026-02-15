"""Service for calculating task recurrence dates."""

from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional


class RecurrenceService:
    """Calculates the next occurrence of a task based on recurrence rules."""

    @staticmethod
    def get_next_date(current_date_str: str, recurrence: str) -> Optional[str]:
        """Calculate the next date/time based on recurrence frequency.

        Args:
            current_date_str: ISO format date or datetime string
            recurrence: DAILY, WEEKLY, MONTHLY

        Returns:
            Next occurrence in same format as input, or None if invalid/NONE
        """
        if not current_date_str or recurrence == "NONE":
            return None

        # Determine format (date vs datetime)
        is_datetime = " " in current_date_str
        date_format = "%Y-%m-%d %H:%M" if is_datetime else "%Y-%m-%d"

        try:
            dt = datetime.strptime(current_date_str, date_format)
        except ValueError:
            return None

        # Apply recurrence logic relative to the ORIGINAL due date
        # (as per Edge Case assumption to maintain cadence)
        if recurrence == "DAILY":
            delta = relativedelta(days=1)
        elif recurrence == "WEEKLY":
            delta = relativedelta(weeks=1)
        elif recurrence == "MONTHLY":
            delta = relativedelta(months=1)
        else:
            return None

        next_dt = dt + delta
        return next_dt.strftime(date_format)
