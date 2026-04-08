# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — Abstract Base Channel Provider
"""
from abc import ABC, abstractmethod


class BaseChannelProvider(ABC):
    """Abstract base for all notification channel providers."""

    def __init__(self, channel_doc):
        self.channel = channel_doc

    @abstractmethod
    def send(self, recipient: str, content: str, template: str | None = None) -> dict:
        """Send a message. Returns dict with at least message_id."""
        ...

    @abstractmethod
    def check_delivery(self, message_id: str) -> dict:
        """Check delivery status. Returns dict with status."""
        ...

    @abstractmethod
    def validate_recipient(self, identifier: str) -> bool:
        """Validate recipient identifier format."""
        ...

    @abstractmethod
    def health_check(self) -> bool:
        """Check if provider is reachable."""
        ...

    def get_cost(self, message_type: str = "text", destination: str = "") -> float:
        """Return estimated cost per message."""
        return 0.0
