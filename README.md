# Horizon Theme

Desk themes for Frappe v15. Adds two themes to the desk's **Switch Theme** dialog alongside the
stock Frappe Light / Timeless Night / Automatic:

| Theme | Slug | Description |
| --- | --- | --- |
| Tekton Blue | `tekton-blue` | The deep blue desk theme carried over from the `Tekton-Theme` app, kept unchanged so sites moving off it keep their default look. |
| Horizon Calm | `horizon-calm` | Light theme built from the `Horizontal_Main` "Calm Premium" design kit — soft surfaces, hairline borders, layered shadows and one muted indigo accent. |

## Install

```bash
cd frappe-bench
bench get-app horizon_theme /path/to/horizon_theme   # or: bench get-app <git-url>
bench --site <site> install-app horizon_theme
bench build --app horizon_theme
```

`install-app` runs `after_install`, which widens the `User.desk_theme` select so the extra themes are
valid values. `bench migrate` re-applies it via `after_migrate`.

## Switching theme

- **Desk** — avatar menu → *Toggle Theme* (or `Ctrl/Cmd + Shift + G`), pick a theme.
- **Per user** — User form → *Desk Theme*, set `Tekton-blue` or `Horizon-calm`.

The desk stores `desk_theme` in title case (`Tekton-blue`) and `frappe/www/app.html` renders it
lowercased as `data-theme`, which is what the stylesheets are scoped to.

## Adding a theme

1. Add a `[data-theme="<slug>"]` partial under `horizon_theme/public/scss/themes/` and `@import` it
   from `horizon_theme.bundle.scss`.
2. Add the slug/label/info to `APP_DESK_THEMES` in `horizon_theme/theme_registry.py`.
3. `bench --site <site> migrate && bench build --app horizon_theme`.

The registry is the only list — the theme switcher reads it from boot info and `switch_theme`
validates against it, so the two cannot drift apart.

## Uninstall

`bench --site <site> uninstall-app horizon_theme` runs `before_uninstall`, which moves any user on a
theme from this app back to `Light` and removes the `User.desk_theme` property setter.

## Credits

- Tekton Blue is derived from [Tekton-Theme](https://github.com/vineyrawat/Tekton-Theme) (MIT).
- Horizon Calm's tokens and visual treatment come from the `Horizontal_Main` design kit.

## License

MIT
