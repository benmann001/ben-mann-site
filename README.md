# Ben Mann — Personal Landing Page · v2 (elevated)

A single-page, vanilla HTML/CSS/JS landing site for Ben Mann.

## Files

```
ben-mann-site-v2/
  index.html
  styles.css
  script.js
  README.md
  assets/                ← drop your logos + portrait here
```

No build step. Open `index.html` in a browser, or serve the folder with any static server (`python3 -m http.server` or `npx serve`).

---

## Direction

**Neo-editorial.** A warm ivory paper, deep cobalt accent, italic serif used as the recurring brand voice, magazine-style numbering in the margins, asymmetric work grid, and a paper-grain overlay across everything. Light theme but a deliberately different temperature and mood from anything in the wider portfolio.

**Three signals the page is built to deliver in the first three seconds:**
1. *Operator* — italic serif treatment of the word recurs across every section, framing Ben as the thesis.
2. *Trust* — refined typography, generous space, real specifics in copy (REPs Registrar, COO, CIO).
3. *Future* — cobalt + cursor blink + AI Agents tile in inverted dark + live system metadata.

---

## Type

| Role          | Family                       | Notes                                                   |
|---------------|------------------------------|---------------------------------------------------------|
| Display       | **Instrument Serif** (regular + italic) | High-contrast editorial serif. Italic does the brand voice — it appears everywhere a key word needs weight. |
| Body / UI     | **Instrument Sans** (variable 400–700, italic) | Companion modernist sans by the same designer. |
| System / labels | **DM Mono** (300–500)      | Used for kickers, capability numbers, system metadata, footer clock. |

All loaded from Google Fonts with `display=swap`. To swap to system stacks, change `--serif`, `--sans`, `--mono` in `:root`.

---

## Colour palette

| Token             | Value      | Use                                       |
|-------------------|------------|-------------------------------------------|
| `--paper`         | `#EFE9DD`  | Warm ivory — page background              |
| `--paper-deep`    | `#E5DECF`  | Deeper cream for bands (tape, sector, footer, testimonial) |
| `--paper-card`    | `#F5F0E5`  | Card surfaces                             |
| `--ink`           | `#16140F`  | Warm near-black — primary text + buttons  |
| `--ink-soft`      | `#44403A`  | Body copy                                 |
| `--ink-mute`      | `#7E776C`  | Meta / labels / muted                     |
| `--accent`        | `#1834D6`  | Deep electric cobalt — single accent      |
| `--accent-deep`   | `#0F22A5`  | Hover variant                             |
| `--accent-glow`   | `rgba(24,52,214,.18)` | Halos on form, status pill, footer dot |
| `--ember`         | `#C8412B`  | Form-error red — sparing                  |
| `--rule`          | `rgba(22,20,15,.14)` | Hairline rules                  |
| `--rule-strong`   | `rgba(22,20,15,.28)` | Stronger rules / chip borders   |

Cobalt does all the colour work. Italic serif does all the *voice* work. Every `<em>` on the page automatically gets the italic-serif-cobalt treatment via a global rule.

---

## What's in the design

- **Italic serif as accent device** — `<em>` is wired globally to render in Instrument Serif italic + cobalt, so any keyword you wrap in `<em>` becomes a brand moment.
- **Hero** — left-aligned, max headline width 17ch, "Portfolio · Vol. 01 · 2026" rotated vertically along the right edge (hidden on tablet/mobile), terminal cursor blink at the end of the third line.
- **Tape / marquee** — affiliations + clients scroll horizontally, pause on hover, edges feathered with a soft mask.
- **Capabilities** — 4 tiles in a 2×2 grid; AI Agents below as a wide *dark* inverted tile with a slow shimmer sweep, signalling current focus.
- **Sector** — copy left, sticky pill cloud right, top edge marked with a soft cobalt gradient line.
- **Mid-CTA** — full-bleed dark band with a cobalt radial glow and an oversized italic line.
- **Selected work** — split into two labelled sub-sections: *Founded & co-founded* (FitWeb, ASA) and *Clients & institutional roles* (ExerciseNZ, REPs).
- **About** — sticky portrait box on the left with a CSS duotone treatment (cobalt + cream) applied to the portrait via SVG filter.
- **Testimonial** — oversized italic quote-mark behind the body text, treated like an editorial pull quote.
- **Form** — paper-card surface, italic serif placeholders, dashed-rule head with a `[•] new enquiry — form/01` system label.
- **Footer** — live NZT clock, `SYS · online · NZT 14:23`, updates every 30s.
- **Paper grain** — fixed SVG noise overlay across the whole page, multiplied at 18% opacity for an editorial print feel.

Motion respects `prefers-reduced-motion` everywhere.

---

## Drop your assets here

Put files into the `assets/` folder using these exact names — the markup already references them:

| Where       | Path                          | Format           | Notes                                       |
|-------------|-------------------------------|------------------|---------------------------------------------|
| About photo | `assets/ben-portrait.jpg`     | JPG or PNG       | Any clear portrait. 4:5 ratio works best (e.g. 800×1000). The site applies a **cobalt + cream duotone** automatically via an SVG filter — no Photoshop needed. |
| FitWeb logo | `assets/logo-fitweb.svg`      | SVG (preferred) or PNG with transparent background | Used in the FitWeb work card. |
| ASA logo    | `assets/logo-asa.svg`         | SVG/PNG          | Affinity Supply Alliance card.              |
| ExerciseNZ logo | `assets/logo-exercise-nz.svg` | SVG/PNG    | ExerciseNZ card.                            |
| REPs logo   | `assets/logo-reps.svg`        | SVG/PNG          | NZ Register of Exercise Professionals card. |
| Social card | `og-image.jpg`                | 1200×630 JPG     | For link previews on LinkedIn, Slack, etc.  |

Once a logo file lives at the path above, replace the `<span class="case__placeholder">FW</span>` inside the matching `.case__media` block with:

```html
<img src="assets/logo-fitweb.svg" alt="FitWeb logo" loading="lazy" />
```

The `.case__media` CSS already handles sizing (`max-width: 60%; max-height: 60%; object-fit: contain;`) so logos sit centered with breathing room.

### About the duotone

The portrait gets tinted **cobalt (#1834D6) + cream (#EFE9DD)** automatically — dark areas of the photo become cobalt, light areas become cream. This is done via an inline SVG `<filter id="duotone-cobalt">` at the top of `index.html`, applied with `filter: url(#duotone-cobalt)` in CSS.

If you'd prefer:
- **No duotone** — remove `filter: url(#duotone-cobalt);` from `.about__portrait` in `styles.css`.
- **Different tint** — edit the matrix values in the SVG filter (last column of the first three rows is the target RGB). For an ember-orange duotone for example, use `0.78 / 0.25 / 0.17` instead of `0.094 / 0.207 / 0.835`.

---

## Form

The contact form has working front-end validation, focus management, success/error states, accessible status messaging via `aria-live`, and **simulates** a successful submit. To wire up a real backend, edit the `setTimeout` block in `script.js`:

```js
fetch('/api/enquiry', { method: 'POST', body: fd })
  .then(/* … */)
```

Or change the form's `action` attribute to a Formspree / Basin endpoint and remove the JS simulation.

Email link in the footer + form fineprint currently points to `hello@benmann.co.nz`.

---

## Accessibility

- Semantic landmarks (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`)
- Skip link for keyboard users
- Heading hierarchy: one `<h1>`, then `<h2>` per section
- All interactive elements keyboard-reachable with visible `:focus-visible` rings
- Form inputs have associated `<label>`s and `aria-invalid` on errors
- `aria-live="polite"` form status region
- `prefers-reduced-motion` respected — animations disabled
- Body copy passes WCAG AA on the warm-paper background; cobalt accent is used on light surfaces only at large display sizes (logo, kickers, headings, italic accents)

---

## Performance

- No frameworks, no build step, no runtime dependencies
- Three font families, all from Google Fonts with `display=swap`
- Inline SVG favicon (data URI) — no extra request
- Paper grain is a tiny inline SVG noise pattern
- Background grid in case media is pure CSS
- Scroll reveals via IntersectionObserver

---

## Quick QA before launch

- [ ] Drop `ben-portrait.jpg` into `assets/`
- [ ] Drop the four logos into `assets/`
- [ ] Update email address in footer + form fineprint if `hello@benmann.co.nz` isn't right
- [ ] Wire form submit to a real endpoint
- [ ] Add `og-image.jpg` (1200×630) for social previews
- [ ] Add real testimonials beyond the Richard Beddie one
- [ ] Run Lighthouse — aim for 95+ across the board
