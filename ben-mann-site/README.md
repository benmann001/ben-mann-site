# Ben Mann — Personal Landing Page

A single-page, vanilla HTML/CSS/JS landing site for Ben Mann.

## Files

- `index.html` — markup, content, semantic structure
- `styles.css` — all styling, design tokens, responsive layout
- `script.js` — sticky-nav state, scroll reveals, form validation, footer build stamp
- `README.md` — this file

No build step. Open `index.html` in a browser, or serve the folder with any static server (e.g. `python3 -m http.server` or `npx serve`).

---

## Design choices

**Dark, forward, operator-confident.** The page commits to a dark midnight surface with a single electric chartreuse accent. The intent is for a visitor to read three signals within seconds: *modern* (dark UI, mono labels, subtle grid backdrop), *trustworthy* (restrained motion, generous space, real specifics in copy), and *future-facing* (AI-agent capability called out distinctly, status-style indicators, system metadata in the footer).

**Differentiated from adjacent work.** The earlier draft of this page borrowed too heavily from the Richard Beddie site (warm bone + terracotta + Fraunces). This rebuild deliberately moves to a fundamentally different palette and type system so Ben's own portfolio stands apart from work he's done for clients.

**Operator over consultant.** Copy is written in first person and threads the same idea throughout — *"I run what I build. I build what I recommend."* Specific roles (founder, COO, CIO) are named on-page rather than implied. The 30-minute call is positioned as the offer, not a sales process.

**AI agents called out distinctly.** Capabilities 01–04 sit as equal-weight tiles; AI Agents (S/05) gets a wider featured tile with a soft glow and a small "where I'm spending the most time right now" tag. This signals current focus without elevating it above the four other disciplines in the section hierarchy.

**Sector depth as the unfair advantage.** A full section frames fitness, health, wellness, and membership as the deep specialism while explicitly inviting work outside it.

---

## Type

| Role          | Family                       | Notes                                                   |
|---------------|------------------------------|---------------------------------------------------------|
| Display + UI  | **Space Grotesk** (400–700)  | Geometric sans with enough character to feel designed, not generic. Negative tracking on display. |
| System / labels | **JetBrains Mono** (400–500) | Used for kickers, status pills, capability numbers, footer metadata. Adds the engineering/AI flavour without coldness. |

Both fonts loaded from Google Fonts with `display=swap`. To swap to system stacks, change the `--sans` and `--mono` variables in `:root`.

---

## Colour palette

| Token             | Value                       | Use                                       |
|-------------------|-----------------------------|-------------------------------------------|
| `--bg`            | `#0A0E17`                   | Midnight — page background                |
| `--bg-elev`       | `#11161F`                   | Slightly elevated band (sector, footer, trusted, testimonial) |
| `--bg-card`       | `#141A24`                   | Card surfaces (capabilities, work, form)  |
| `--bg-input`      | `#0E141D`                   | Form inputs                               |
| `--ink`           | `#F2F4F8`                   | Warm white — primary text                 |
| `--ink-soft`      | `#B0B7C4`                   | Slate — body copy                         |
| `--ink-mute`      | `#6F7787`                   | Muted slate — meta / labels               |
| `--accent`        | `#CDF44A`                   | Electric chartreuse — single accent       |
| `--accent-deep`   | `#9FBE2C`                   | Hover variant of accent                   |
| `--accent-glow`   | `rgba(205,244,74,.28)`      | Glow halos on buttons, hero, form         |
| `--rule`          | `rgba(242,244,248,.08)`     | Hairline rules                            |
| `--rule-strong`   | `rgba(242,244,248,.18)`     | Stronger rules / chip borders             |

The chartreuse does all the colour work. To re-skin (e.g. icy cyan, electric violet), change `--accent`, `--accent-deep`, and `--accent-glow` together — every accent on the page derives from those three.

**Accessibility:** chartreuse on midnight tests at ~14:1 contrast — comfortable AAA. Body copy uses `--ink-soft` on `--bg` (~12:1, AAA). The accent is never used for small body text on light surfaces.

---

## Visual flourishes (used sparingly)

- **Grid backdrop** on hero, mid-CTA, and case-study media — a faint 60–80px grid masked into a soft ellipse so it adds depth without taking attention.
- **Status pill** in the hero — pulsing accent dot + monospace label, signalling availability.
- **Featured capability glow** on AI Agents tile — soft radial highlight + accent top border.
- **Glow on primary buttons hover** — soft chartreuse halo, never a hard glow.
- **Mono labels** prefixed with `// ` or `S/0X` — gentle terminal/system flavour.
- **Footer build stamp** — `SYS / v1.0 · last shipped {month} {year}`, populated by JS.

All motion respects `prefers-reduced-motion`. The base body has a fixed dot-grid texture which loads once and doesn't animate.

---

## Swapping in real content

### Photo of Ben (About section)
Replace the `.about__photoBox` `<div>` in `index.html` with an `<img>`:

```html
<img src="ben-portrait.jpg"
     alt="Portrait of Ben Mann, smiling, outdoors"
     class="about__photoBox"
     width="800" height="1000" />
```

Recommended ratio **4:5**, 800×1000 or larger. The CSS already gives the box rounded corners and a border — an `<img>` with `class="about__photoBox"` will inherit the same shape.

### Case-study visuals (Selected work)
Each `.case__media` currently contains a placeholder mark + a small badge (`<span class="case__placeholder">MP</span>` + `<span class="case__badge">// founder</span>`). Replace the placeholder with a screenshot — keep the badge for the role tag:

```html
<div class="case__media">
  <img src="memberpro-thumb.jpg"
       alt="MemberPRO landing page screenshot"
       loading="lazy" />
  <span class="case__badge">// founder</span>
</div>
```

The `.case__media` is `aspect-ratio: 16 / 9`. Use images at that ratio (e.g. 1280×720) for best results.

### Trusted-by row
Currently typographic chips. To use real logos, replace the `<li>` items with `<img>` tags and add a small style block (white/lime SVG marks work best on the dark band).

### Testimonials
The single quote is wrapped in `<figure class="quote">` inside `.testimonial`. Duplicate the block to add more — the CSS centres the section and will accommodate stacked quotes; for a row layout on desktop, wrap them in a flex/grid container.

### SEO + social
Update `<title>`, `<meta name="description">`, and the `og:*` tags at the top of `index.html`. Add an `og-image.jpg` (1200×630) at the project root.

---

## Form

The contact form in `#contact` is a fully working front-end: validation, focus management, success/error states, accessible status messaging via `aria-live`. The submit currently **simulates** a network request and shows a thank-you message — no data is sent anywhere.

To wire to a real backend, edit `script.js` and replace the simulated `setTimeout` block. Low-friction options:

- **Formspree** / **Basin** — change the form's `action` to your endpoint and remove the JS simulation.
- **Custom endpoint** — replace the `setTimeout` with a `fetch('/api/enquiry', { method: 'POST', body: fd })`. The success/error pattern is already in place.

Email link in the footer + form fineprint currently points to `hello@benmann.co.nz` — swap to the real address.

---

## Accessibility

- Semantic landmarks (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`)
- Skip-link for keyboard users
- Heading hierarchy: one `<h1>`, then `<h2>` per section
- All interactive elements keyboard-reachable with visible `:focus-visible` rings
- Form inputs have associated `<label>`s and `aria-invalid` on errors
- `aria-live="polite"` status region for form feedback
- `prefers-reduced-motion` respected — animations and smooth scroll disabled
- Colour contrast tested AA/AAA on all functional text
- The chartreuse accent is used for accent text only on dark backgrounds, never for small body text on light surfaces

---

## Performance

- No frameworks, no build step, no runtime dependencies
- Two Google Font families with `display=swap` (variable Space Grotesk + JetBrains Mono)
- Inline SVG favicon (data URI) — no extra request
- Background grid is pure CSS — no images
- Scroll reveals via IntersectionObserver (gracefully no-ops if unsupported)
- Total weight: tens of KB before fonts

---

## Quick QA checklist before launch

- [ ] Replace photo of Ben in About
- [ ] Replace case-study placeholders with screenshots or real brand marks
- [ ] Update email address in footer + form fineprint
- [ ] Wire form submit to real endpoint
- [ ] Add `og-image.jpg` (1200×630) for social sharing
- [ ] Add real testimonials beyond the Richard Beddie one
- [ ] Update `<title>` and `<meta description>` if copy shifts
- [ ] Run Lighthouse — target 95+ across the board
