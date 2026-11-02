frappe.ui.form.on("Promantia Custom Theme", {
	// --- Standard Events ---
	refresh(frm) {
		frm.events.load_default_app_options(frm);
		frm.events.add_apply_theme_button(frm);
		frm.events.add_restore_default_colors_button(frm);
	},

	// --- Field Change Events ---
	hide_app_switcher(frm) {
		if (!frm.doc.hide_app_switcher) {
			frm.set_value("default_app", "");
		}
	},

	// --- Helper Functions ---
	async load_default_app_options(frm) {
		const apps = await frappe.xcall("promantia_theme.custom_theme.get_installed_app_options");
		frm.set_df_property("default_app", "options", ["", ...(apps || [])]);
	},

	// Saving stores the values; the desk only re-reads them on the next load unless nudged
	add_apply_theme_button(frm) {
		frm.add_custom_button(__("Apply Theme"), () => {
			if (!promantia_theme.custom_theme) {
				frappe.msgprint(
					__("Select the Promantia Custom Theme from Toggle Theme to see it applied.")
				);
				return;
			}

			promantia_theme.custom_theme.refresh();
			frappe.show_alert({ message: __("Theme applied"), indicator: "green" });
		});
	},

	// Fills the form only - nothing changes until the System Manager reviews and saves
	add_restore_default_colors_button(frm) {
		frm.add_custom_button(__("Restore Default Colors"), () => {
			frappe.confirm(
				__("Replace every desk color with the preset palette? Login page colors are left as they are."),
				async () => {
					const colors = await frappe.xcall(
						"promantia_theme.custom_theme.get_preset_theme_colors"
					);
					await frm.set_value(colors);
					frappe.show_alert({
						message: __("Default colors restored. Save to keep them."),
						indicator: "blue",
					});
				}
			);
		});
	},
});
