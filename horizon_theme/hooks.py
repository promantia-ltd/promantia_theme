app_name = "horizon_theme"
app_title = "Horizon Theme"
app_publisher = "Promantia Business Solutions Pvt Ltd"
app_description = "Desk themes for Frappe: Tekton Blue plus the Horizon Calm theme derived from the Horizontal_Main design kit."
app_email = "notifications@promantia.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# esbuild resolves these from horizon_theme/public/**; the .scss bundle is served as .css
app_include_js = ["horizon_theme.bundle.js"]
app_include_css = ["horizon_theme.bundle.css"]

# Boot
# ----
# Publishes the theme registry to the desk so the theme switcher does not repeat it

extend_bootinfo = "horizon_theme.boot.extend_bootinfo"

# Overriding Methods
# ------------------
# frappe's own switch_theme only accepts Light/Dark/Automatic

override_whitelisted_methods = {
	"frappe.core.doctype.user.user.switch_theme": "horizon_theme.overrides.user.switch_theme"
}

# Installation
# ------------

after_install = "horizon_theme.install.after_install"
after_migrate = "horizon_theme.install.after_migrate"

# Uninstallation
# --------------

before_uninstall = "horizon_theme.install.before_uninstall"
