# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
NotifyPro — Email Channel Provider (wraps Frappe email)
"""
import frappe
from notifypro.channels.base_provider import BaseChannelProvider


class EmailProvider(BaseChannelProvider):
    def send(self, recipient: str, content: str, template: str | None = None) -> dict:
        frappe.sendmail(
            recipients=[recipient],
            subject=content[:100] if not template else template,
            message=content,
            now=True,
        )
        return {"message_id": f"email-{frappe.generate_hash(length=10)}"}

    def check_delivery(self, message_id: str) -> dict:
        return {"status": "sent"}

    def validate_recipient(self, identifier: str) -> bool:
        return "@" in identifier and "." in identifier

    def health_check(self) -> bool:
        return True
