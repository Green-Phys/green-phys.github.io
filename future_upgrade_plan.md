# Future Upgrade Plan for green-phys.org

Both `green-phys.github.io` and `alpsim.github.io` are Hugo sites built on the
[hextra](https://github.com/imfing/hextra) theme, and until recently they were
close siblings in structure and features. Over the past ~6 weeks
(2026-05-21 → 2026-07-06, PRs #43-#103) the ALPS site went through a large,
deliberate revamp. This document inventories what changed there and proposes
an equivalent punch list for GREEN, roughly in priority order.

Source of comparison: local `green-phys.github.io` repo vs. a fresh clone of
`https://github.com/ALPSim/alpsim.github.io` (main, as of 2026-07-07).

## Where the two sites stand today

| Aspect | green-phys (now) | alpsim (now) |
|---|---|---|
| hextra theme version | `v0.7.3` (go.mod) | `v0.12.3` |
| Top nav | About, Search, GitHub, Discord, Toggle | Installation, Getting Started, Tutorials, Documentation, About, Governance, Events, FAQs, Search, GitHub, Discord, YouTube, Toggle, Language |
| Languages | English only | English, 中文 (zh-cn), 日本語 (ja), Español (es) — *out of scope, see note below* |
| Homepage | Single feature-grid of components + 3 flex buttons (`cta-buttons` class, no true grid) | Two-column intro + logo, responsive `.btn-grid` of 12 CTA buttons, dedicated Tutorials button row, Acknowledgement section with funding-agency logo |
| About page | One paragraph + licensing + acknowledgements, no nav aids | Intro, Mission, Licensing, Acknowledgements, **and** a `btn-grid` linking to Events/Governance/FAQ |
| Governance | None | `govern/_index.md`, `maintainers.md`, `contribute.md`, `onboard.md` (student onboarding) |
| FAQ | None | Dedicated FAQ page with actionable button links per answer |
| Installation | One page + subpages, some cards missing links (e.g. "Install Packaged Versions" has no `link=`) | Split into Binary / Source / Spack pages with explicit audience guidance ("most users...", "developers...", "HPC operators...") |
| Publications | Not present as own section | "Papers and Citations" page explaining 3 citation categories (algorithm / implementation / library), separate `papers.md` + `refs.md` |
| Search | Hextra default only | Auto-generated docs search index used as chatbot fallback |
| Chatbot | None | Keyword-based "ALPS Assistant" widget (explicitly labeled "not AI") with a limitations warning — *out of scope, see note below* |
| Math rendering | Custom `mathjax/inline` shortcode | Goldmark `passthrough` extension configured for native `$...$` / `$$...$$` KaTeX delimiters; had to fix a triple-backslash CI build break |
| Mobile | Not recently audited | Fixed hamburger menu breakage on iOS Safari/Chrome, fixed language-selector label disappearing |
| Tutorials content | Present, not recently audited for correctness | Multi-pass rewrite: fixed factual/code bugs, heading hierarchy, dead citations, translated everything into zh-cn/ja/es |

**Decision: multi-language support and the ALPS-style chatbot are explicitly
out of scope for GREEN** and have been dropped from the punch list below.
Kept in this table only as factual comparison points against ALPS.

## Proposed changes for green-phys.org, in priority order

### 1. Update the hextra theme — DONE
Bumped `github.com/imfing/hextra` from `v0.7.3` to `v0.12.3` (matching ALPS),
along with the min Hugo version, CI's pinned Hugo version, and all the
downstream template/CSS-prefix/JS fallout from the jump. (Mirrors ALPS PR #67,
"fix: upgrade theme to imfing/hextra v0.12.3".)

### 2. Restructure top-level navigation — PARTIALLY DONE
Added Installation, Getting Started, and Documentation to `hugo.yaml`'s
`menu.main` (pointing at the existing `/docs/installation`,
`/docs/getting-started`, `/docs` sections — no content restructuring needed),
ahead of the existing About/Search/GitHub/Discord/Toggle. Nav highlighting
and sidebar active-state both confirmed working.

Still open: Tutorials (if/when GREEN has a stand-alone tutorials section,
currently only inside `docs/tutorials`), Governance (new, see #5), FAQ (new,
see #6) — none of these have content yet, so nothing to link to. (Mirrors
ALPS PRs #70 "redesign homepage with navigation and tutorial button grids",
#78 "add Getting Started to top navbar", #84 "reorganize top nav — promote
install/start to top-level sections".)

### 3. Rebuild the homepage with a proper button grid — DONE
Added the `.btn-grid` CSS component (responsive: 3 columns → 2 → 1 on narrow
screens, ported from `alps.css`) and switched the homepage's CTA buttons to
use it instead of the old `cta-buttons` flex row. Replaced the button color
CSS (`.btn`, `.btn-primary`, `.btn-outlined-primary`), which had bit-rotted
into unstyled buttons — it depended on Tailwind v3 `--tw-bg-opacity`/
`--tw-text-opacity` custom properties that no longer exist under the new
theme's Tailwind v4 setup, and an undefined `--btn-primary-bg` variable —
with clean, self-contained HSL-based rules.

Buttons now use a dedicated `--btn-hue`/`--btn-saturation` pair (42deg/50%,
100% in dark mode — ALPS's exact values) rather than reusing GREEN's own
green `--primary-hue`, so the CTA buttons get ALPS's dark-orange accent
without recoloring the sidebar/links elsewhere on the site. Also dropped the
`prim="yes"`/`err="yes"` shortcode flags so every button renders in the same
plain outlined style ("appear equally"), matching how ALPS's own homepage
buttons are all plain/outlined with no per-button color variation.

Grid populated with 6 buttons (2 rows × 3 cols): Installation, Getting
Started, Documentation, GitHub Source, Submit an issue, Discord — pulling in
the same links now on the top navbar plus the existing GitHub/Discord.

Also replaced the persistent left-hand "sponsor-container" sidebar (a 20%-wide
`<aside>` pinning the NSF logo next to the content on every `green-home`-
layout page — homepage, About, and both News templates) with an inline
"## Acknowledgement" section near the bottom of the homepage content, and
added the matching NSF-logo-plus-award-link block to the About page's
existing Acknowledgements section too — mirroring ALPS's exact pattern,
where the same logo/link markup lives inline in both `_index.md` and
`about.md` rather than in a page-wide sidebar. Content now uses the page's
full width on all four templates; the dead `.sponsor-container` CSS was
removed.

Still open: a distinct "Documentation sections"/"Components"/Tutorials
button row beneath the main grid. (Mirrors ALPS PRs #70, #77 "lock homepage
btn-grid to 3 columns on wide screens", #65 "rewrite homepage package
description".)

### 4. Revamp the About page
Add a sidebar/nav-button block linking out to Governance/FAQ (once they
exist) and tidy the Mission/Licensing/Acknowledgements sections to match the
homepage's tone. (Mirrors ALPS PR #79 "revamp About page — sidebar, intro,
mission, and nav buttons".)

### 5. Add a Governance section
GREEN has no equivalent of ALPS's `govern/` section. Worth adding:
- `_index.md` — steering committee / decision-making overview
- `maintainers.md` — who maintains which component (GREEN already documents
  components in `docs/components/`, so this would just need an ownership
  matrix)
- `contribute.md` — how to start contributing (GREEN has `docs/contribution.md`
  already; consider whether it should move up to Governance or be linked from
  it)
- `onboard.md` — a statement for students/early-career contributors wanting
  to get involved

(Mirrors ALPS PRs #94 "Add Contributing to ALPS page and update governance
section", #97 "Add Code Maintainers page under Governance".)

### 6. Add an FAQ page — DONE (via the existing Troubleshooting page)
Rather than write a separate, largely-redundant FAQ page from scratch,
GREEN already had a `docs/troubleshoot.md` page covering the same
"how do I get unstuck" need with real content (convergence issues, build
failures) — so it got the ALPS-FAQ treatment instead of duplicating it:
- Added to the top navbar (`hugo.yaml` `menu.main`) and to the homepage
  CTA `.btn-grid`, so it's reachable in one click like ALPS's FAQ.
- Added to the docs index page's feature-card grid.
- Added ALPS-style action-button rows: an intro "need more help?"
  Issues/Discord row at the top, and a closing button row after each of
  the two major sections (DIIS Tutorial/Convergence Theory after the
  convergence section; Installation Guide/Submit an issue after the
  build section) — matching how ALPS ends every FAQ answer with
  relevant action buttons.
(Mirrors ALPS PR #85 "rewrite FAQ page with improved content and action
buttons".)

### 7. Split installation docs by audience and fix broken cards — DONE
Removed the dead "Install Packaged Versions" feature-card from
`content/docs/installation/_index.md` — it had no `link=` and there's no
actual packaged-install content behind it (GREEN currently only ships
source builds), so a missing link would have been the wrong fix; removing
the card was the honest one. Added ALPS-style audience-first framing above
the card grid: most users → general source install, NSF ACCESS users →
the NSF machine guide, DOE users → the DOE machine guide.

Fixed the copy-button `$`-prefix bug ALPS had already hit (PR #103): all 21
`$ ` shell-prompt prefixes in `from_sources.md`'s ShellSession blocks are
gone, so the copy button now yields runnable commands instead of lines
starting with a literal `$`. Also fixed a lexer-name typo (`ShellSesion` →
`ShellSession`) in the NCSA Delta guide.

Along the way, found and fixed a real regression from the hextra upgrade
(#1): GREEN's own `layouts/shortcodes/tabs.html` override predates the new
theme's `tab`/`tabs` shortcode protocol (child `tab` shortcodes now feed
their content into the parent's `.Store` instead of rendering directly),
so every tabbed page on the site — `from_sources.md`, `seet_example.md`,
`examples/si.md`, `examples/N2.md`, `pauli/_index.md` — was silently
rendering **empty tab panels** (tab buttons with no content behind them).
Deleted the redundant override; the theme's own `tabs.html` already
supports the legacy `items="..."` syntax GREEN's content uses, so this
was a net deletion, not a rewrite. Verified all five affected pages now
render their tab content and switch correctly.
(Mirrors ALPS PRs #43, #59 "improve source installation guide for
beginners", #86 "rewrite installation index with audience guidance and
action buttons", #98 "Remove sample supercomputer batch script from Spack
install docs", #103.)

### 8. Add a "Papers and Citations" page — DONE
Added `content/docs/publications/_index.md`, modeled directly on ALPS's
`documentation/pubs/_index.md` + `papers.md`: an intro explaining GREEN's
MIT license and citation expectations, the Green/WeakCoupling CPC paper
(Iskakov et al. 2025, https://doi.org/10.1016/j.cpc.2024.109380) as the
paper to cite, with Journal/Scholar/BibTeX buttons in a `btn-grid-4`, and a
closing note pointing to the Theory pages for individual algorithm
citations. The BibTeX itself lives at `static/data/iskakov2025.bib` and is
also linked directly from a new "Cite" button in the homepage CTA row and
a "Papers and Citations" button in the homepage panel, plus a feature-card
on the docs index page — matching ALPS's pattern of linking the bib file
straight from the homepage. (Mirrors ALPS PR #87 "redesign Publications
section as Papers and Citations".)

### 9. Audit content for correctness and pedagogy
ALPS did several multi-page passes fixing dead citations, factual/code
mismatches (parameters in prose not matching the actual scripts), heading
hierarchy, and MediaWiki-era leftover link text carried over from an older
site generation. GREEN's `docs/theory/`, `docs/legacy/`, and
`docs/tutorials/` trees are good candidates for the same kind of pass,
especially the `legacy/` docs which by name suggest older, potentially
stale content.
(Mirrors ALPS PRs #44, #60-#64, #73-#76, #102.)

### 10. Fix math rendering approach — DONE
This turned out not to be optional: after the hextra upgrade (#1), math had
silently stopped rendering site-wide (reported as `/docs/theory/introduction/`
showing raw LaTeX). Root causes:
- `hugo.yaml` never enabled Goldmark's `passthrough` extension, so `$...$`/
  `$$...$$` was never recognized as math at all (the new theme's math
  pipeline — build-time KaTeX via `transform.ToMath`, gated by a
  `Page.Store` flag set from the passthrough render hook — depends entirely
  on it). Added it with `$`/`$$` delimiters, matching ALPS.
- GREEN's own `head.html` override didn't include the new theme's
  math-engine-loading block (`scripts/katex.html` gated on
  `.Page.Store.Get "hasMath"`), so even with passthrough enabled nothing
  would have loaded the KaTeX CSS. Added it.
- 5 content files (`GW_theory.md`, `GF2_theory.md`, `embedding_theory.md`,
  `postprocessing/thermodynamics.md`, `getting-started/seet_example.md`)
  wrapped their math in a legacy `{{< raw >}}...{{< /raw >}}` shortcode — a
  workaround for the old client-side auto-render approach — which prevented
  Goldmark from recognizing the passthrough blocks under the new pipeline.
  Stripped the wrapper.
- Found and fixed two genuine content bugs the old (non-functional) math
  pipeline had been silently hiding: a stray `\)` in
  `Convergence_Acceleration.md` and a blank line inside a `$$...$$` block in
  `postprocessing/thermodynamics.md` (both broke KaTeX parsing/passthrough
  block detection once math was actually being processed).
- The old `mathjax/inline` shortcode is unused everywhere and was left in
  place (harmless dead code) rather than removed, since deleting it wasn't
  needed to fix rendering.

Verified: full-site scan of the built HTML for literal un-rendered `$$` (zero
matches) and spot-checked every flagged page in-browser in both light/dark
mode. (Mirrors ALPS's `passthrough` config and PR #82's
KaTeX-build-break fix.)

### 11. Small polish items — DONE (mobile hamburger menu)
Audited every custom page template for the exact bug ALPS hit in PR #90:
`core/menu.js`'s `DOMContentLoaded` handler calls
`sidebarContainer.setAttribute(...)`/`removeAttribute(...)` unconditionally
on load, before registering the hamburger's click listener — if
`.hextra-sidebar-container` isn't in the DOM, this throws and the whole
handler aborts, silently breaking the hamburger button on that page
(confirmed via direct `.click()` + `aria-expanded` checks, not just visual
inspection, since the failure is viewport-independent).

Unlike ALPS (whose bug was homepage-only), GREEN's homepage
(`green-home.html`) already included the sidebar partial and was fine.
The actual bugged templates were `layouts/news/list.html` and
`layouts/news/single.html` — neither ever called `partial "sidebar.html"`,
so the hamburger menu was completely non-functional on `/news/` and every
individual news post. Fixed with ALPS's exact approach: add
`{{ partial "sidebar.html" (dict "context" . "disableSidebar" true "displayPlaceholder" false) }}`
to both — invisible on desktop, functional on mobile. Verified no other
custom template (green-home, docs pages, about, pauli) has the bug.

## Suggested first PR

Given the above, the highest-value, lowest-risk starting point is probably:
bump the hextra theme (#1) + add a real `.btn-grid` component and use it on
the homepage (#3) + fix the dead "Install Packaged Versions" card (#7).
These are self-contained, don't require new content, and immediately make
the homepage feel as polished as ALPS's.
