import datetime
import logging

import httpx

from .const import BASE_URL

_LOGGER = logging.getLogger(__name__)


class Checker:
    """Get a process Skomer avalibilities."""

    def __init__(self):
        """Initialize the Skomer Checker."""
        self.data = None
        self.date = datetime.datetime.now().date()
        self.url = BASE_URL

    def _build_url(self, date: datetime.date) -> str:
        """Build the URL."""
        return f"{self.url}/{date.year:02d}/{date.month:02d}"

    def get_data(self, date: datetime.date) -> dict | None:
        """Get the data."""
        url = self._build_url(date)
        try:
            with httpx.Client(follow_redirects=True) as client:
                _LOGGER.debug("Requesting data from %s", url)
                response = client.get(url)
                response.raise_for_status()
                return response.json()["calendar"]
        except httpx.RequestError as err:
            _LOGGER.error("Error during request: %s", err)
            return None
