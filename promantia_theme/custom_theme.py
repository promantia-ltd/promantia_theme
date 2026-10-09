"""Serves the Promantia Custom Theme configuration to the desk and to the login page."""

import re

import frappe

CUSTOM_THEME_DOCTYPE = "Promantia Custom Theme"
DESK_FOOTER_TEMPLATE = "promantia_theme/templates/includes/desk_footer.html"

# Routes whose <head> gets the login appearance. The login page is public, so it cannot be
# gated on a user's desk_theme the way the desk styling is.
LOGIN_ROUTES = ("login", "update-password")

# Only these fields ever leave the server for a desk, which is what lets the settings doctype
# stay System Manager only while every user's desk can still render the theme.
DESK_THEME_FIELDS = (
	"navbar_background_color",
	"navbar_text_color",
	"hide_help",
	"hide_app_switcher",
	"default_app",
	"primary_button_background_color",
	"primary_button_text_color",
	"primary_button_hover_background_color",
	"primary_button_hover_text_color",
	"secondary_button_background_color",
	"secondary_button_text_color",
	"secondary_button_hover_background_color",
	"secondary_button_hover_text_color",
	"body_background_color",
	"content_background_color",
	"content_text_color",
	"sidebar_background_color",
	"sidebar_text_color",
	"input_background_color",
	"input_border_color",
	"input_text_color",
	"input_label_color",
	"table_head_background_color",
	"table_head_text_color",
	"table_body_background_color",
	"table_body_text_color",
	"number_card_background_color",
	"number_card_border_color",
	"number_card_text_color",
	"footer_background_color",
	"footer_text_color",
	"sticky_footer",
)

# CSS rules for the login page, keyed by the field that switches each one on. The login page
# carries none of this app's stylesheets, so these are emitted as complete rules rather than
# as custom properties, and every one of them is scoped to #page-login.
LOGIN_RULES_BY_FIELD = {
	"login_background_color": "#page-login {{ background-color: {value}; }}",
	"login_background_image": (
		'#page-login {{ background-image: url("{value}"); background-size: cover;'
		" background-position: center center; background-repeat: no-repeat; }}"
	),
	"login_box_background_color": (
		"#page-login .login-content.page-card {{ background-color: {value}; border-color: {value}; }}"
	),
	"login_heading_text_color": "#page-login .page-card-head h4 {{ color: {value}; }}",
	"login_button_background_color": (
		"#page-login .btn-primary.btn-login, #page-login .btn-primary.btn-forgot"
		" {{ background-color: {value}; }}"
	),
	"login_button_text_color": (
		"#page-login .btn-primary.btn-login, #page-login .btn-primary.btn-forgot {{ color: {value}; }}"
	),
	"login_button_hover_background_color": (
		"#page-login .btn-primary.btn-login:hover, #page-login .btn-primary.btn-forgot:hover"
		" {{ background-color: {value}; }}"
	),
	"login_button_hover_text_color": (
		"#page-login .btn-primary.btn-login:hover, #page-login .btn-primary.btn-forgot:hover"
		" {{ color: {value}; }}"
	),
}

LOGIN_BOX_ALIGNMENT_BY_POSITION = {
	"Left": "flex-start",
	"Right": "flex-end",
}

HEX_COLOR_PATTERN = re.compile(r"^#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
# Attached filenames on this site may contain spaces, which are legal inside a quoted CSS url().
# Quotes, parentheses, backslashes and semicolons are excluded so the value cannot break out.
SITE_RELATIVE_PATH_PATTERN = re.compile(r"^/[\w\-./% ]+$")


# --- Website Hooks ---
def update_website_context(context):
	"""Adds the configured login appearance to the login route's head, so no asset or fetch is needed."""
	if _current_route() not in LOGIN_ROUTES:
		return

	style_tag = _build_login_style_tag()
	if not style_tag:
		return

	# head_html, not head_include: login.html and update-password.html both override the
	# head_include block, which would silently drop anything added there.
	return {"head_html": (context.get("head_html") or "") + style_tag}


# --- Update Website Context Helpers ---
def _current_route():
	return (getattr(frappe.local, "path", "") or "").strip("/")


def _build_login_style_tag():
	theme = get_custom_theme_settings()
	rules = _collect_login_rules(theme)
	if not rules:
		return ""

	return f'<style id="promantia-login-theme">{"".join(rules)}</style>'


def _collect_login_rules(theme):
	rules = []

	for field, rule in LOGIN_RULES_BY_FIELD.items():
		value = _sanitized_login_value(theme, field)
		if value:
			rules.append(rule.format(value=value))

	login_box_rule = _login_box_position_rule(theme)
	if login_box_rule:
		rules.append(login_box_rule)

	return rules


def _sanitized_login_value(theme, field):
	"""Refuses anything that is not a plain hex color or a site-relative file path."""
	value = theme.get(field)
	if not value:
		return ""

	if field == "login_background_image":
		return value if SITE_RELATIVE_PATH_PATTERN.match(value) else ""

	return value if HEX_COLOR_PATTERN.match(value) else ""


def _login_box_position_rule(theme):
	"""Aligns the login box with flexbox, which keeps the page in flow at every viewport width."""
	alignment = LOGIN_BOX_ALIGNMENT_BY_POSITION.get(theme.get("login_box_position"))
	if not alignment:
		return ""

	selectors = (
		"#page-login .for-login, #page-login .for-signup,"
		" #page-login .for-forgot, #page-login .for-login-with-email-link"
	)

	return (
		f"@media (min-width: 768px) {{ {selectors}"
		f" {{ display: flex; flex-direction: column; align-items: {alignment}; padding: 0 8%; }} }}"
	)


# --- Helpers ---
def get_custom_theme_settings():
	"""Reads the singleton without a permission check, so callers must expose only allow-listed fields."""
	return frappe.get_cached_doc(CUSTOM_THEME_DOCTYPE, CUSTOM_THEME_DOCTYPE)


# --- Whitelisted Methods ---
@frappe.whitelist()
def get_desk_custom_theme():
	"""Returns the desk-facing theme values for the logged-in user, plus the rendered desk footer."""
	theme = get_custom_theme_settings()
	config = {field: theme.get(field) for field in DESK_THEME_FIELDS if theme.get(field)}

	footer_html = _render_desk_footer(theme)
	if footer_html:
		config["footer_html"] = footer_html

	return config


@frappe.whitelist()
def get_installed_app_options():
	"""Returns the apps the Default App select may hold, for the settings form only."""
	frappe.only_for("System Manager")
	return [app for app in frappe.get_installed_apps() if app != "frappe"]


# --- Get Desk Custom Theme Helpers ---
def _render_desk_footer(theme):
	if not (theme.copyright_text or theme.footer_powered_by):
		return ""

	return frappe.render_template(
		DESK_FOOTER_TEMPLATE,
		{
			"copyright_text": theme.copyright_text,
			"footer_powered_by": theme.footer_powered_by,
			"sticky_footer": theme.sticky_footer,
		},
	)
