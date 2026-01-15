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
    
    # Optional logic: If used, do we reject?
    # User said: "a option to check whather it is a prize or better luck next time, and a check box to set whather it is used ot not"
    # User also said: "if there code won or the code has chekced with it has prize we need to show them they have won"
    # Usually if it is used, we might want to say it's already redeemed. But for now I'll just return the status.
	
	return {
		"status": "success",
		"result_type": prize_code.result_type,
		"prize": prize_code.prize,
		"is_used": prize_code.is_used,
		"image": prize_code.image
	}
