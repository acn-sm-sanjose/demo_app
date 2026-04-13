import frappe

@frappe.whitelist(allow_guest=True)
def receive_validation_request(**payload):
    """
    1. Receives webhook from HubSpot
    2. Enqueues background validation job
    3. Returns immediately
    """

    frappe.enqueue(
        "demo_app.jobs.validate_capacity",
        queue="default",
        payload=payload,
        user="Administrator"
    )

    return {
        "hubspot object id": payload["hs_object_id"]
    }