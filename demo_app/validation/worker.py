
print("✅ demo_app.validation.worker LOADED")

import frappe
from demo_app.integrations.hubspot import update_deal


def validate_one_deal():
    record = frappe.db.sql("""
        SELECT hs_object_id, requested_capacity
        FROM deal_validation_queue
        WHERE validation_status = 'Pending'
        ORDER BY hs_object_id
        LIMIT 1
    """, as_dict=True)

    if not record:
        print("[Process 2] No Pending records found")
        return

    record = record[0]
    hs_object_id = record["hs_object_id"]
    requested_capacity = record["requested_capacity"]

    print(f"[Process 2] Processing Deal ID: {hs_object_id}")
    print(f"[Process 2] Requested Capacity: {requested_capacity}")

    # ✅ Validation logic (PoC)
    if requested_capacity <= 10:
        status = "Valid"
        message = "Requested capacity is within allowed limit"
    else:
        status = "Invalid"
        message = "Requested capacity exceeds allowed limit"

    frappe.db.sql("""
        UPDATE deal_validation_queue
        SET validation_status = %s,
            validation_message = %s
        WHERE hs_object_id = %s
    """, (status, message, hs_object_id))

    frappe.db.commit()

    update_deal(
        hs_object_id,
        {
            "validation_status": status,
            "validation_message": message
        }
    )

    print(f"[Process 2] Deal {hs_object_id} marked as {status}")
    print("[Process 2] Validation completed\n")
