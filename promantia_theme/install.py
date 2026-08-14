import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

from promantia_theme.theme_registry import get_allowed_theme_values, get_app_theme_values

DESK_THEME_PROPERTY_SETTER = "User-desk_theme-options"
DEFAULT_DESK_THEME = "Light"

# --- Install Hooks ---
def after_install():
	"""Makes this app's themes valid values of User.desk_theme right after installation."""
	sync_desk_theme_options()


def after_migrate():
	"""Re-applies the desk theme options, which a doctype sync or a registry change can invalidate."""
	sync_desk_theme_options()


def before_uninstall():
	"""Leaves no user stranded on a theme whose stylesheet is about to disappear."""
	reset_users_on_app_themes()
	remove_desk_theme_options()


# --- Helpers ---
def sync_desk_theme_options():
	"""Widens the User.desk_theme select to the registered themes, keeping any options set elsewhere."""
	options = merge_desk_theme_options()
	if options == get_current_desk_theme_options():
		return

	make_property_setter(
		"User",
		"desk_theme",
		"options",
		"\n".join(options),
		"Text",
		is_system_generated=False,
	)
	frappe.clear_cache(doctype="User")


def merge_desk_theme_options():
	"""Returns the registered theme values followed by any extra option another app or admin added."""
	options = get_allowed_theme_values()
	options.extend(option for option in get_current_desk_theme_options() if option not in options)
	return options


def get_current_desk_theme_options():
	"""Returns the User.desk_theme select options currently in effect on this site."""
	field = frappe.get_meta("User").get_field("desk_theme")
	if not field or not field.options:
		return []

	return [option.strip() for option in field.options.split("\n") if option.strip()]


def reset_users_on_app_themes():
	"""Moves every user sitting on one of this app's themes back to the stock light theme."""
	for theme in get_app_theme_values():
		frappe.db.set_value(
			"User", {"desk_theme": theme}, "desk_theme", DEFAULT_DESK_THEME, update_modified=False
		)


def remove_desk_theme_options():
	"""Drops the property setter so User.desk_theme falls back to its shipped select options."""
	if frappe.db.exists("Property Setter", DESK_THEME_PROPERTY_SETTER):
		frappe.delete_doc("Property Setter", DESK_THEME_PROPERTY_SETTER, ignore_permissions=True)
		frappe.clear_cache(doctype="User")
