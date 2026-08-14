# Promantia Theme

Desk themes for Frappe v15. Adds five themes to the desk's **Switch Theme** dialog alongside the
stock Frappe Light / Timeless Night / Automatic — four fixed stylesheets and one a System Manager
configures from a doctype:

| Theme | Slug | Description |
| --- | --- | --- |
| Tekton Blue | `tekton-blue` | The deep blue desk theme carried over from the `Tekton-Theme` app, kept unchanged so sites moving off it keep their default look. |
| Horizon Calm | `horizon-calm` | Light theme built from the `Horizontal_Main` "Calm Premium" design kit — soft surfaces, hairline borders, layered shadows and one muted indigo accent. |
| Magenta Aurora | `magenta-aurora` | Vivid fuchsia brand theme — a plum-to-magenta gradient navbar with a white pill search field, a magenta page title, and solid-magenta active/selected fills on a near-white lavender ground. |
| Paper Ledger | `paper-ledger` | Stationery-toned theme — powder-blue chrome, cream data-entry surfaces with inputs ruled like ledger paper, ink-black primary actions, pale blue sidebar pills that turn teal when active, and workspace widgets tinted inside a white card. |
| Promantia Custom Theme | `promantia-custom` | Not a fixed palette — the colors come from the **Promantia Custom Theme** doctype, so a System Manager sets them per site without touching SCSS. Anything left blank keeps Frappe Light's default. See [Promantia Custom Theme](#promantia-custom-theme). |

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
- **Per user** — User form → *Desk Theme*, set `Tekton-blue`, `Horizon-calm`, `Magenta-aurora`,
  `Paper-ledger` or `Promantia-custom`.

The desk stores `desk_theme` in title case (`Tekton-blue`) and `frappe/www/app.html` renders it
lowercased as `data-theme`, which is what the stylesheets are scoped to.

## Architecture

- **`theme_registry.py`** is the only list of themes. `boot.py` publishes it to the desk via
  `extend_bootinfo`, the `ThemeSwitcher` subclass renders it, and the overridden `switch_theme`
  validates against it — so the three cannot drift apart. `install.py` reads the same list, which
  is why adding a theme there is all it takes for `User.desk_theme` to accept it after `migrate`
  and for `before_uninstall` to move users off it again.
- **`public/scss/_theme_tokens.scss`** holds the shared design-token layer. A light theme declares
  the `--theme-*` contract (surfaces, hairlines, text ramp, accent, semantics, neutral ramp,
  shadows, radii, chrome) and calls `@include desk_theme_tokens` to map it onto the ~130 CSS
  variables Frappe's desk actually reads, plus `@include desk_theme_widget_tokens` for charts,
  heatmaps, ratings, skeletons and indicator dots. Only values differ between themes.
- Each theme partial then adds its own *treatment* block — the component styling that gives it its
  character (Horizon Calm's blurred navbar and hover-lift cards; Magenta Aurora's gradient navbar
  and solid-magenta active pills).
- Tekton Blue predates this layer and maps Frappe's variables directly, preserved verbatim.
- Promantia Custom Theme sits outside the token layer on purpose: its values arrive at runtime, so
  it overrides individual elements with `var(--ptc-*, <frappe's own variable>)` instead of
  redefining the token contract. `custom_theme.py` serves the configuration and renders the login
  `<style>`; `public/js/custom_theme.js` applies and tears it down on the desk.

## Promantia Custom Theme

The one theme whose values are configuration rather than code. **The configuration is site-wide —
one Single doctype for the whole site — but activation is per user**, through each user's own theme
selection. Configuring it changes nothing for anyone until they pick it.

### Configuring it

1. Open **Promantia Custom Theme** (`/app/promantia-custom-theme`). System Manager only.
2. Set the colors and switches you want, and **Save**. Every field is optional: leave one blank and
   Frappe's own default for that element stays in place.
3. Pick **Promantia Custom Theme** from *Toggle Theme* (avatar menu, or `Ctrl/Cmd + Shift + G`).

A reload picks up saved changes; **Apply Theme** on the form re-reads them without one.

### What is configurable

| Tab | Fields |
| --- | --- |
| Navbar | background / text color, hide Help, hide app switcher, default app |
| Buttons | primary and secondary — background, text, hover background, hover text |
| Desk | page and content-area background, content text, sidebar, inputs (background, border, text, label), list/table head and body, number cards |
| Login Page | page background color or image, login box background and position, heading color, login button colors |
| Footer | copyright text, powered-by text, background and text color, sticky |

### How it stays out of the other themes' way

Colors are written as `--ptc-*` custom properties into a single `<style>` element scoped to
`[data-theme="promantia-custom"]`, and the switches as classes on `<html>`. Selecting any other
theme removes the style element, the classes and the footer outright — so nothing configured here
can leak into Tekton Blue, Paper Ledger, Light or Dark. `public/scss/themes/_promantia_custom.scss`
reads those properties with Frappe's own variable as the fallback for each one, which is what makes
a blank field a genuine no-op rather than an empty value.

### Login page and default app — the two version-dependent bits

- **Login page.** The desk bundle does not load on `/login`, so the login appearance is rendered
  server-side instead: the `update_website_context` hook appends a scoped `<style>` to the login
  route's `<head>`. No asset or fetch is added to any other portal page, and only plain hex colors
  and site-relative image paths are emitted. Because the login page is public it is genuinely
  site-wide: it applies to everyone signing in, not only to users who selected this theme.
- **Default App.** *Hide App Switcher* hides the **Apps** entry in the navbar settings dropdown,
  which is what the app switcher is on Frappe v15. *Default App* is validated (required, and must
  be installed) and repoints the desk logo at that app, so the app stays reachable with the
  switcher hidden. This app deliberately does **not** write System Settings → *Default App*; set
  that separately if you also want the post-login landing route changed.

## Adding a theme

1. Add a `[data-theme="<slug>"]` partial under `promantia_theme/public/scss/themes/`, declare the
   `--theme-*` tokens, `@include desk_theme_tokens`, then add any treatment rules. `@import` it
   from `promantia_theme.bundle.scss`.
2. Add the slug/label/info to `APP_DESK_THEMES` in `promantia_theme/theme_registry.py` — that one
   entry is what makes it show up in *Toggle Theme*, become a valid `User.desk_theme` on the next
   `migrate`, and get cleaned up on uninstall.
3. `bench --site <site> migrate && bench build --app promantia_theme`.

To add a *configurable* field to Promantia Custom Theme instead: add the field to the doctype, then
its fieldname to `DESK_THEME_FIELDS` and `CUSTOM_PROPERTY_BY_FIELD` (colors) or `HTML_CLASS_BY_FIELD`
(switches), and consume the new `--ptc-*` property in `_promantia_custom.scss` with Frappe's own
variable as the fallback.

## Uninstall

`bench --site <site> uninstall-app promantia_theme` runs `before_uninstall`, which moves any user on a
theme from this app — Promantia Custom Theme included — back to `Light` and removes the
`User.desk_theme` property setter. The Promantia Custom Theme doctype and its stored values go with
the app, and nothing outside this app was ever written, so no global setting needs unwinding.

## Credits

- Tekton Blue is derived from [Tekton-Theme](https://github.com/vineyrawat/Tekton-Theme) (MIT).
- Horizon Calm's tokens and visual treatment come from the `Horizontal_Main` design kit.
- Promantia Custom Theme's field groups follow the configuration model of
  [frappe_desk_theme](https://github.com/dhwaniris/frappe_desk_theme) (MIT), reimplemented here —
  this app does not depend on it or import from it.

## License

MIT
