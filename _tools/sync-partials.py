#!/usr/bin/env python3
"""Copy the shared nav and footer into every page.

Edit _partials/nav.html or _partials/footer.html, then run:
    python3 _tools/sync-partials.py
Each page has <!-- BT-NAV --> ... <!-- /BT-NAV --> and
<!-- BT-FOOT --> ... <!-- /BT-FOOT --> markers; everything between them
is replaced. Add a new page by adding it to PAGES and pasting the two
empty marker pairs where the nav and footer should go.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = [
    "index.html",
    "guest-guide.html",
    "beaches.html",
    "reef-guide.html",
    "curacao-snorkel-guide.html",
    "restaurants.html",
    "banda-abou.html",
]

def render(partial, page):
    html = (ROOT / "_partials" / partial).read_text(encoding="utf-8").strip()
    # mark the current page
    html = html.replace(f'<a href="{page}">', f'<a href="{page}" aria-current="page">')
    if page == "index.html":
        # stay on the page instead of reloading it
        html = html.replace('href="index.html#contact"', 'href="#contact"')
    return html

def swap(text, tag, block, page):
    pat = re.compile(rf"(<!-- {tag} -->)(.*?)(<!-- /{tag} -->)", re.S)
    if not pat.search(text):
        sys.exit(f"{page}: missing <!-- {tag} --> markers")
    return pat.sub(lambda m: f"{m.group(1)}\n{block}\n{m.group(3)}", text, count=1)

for page in PAGES:
    path = ROOT / page
    text = path.read_text(encoding="utf-8")
    new = swap(text, "BT-NAV", render("nav.html", page), page)
    new = swap(new, "BT-FOOT", render("footer.html", page), page)
    if new != text:
        path.write_text(new, encoding="utf-8")
        print("updated", page)
    else:
        print("unchanged", page)
