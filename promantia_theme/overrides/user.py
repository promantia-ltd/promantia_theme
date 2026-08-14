import frappe

from promantia_theme.theme_registry import get_allowed_theme_values

# --- Overridden Whitelisted Methods ---
@frappe.whitelist()
def switch_theme(theme):
	"""Persists the chosen desk theme, widening frappe's own switch_theme to this app's registry."""
	if theme in get_allowed_theme_values():
		frappe.db.set_value("User", frappe.session.user, "desk_theme", theme)
