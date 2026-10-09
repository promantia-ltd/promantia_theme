app_name = "promantia_theme"
app_title = "Promantia Theme"
app_publisher = "Promantia Business Solutions Pvt Ltd"
app_description = "Desk themes for Frappe: Tekton Blue, Horizon Calm, Magenta Aurora and Paper Ledger."
app_email = "notifications@promantia.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# esbuild resolves these from promantia_theme/public/**; the .scss bundle is served as .css
app_include_js = ["promantia_theme.bundle.js"]
app_include_css = ["promantia_theme.bundle.css"]

# Boot
# ----
# Publishes the theme registry to the desk so the theme switcher does not repeat it

extend_bootinfo = "promantia_theme.boot.extend_bootinfo"

# Website
# -------
# Adds the Promantia Custom Theme login appearance to the login route's <head>. Doing it here
# rather than through web_include_* keeps every other portal page free of this app's assets.

update_website_context = "promantia_theme.custom_theme.update_website_context"

# Overriding Methods
# ------------------
# frappe's own switch_theme only accepts Light/Dark/Automatic

override_whitelisted_methods = {
	"frappe.core.doctype.user.user.switch_theme": "promantia_theme.overrides.user.switch_theme"
}

# Installation
# ------------

after_install = "promantia_theme.install.after_install"
after_migrate = "promantia_theme.install.after_migrate"

# Uninstallation
# --------------

before_uninstall = "promantia_theme.install.before_uninstall"
