import frappe
import unittest
from lovelymom.lovelymom.doctype.prize_code.prize_code import validate_code

class TestPrizeCode(unittest.TestCase):
	def setUp(self):
		frappe.db.delete("Prize Code")

	def create_code(self, code, prize, result_type, active="Active", is_used=0):
		doc = frappe.get_doc({
			"doctype": "Prize Code",
			"code": code,
			"prize": prize,
			"result_type": result_type,
			"active": active,
			"is_used": is_used
		})
		doc.insert()
		return doc

	def test_valid_win(self):
		self.create_code("WIN123", "iPhone", "Win")
		result = validate_code("WIN123")
		self.assertEqual(result.get("status"), "success")
		self.assertEqual(result.get("result_type"), "Win")
		self.assertEqual(result.get("prize"), "iPhone")

	def test_valid_loss(self):
		self.create_code("LOSS123", "", "Better Luck Next Time")
		result = validate_code("LOSS123")
		self.assertEqual(result.get("status"), "success")
		self.assertEqual(result.get("result_type"), "Better Luck Next Time")

	def test_invalid_code(self):
		result = validate_code("INVALID")
		self.assertEqual(result.get("status"), "error")
		self.assertIn("Invalid Code", result.get("message"))

	def test_inactive_code(self):
		self.create_code("INACTIVE", "Prize", "Win", active="Inactive")
		result = validate_code("INACTIVE")
		self.assertEqual(result.get("status"), "error")
		self.assertIn("inactive", result.get("message"))
