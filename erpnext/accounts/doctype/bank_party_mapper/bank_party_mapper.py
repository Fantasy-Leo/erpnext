# Copyright (c) 2023, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BankPartyMapper(Document):
	def on_update(self):
		self.update_party_in_linked_transactions()

	def update_party_in_linked_transactions(self):
		if self.is_new():
			return

		# Set updated party values in other linked bank transactions
		bank_transaction = frappe.qb.DocType("Bank Transaction")

		frappe.qb.update(bank_transaction).set("party_type", self.party_type).set(
			"party", self.party
		).where(
			(bank_transaction.bank_party_mapper == self.name)
			& ((bank_transaction.party_type != self.party_type) | (bank_transaction.party != self.party))
		).run()