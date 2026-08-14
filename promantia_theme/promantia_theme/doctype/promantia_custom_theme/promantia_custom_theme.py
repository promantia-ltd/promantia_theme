import frappe
from frappe import _
from frappe.model.document import Document


class PromantiaCustomTheme(Document):
	# --- Controller Methods ---
	def validate(self):
		self._validate_default_app()

	# --- Validate Utils ---
	def _validate_default_app(self):
		"""Keeps a hidden app switcher from pointing the desk logo at an app nobody can reach."""
		if not self.hide_app_switcher:
			self.default_app = None
			return

		if not self.default_app:
			frappe.throw(_("Default App is required when Hide App Switcher is enabled."))

		if self.default_app not in frappe.get_installed_apps():
			frappe.throw(_("App {0} is not installed on this site.").format(self.default_app))
