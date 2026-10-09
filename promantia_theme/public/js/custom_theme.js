frappe.provide("promantia_theme");

// Applies the Promantia Custom Theme, whose values live in a doctype instead of a stylesheet.
//
// Everything written here is scoped to [data-theme="promantia-custom"] or removed outright the
// moment another theme is picked, so the other four themes in this app never inherit a value that
// was configured for this one. public/scss/themes/_promantia_custom.scss reads these variables and
// falls back to frappe's own for any field left blank.

// --- Constants ---
const THEME_SLUG = "promantia-custom";
const STYLE_ELEMENT_ID = "promantia-custom-theme";

// doctype fieldname -> the custom property the scss partial reads
const CUSTOM_PROPERTY_BY_FIELD = {
	navbar_background_color: "--ptc-navbar-bg",
	navbar_text_color: "--ptc-navbar-color",
	primary_button_background_color: "--ptc-btn-primary-bg",
	primary_button_text_color: "--ptc-btn-primary-color",
	primary_button_hover_background_color: "--ptc-btn-primary-hover-bg",
	primary_button_hover_text_color: "--ptc-btn-primary-hover-color",
	secondary_button_background_color: "--ptc-btn-secondary-bg",
	secondary_button_text_color: "--ptc-btn-secondary-color",
	secondary_button_hover_background_color: "--ptc-btn-secondary-hover-bg",
	secondary_button_hover_text_color: "--ptc-btn-secondary-hover-color",
	body_background_color: "--ptc-body-bg",
	content_background_color: "--ptc-content-bg",
	content_text_color: "--ptc-content-color",
	sidebar_background_color: "--ptc-sidebar-bg",
	sidebar_text_color: "--ptc-sidebar-color",
	input_background_color: "--ptc-input-bg",
	input_border_color: "--ptc-input-border",
	input_text_color: "--ptc-input-color",
	input_label_color: "--ptc-input-label-color",
	table_head_background_color: "--ptc-table-head-bg",
	table_head_text_color: "--ptc-table-head-color",
	table_body_background_color: "--ptc-table-body-bg",
	table_body_text_color: "--ptc-table-body-color",
	number_card_background_color: "--ptc-card-bg",
	number_card_border_color: "--ptc-card-border",
	number_card_text_color: "--ptc-card-color",
	footer_background_color: "--ptc-footer-bg",
	footer_text_color: "--ptc-footer-color",
};

// doctype fieldname -> the class on <html> the scss partial keys its hide rules off
const HTML_CLASS_BY_FIELD = {
	hide_help: "promantia-hide-help",
	hide_app_switcher: "promantia-hide-app-switcher",
	sticky_footer: "promantia-has-sticky-footer",
};

// a configured color is written verbatim into a stylesheet, so it has to look like a color
const COLOR_PATTERN = /^#(?:[0-9a-f]{3,4}|[0-9a-f]{6}|[0-9a-f]{8})$/i;

promantia_theme.CustomTheme = class PromantiaCustomTheme {
	constructor() {
		this.config = null;
		this.watch_selected_theme();
		this.sync();
	}

	// --- Lifecycle ---
	async sync() {
		if (!this.is_selected()) {
			this.teardown();
			return;
		}

		if (!this.config) {
			this.config = await this.fetch_config();
		}

		if (this.config) {
			this.apply();
		}
	}

	async refresh() {
		this.config = null;
		await this.sync();
	}

	apply() {
		this.write_custom_properties();
		this.toggle_html_classes();
		this.render_footer();
		this.point_logo_at_default_app();
	}

	teardown() {
		document.getElementById(STYLE_ELEMENT_ID)?.remove();
		Object.values(HTML_CLASS_BY_FIELD).forEach((name) =>
			document.documentElement.classList.remove(name)
		);
		this.footer_mount()?.replaceChildren();
		this.restore_logo_link();
	}

	// --- Helpers ---
	is_selected() {
		return document.documentElement.getAttribute("data-theme") === THEME_SLUG;
	}

	// data-theme is the attribute frappe.ui.set_theme writes, whichever path changed the theme
	watch_selected_theme() {
		new MutationObserver(() => this.sync()).observe(document.documentElement, {
			attributes: true,
			attributeFilter: ["data-theme"],
		});
	}

	async fetch_config() {
		try {
			return await frappe.xcall("promantia_theme.custom_theme.get_desk_custom_theme");
		} catch (error) {
			// a theme is not worth breaking the desk over - frappe's defaults stay in place
			return null;
		}
	}

	// --- Apply Helpers ---
	write_custom_properties() {
		const declarations = Object.entries(CUSTOM_PROPERTY_BY_FIELD)
			.filter(([field]) => COLOR_PATTERN.test(this.config[field]))
			.map(([field, property]) => `${property}: ${this.config[field]};`);

		const style = this.style_element();
		style.textContent = declarations.length
			? `[data-theme="${THEME_SLUG}"] { ${declarations.join(" ")} }`
			: "";
	}

	style_element() {
		let style = document.getElementById(STYLE_ELEMENT_ID);
		if (!style) {
			style = document.createElement("style");
			style.id = STYLE_ELEMENT_ID;
			document.head.appendChild(style);
		}

		return style;
	}

	toggle_html_classes() {
		Object.entries(HTML_CLASS_BY_FIELD).forEach(([field, name]) => {
			document.documentElement.classList.toggle(name, Boolean(this.config[field]));
		});
	}

	// the desk shell ships an empty <footer>, which survives every route change
	render_footer() {
		const mount = this.footer_mount();
		if (!mount) {
			return;
		}

		if (!this.config.footer_html) {
			mount.replaceChildren();
			return;
		}

		mount.innerHTML = this.config.footer_html;
	}

	footer_mount() {
		return document.querySelector(".main-section > footer");
	}

	// with the app switcher hidden the desk logo is the only way left to reach the chosen app
	point_logo_at_default_app() {
		const logo = this.navbar_logo_link();
		const route = this.default_app_route();
		if (!logo || !route) {
			return;
		}

		logo.dataset.promantiaDefaultHref ??= logo.getAttribute("href");
		logo.setAttribute("href", route);
	}

	default_app_route() {
		if (!this.config.hide_app_switcher || !this.config.default_app) {
			return "";
		}

		const apps = frappe.boot.apps_data?.apps || [];
		return apps.find((app) => app.name === this.config.default_app)?.route || "";
	}

	restore_logo_link() {
		const logo = this.navbar_logo_link();
		if (!logo?.dataset.promantiaDefaultHref) {
			return;
		}

		logo.setAttribute("href", logo.dataset.promantiaDefaultHref);
		delete logo.dataset.promantiaDefaultHref;
	}

	navbar_logo_link() {
		return document.querySelector(".navbar .navbar-brand.navbar-home");
	}
};

// app_ready is the first point at which both the navbar and the desk shell footer exist
$(document).on("app_ready", () => {
	promantia_theme.custom_theme = new promantia_theme.CustomTheme();
});
