import frappe

def test_doctype():
    try:
        # Check if doctype exists
        if not frappe.db.exists("DocType", "Prize Redeem Log"):
            print("DocType 'Prize Redeem Log' NOT FOUND in database.")
            return

        print("DocType 'Prize Redeem Log' found.")

        # Try to insert a record
        doc = frappe.get_doc({
            "doctype": "Prize Redeem Log",
            "user_name": "Test User",
            "phone_number": "1234567890",
            "place": "Test Place",
            "prize_code": "TEST-CODE",
            "prize": "Test Prize"
        })
        doc.insert(ignore_permissions=True)
        print(f"Successfully inserted document: {doc.name}")
        
        # Cleanup
        doc.delete()
        print("Successfully deleted test document.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    frappe.init(site="sahee.com", sites_path="sites")
    frappe.connect()
    test_doctype()
