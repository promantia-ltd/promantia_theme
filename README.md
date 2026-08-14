# Promantia Theme

Desk themes for Frappe v15. Adds four themes to the desk's **Switch Theme** dialog alongside the
stock Frappe Light / Timeless Night / Automatic:

| Theme | Slug | Description |
| --- | --- | --- |
| Tekton Blue | `tekton-blue` | The deep blue desk theme carried over from the `Tekton-Theme` app, kept unchanged so sites moving off it keep their default look. |
| Horizon Calm | `horizon-calm` | Light theme built from the `Horizontal_Main` "Calm Premium" design kit — soft surfaces, hairline borders, layered shadows and one muted indigo accent. |
| Magenta Aurora | `magenta-aurora` | Vivid fuchsia brand theme — a plum-to-magenta gradient navbar with a white pill search field, a magenta page title, and solid-magenta active/selected fills on a near-white lavender ground. |
| Paper Ledger | `paper-ledger` | Stationery-toned theme — powder-blue chrome, cream data-entry surfaces with inputs ruled like ledger paper, ink-black primary actions, pale blue sidebar pills that turn teal when active, and workspace widgets tinted inside a white card. |

## Install

```bash
cd frappe-bench
bench get-app promantia_theme /path/to/promantia_theme   # or: bench get-app <git-url>
bench --site <site> install-app promantia_theme
bench build --app promantia_theme
```

`install-app` runs `after_install`, which widens the `User.desk_theme` select so the extra themes are
valid values. `bench migrate` re-applies it via `after_migrate`.

## Switching theme

- **Desk** — avatar menu → *Toggle Theme* (or `Ctrl/Cmd + Shift + G`), pick a theme.
- **Per user** — User form → *Desk Theme*, set `Tekton-blue`, `Horizon-calm`, `Magenta-aurora` or `Paper-ledger`.

The desk stores `desk_theme` in title case (`Tekton-blue`) and `frappe/www/app.html` renders it
lowercased as `data-theme`, which is what the stylesheets are scoped to.

## Architecture

- **`theme_registry.py`** is the only list of themes. `boot.py` publishes it to the desk via
  `extend_bootinfo`, the `ThemeSwitcher` subclass renders it, and the overridden `switch_theme`
  validates against it — so the three cannot drift apart.
- **`public/scss/_theme_tokens.scss`** holds the shared design-token layer. A light theme declares
  the `--theme-*` contract (surfaces, hairlines, text ramp, accent, semantics, neutral ramp,
  shadows, radii, chrome) and calls `@include desk_theme_tokens` to map it onto the ~130 CSS
  variables Frappe's desk actually reads, plus `@include desk_theme_widget_tokens` for charts,
  heatmaps, ratings, skeletons and indicator dots. Only values differ between themes.
- Each theme partial then adds its own *treatment* block — the component styling that gives it its
  character (Horizon Calm's blurred navbar and hover-lift cards; Magenta Aurora's gradient navbar
  and solid-magenta active pills).
- Tekton Blue predates this layer and maps Frappe's variables directly, preserved verbatim.

## Adding a theme

1. Add a `[data-theme="<slug>"]` partial under `promantia_theme/public/scss/themes/`, declare the
   `--theme-*` tokens, `@include desk_theme_tokens`, then add any treatment rules. `@import` it
   from `promantia_theme.bundle.scss`.
2. Add the slug/label/info to `APP_DESK_THEMES` in `promantia_theme/theme_registry.py`.
3. `bench --site <site> migrate && bench build --app promantia_theme`.

## Uninstall

`bench --site <site> uninstall-app promantia_theme` runs `before_uninstall`, which moves any user on a
theme from this app back to `Light` and removes the `User.desk_theme` property setter.

## Credits

- Tekton Blue is derived from [Tekton-Theme](https://github.com/vineyrawat/Tekton-Theme) (MIT).
- Horizon Calm's tokens and visual treatment come from the `Horizontal_Main` design kit.

## License

MIT
