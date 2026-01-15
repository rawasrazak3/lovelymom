import frappe
from frappe.model.document import Document

class PrizeCode(Document):
	pass

@frappe.whitelist(allow_guest=True)
def validate_code(code):
	if not code:
		return {"status": "error", "message": "Please enter a code."}

	prize_code = frappe.db.get_value("Prize Code", {"code": code}, ["name", "result_type", "prize", "is_used", "active", "image"], as_dict=True)

	if not prize_code:
		return {"status": "error", "message": "Invalid Code. Please try again."}

	if prize_code.active != "Active":
		return {"status": "error", "message": "This code is inactive."}
    
	return {
		"status": "success",
		"result_type": prize_code.result_type,
		"prize": prize_code.prize,
		"is_used": prize_code.is_used,
		"image": prize_code.image
	}
