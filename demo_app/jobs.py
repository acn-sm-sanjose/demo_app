import frappe
import time
from demo_app.integrations.hubspot import update_deal

def validate_capacity(payload=None, **kwargs):
    frappe.set_user("Administrator")
    if not isinstance(payload, dict):
        frappe.throw("Invalid payload")

    deal_id = payload.get("hs_object_id")
    if not deal_id:
        frappe.throw("Missing hs_object_id")

    frappe.logger().info(
        f"[HubSpot] validate_capacity START deal={deal_id}"
    )

    try:
        time.sleep(5)

        requested_capacity = int(payload.get("requested_capacity", 0))

        if requested_capacity <= 20:
            status = "Valid"
            message = "Capacity available"
        else:
            status = "Invalid"
            message = "Insufficient capacity"

        update_deal(
            deal_id,
            {
                "validation_status": status,
                "validation_message": message
            }
        )

        frappe.logger().info(
            f"[HubSpot] Validation {status} sent for deal={deal_id}"
        )

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            f"Validation job failed for deal {deal_id}"
        )
        raise