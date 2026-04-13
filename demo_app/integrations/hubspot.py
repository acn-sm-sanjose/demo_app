import frappe
import requests

HUBSPOT_BASE_URL = "https://api.hubapi.com"

def update_deal(deal_id, properties: dict):
    token = frappe.conf.get("hubspot_private_app_token")

    if not token:
        frappe.throw("HubSpot token not configured")

    url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/deals/{deal_id}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "properties": properties
    }

    response = requests.patch(url, json=payload, headers=headers, timeout=15)

    if not response.ok:
        frappe.log_error(
            message=response.text,
            title="HubSpot Deal Update Failed"
        )
        response.raise_for_status()

    return response.json()
