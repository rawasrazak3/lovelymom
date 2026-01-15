import frappe
from frappe.model.document import Document

class PrizeCode(Document):
	pass

@frappe.whitelist(allow_guest=True)
def validate_code(code, usr_name=None, usr_phone=None, usr_place=None):
	if not code:
		return {"status": "error", "message": "Please enter a code."}
	
	if not usr_name or not usr_phone or not usr_place:
		return {"status": "error", "message": "Please provide Name, Phone and Place."}

	prize_code = frappe.db.get_value("Prize Code", {"code": code}, ["name", "result_type", "prize", "is_used", "active", "image"], as_dict=True)

	if not prize_code:
		return {"status": "error", "message": "Invalid Code. Please try again."}

	if prize_code.active != "Active":
		return {"status": "error", "message": "This code is inactive."}
    
	# Create Log Entry
	try:
		log = frappe.get_doc({
			"doctype": "Prize Redeem Log",
			"user_name": usr_name,
			"phone_number": usr_phone,
			"place": usr_place,
			"prize_code": code,
			"prize": prize_code.prize if prize_code.result_type == "Win" else "Better Luck Next Time"
		})
		log.insert(ignore_permissions=True)
	except Exception as e:
		frappe.log_error(f"Error creating Prize Redeem Log: {str(e)}", "Prize Redeem Log Error")

	return {
		"status": "success",
		"result_type": prize_code.result_type,
		"prize": prize_code.prize,
		"is_used": prize_code.is_used,
		"image": prize_code.image
	}
