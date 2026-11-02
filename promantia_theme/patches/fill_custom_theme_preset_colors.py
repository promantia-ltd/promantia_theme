import frappe

from promantia_theme.custom_theme import CUSTOM_THEME_DOCTYPE, get_preset_colors


def execute():
	"""Gives every blank palette field its preset, leaving anything a System Manager already chose untouched.

	A settings doc that was never saved already reads its colors from the doctype defaults, so it
	has no blanks and nothing is written for it.
	"""
	theme = frappe.get_single(CUSTOM_THEME_DOCTYPE)
	blank_colors = {field: color for field, color in get_preset_colors().items() if not theme.get(field)}
	if blank_colors:
		frappe.db.set_single_value(CUSTOM_THEME_DOCTYPE, blank_colors)
