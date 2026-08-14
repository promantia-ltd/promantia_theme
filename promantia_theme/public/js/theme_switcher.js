frappe.provide("frappe.ui");

// Extends the desk theme switcher with the themes published on boot by promantia_theme.boot
frappe.ui.ThemeSwitcher = class PromantiaThemeSwitcher extends frappe.ui.ThemeSwitcher {
	fetch_themes() {
		const registered_themes = frappe.boot && frappe.boot.promantia_desk_themes;

		// fall back to frappe's built-in list when boot info is stale or unavailable
		if (!registered_themes || !registered_themes.length) {
			return super.fetch_themes();
		}

		this.themes = registered_themes.map((theme) => ({
			name: theme.name,
			label: __(theme.label),
			info: __(theme.info),
		}));

		return Promise.resolve(this.themes);
	}
};
