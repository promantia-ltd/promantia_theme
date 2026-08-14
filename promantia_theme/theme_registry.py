"""Single source of truth for the desk themes this app makes selectable."""

# --- Slugs ---
# The one theme whose values come from a doctype instead of a stylesheet. Shared with
# promantia_theme/custom_theme.py and public/js/custom_theme.js, which key off the same slug.
CUSTOM_THEME_SLUG = "promantia-custom"

# --- Registry ---
# Frappe's built-in themes, re-declared so overriding ThemeSwitcher.fetch_themes() keeps them selectable.
STOCK_DESK_THEMES = (
	{"name": "light", "label": "Frappe Light", "info": "Light Theme"},
	{"name": "dark", "label": "Timeless Night", "info": "Dark Theme"},
	{
		"name": "automatic",
		"label": "Automatic",
		"info": "Uses system's theme to switch between light and dark mode",
	},
)

# Themes shipped by this app. The `name` must match a `[data-theme="..."]` block in public/scss/themes/.
APP_DESK_THEMES = (
	{
		"name": "tekton-blue",
		"label": "Tekton Blue",
		"info": "Tekton's deep blue desk theme",
	},
	{
		"name": "horizon-calm",
		"label": "Horizon Calm",
		"info": "Soft light surfaces, hairline borders and a muted indigo accent",
	},
	{
		"name": "magenta-aurora",
		"label": "Magenta Aurora",
		"info": "Vivid magenta accents under a plum-to-fuchsia gradient navbar",
	},
	{
		"name": "paper-ledger",
		"label": "Paper Ledger",
		"info": "Powder-blue chrome, cream data-entry surfaces and ink-black actions",
	},
	{
		"name": CUSTOM_THEME_SLUG,
		"label": "Promantia Custom Theme",
		"info": "Colors a System Manager configures in the Promantia Custom Theme settings",
	},
)


# --- Accessors ---
def get_desk_themes():
	"""Returns every desk theme selectable while this app is installed, in display order."""
	return [dict(theme) for theme in (*STOCK_DESK_THEMES, *APP_DESK_THEMES)]


def get_app_desk_themes():
	"""Returns only the themes contributed by this app."""
	return [dict(theme) for theme in APP_DESK_THEMES]


def get_stored_theme_value(theme_name):
	"""Converts a theme slug to the User.desk_theme value the desk stores, mirroring its toTitle()."""
	return theme_name[:1].upper() + theme_name[1:]


def get_allowed_theme_values():
	"""Returns the accepted User.desk_theme values, in selection order."""
	return [get_stored_theme_value(theme["name"]) for theme in get_desk_themes()]


def get_app_theme_values():
	"""Returns the User.desk_theme values that only exist while this app is installed."""
	return [get_stored_theme_value(theme["name"]) for theme in APP_DESK_THEMES]
