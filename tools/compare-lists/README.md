# Compare Two Lists

A single-file, client-side rewrite of a 2011 Perl/CGI tool that compares two
text lists and reports what's only in each one, their union, and their
intersection. Live at `/tools/compare-lists/` — open `index.html` directly
in a browser or serve it from any static host (including this GitHub Pages
site).

## What it does

Paste two lists (one entry per line) into the two text areas. As you type,
the page computes and displays, live:

- **List 1 only** — entries in list 1 that aren't in list 2
- **List 2 only** — entries in list 2 that aren't in list 1
- **Union** — every distinct entry across both lists
- **Intersection** — entries present in both lists

Each list's name (the "1" / "2" labels), and a "case insensitive" toggle,
work the same way they did in the original tool. Blank lines are ignored,
duplicate entries are collapsed, and every output list is sorted
alphabetically. A "Copy" button on each result panel copies that list to the
clipboard.

## Why it's a static rewrite

The original tool (`legacy/compare.public.php` + `legacy/compare.public.cgi`)
was a classic form-POST round trip: a static HTML page submitted to a Perl
CGI script, which parsed the two lists, computed the same four outputs, and
rendered a brand-new HTML page in response. The CGI process was stateless —
it read only what was in that one request and wrote only to the response
body, with no database, session, or file storage involved anywhere.

Because there was never any actual server-side state or computation that
required a backend, the entire round trip was unnecessary. The list-diffing
logic (trim, dedupe, sort, set difference/union/intersection) is a handful
of lines of straightforward JavaScript. Moving it into the browser makes the
tool:

- **Ephemeral** — nothing is sent over the network or stored anywhere;
  input never leaves the browser tab.
- **Instant** — results update as you type, no page reload or server
  round trip.
- **Zero-dependency** — one `.html` file, no build step, no runtime to
  host, no Perl/CGI environment to maintain.

## Behavioral notes vs. the original

- **Case-insensitive mode preserves original casing.** The original CGI
  script lowercased every entry when "case insensitive" was checked, so the
  displayed results lost the user's original capitalization. This rewrite
  compares case-insensitively but always displays the first-seen casing of
  each entry — a small, deliberate improvement, not a bug.
- **Sorting** uses `String.prototype.localeCompare`, which behaves like the
  original's ASCII sort for typical input but handles non-ASCII text more
  sensibly.
- **Output is safe by construction.** The original printed user input
  directly into HTML/`<textarea>` markup without escaping it — a reflected
  XSS vulnerability (crafted input could break out of the `<textarea>` and
  inject a `<script>`). This rewrite only ever assigns values through DOM
  properties (`textarea.value`, `.textContent`), which the browser always
  treats as plain text, so the same class of bug isn't possible here.

## Files

- `index.html` — the tool. Self-contained: markup, styles, and script in
  one file, no external requests.
- `legacy/compare.public.php` — original static HTML form (despite the
  `.php` extension, it contains no PHP).
  `legacy/compare.public.cgi` — original Perl CGI handler.
  Both are archived verbatim for reference/history and are not served or
  linked to from the live tool other than this README.
  Original copyright: © 2011 Whitehead Institute for Biomedical Research,
  by George Bell (Bioinformatics and Research Computing).

## Browser support

Any evergreen browser (uses `Map`/`Set`, template literals, and the
Clipboard API). The clipboard "Copy" buttons hide themselves automatically
if `navigator.clipboard` isn't available; the rest of the tool works
regardless.
