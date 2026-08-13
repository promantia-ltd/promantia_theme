from horizon_theme.theme_registry import get_desk_themes

# --- Boot Hooks ---


def extend_bootinfo(bootinfo):
	"""Publishes the theme registry to the desk so the theme switcher renders it without a second list."""
	bootinfo.horizon_desk_themes = get_desk_themes()
