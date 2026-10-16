#!/usr/bin/env python3
"""
new-post.py  -  add a blog post without touching any HTML.

    python3 new-post.py posts/my-post.md

The .md file starts with a front-matter block:

    ---
    title: Six Sigma and AI: where it actually helps
    category: Manufacturing
    date: 2026-10-20
    image: images/blog/six-sigma-ai.jpg      # optional header image
    excerpt: One line for the listing card.
    ---
    ## A heading

    Body text in markdown.

It writes blog/<slug>.html, adds the card to blog.html, and appends the URL
to sitemap.xml. Nothing else to do but commit.
"""
import os, re, sys, html, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://humanskills.in"


# ----------------------------------------------------------------- helpers
def slugify(text):
    t = text.lower().replace("'", "").replace("\u2019", "")
    s = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return re.sub(r"-{2,}", "-", s)


def read_front_matter(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", raw, re.S)
    if not m:
        sys.exit("!! %s has no front matter block (--- ... ---) at the top" % path)
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip().lower()] = v.strip()
    return meta, m.group(2)


def inline(t):
    """Bold, italic and links inside a line of text."""
    t = html.escape(t, quote=False)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", t)
    return t


def markdown_to_html(md):
    out, lines, i = [], md.split("\n"), 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("### "):
            out.append(f"  <h3>{inline(ln[4:])}</h3>")
        elif ln.startswith("## "):
            out.append(f"  <h2>{inline(ln[3:])}</h2>")
        elif ln.startswith("# "):
            out.append(f"  <h2>{inline(ln[2:])}</h2>")
        elif ln.strip() in ("---", "***"):
            out.append("  <hr>")
        elif ln.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].startswith("> "):
                buf.append(inline(lines[i][2:])); i += 1
            out.append("  <blockquote><p>" + " ".join(buf) + "</p></blockquote>")
            continue
        elif re.match(r"^[-*]\s+", ln):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                items.append("    <li>" + inline(re.sub(r"^[-*]\s+", "", lines[i])) + "</li>")
                i += 1
            out.append("  <ul>\n" + "\n".join(items) + "\n  </ul>")
            continue
        elif re.match(r"^\d+\.\s+", ln):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                items.append("    <li>" + inline(re.sub(r"^\d+\.\s+", "", lines[i])) + "</li>")
                i += 1
            out.append("  <ol>\n" + "\n".join(items) + "\n  </ol>")
            continue
        else:
            buf = []
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,3}\s|[-*]\s|\d+\.\s|>\s|---$)", lines[i].strip()):
                buf.append(lines[i].strip()); i += 1
            out.append("  <p>" + inline(" ".join(buf)) + "</p>")
            continue
        i += 1
    return "\n".join(out)


def extract(block_re, source):
    m = re.search(block_re, source, re.S)
    return m.group(0) if m else ""


# ----------------------------------------------------------------- build
def build(md_path):
    meta, body_md = read_front_matter(md_path)
    for req in ("title", "category", "date", "excerpt"):
        if req not in meta:
            sys.exit("!! front matter is missing '%s'" % req)

    title, category, date = meta["title"], meta["category"], meta["date"]
    excerpt, image = meta["excerpt"], meta.get("image", "").strip()
    slug = meta.get("slug") or slugify(title)
    read = meta.get("read") or ("%d min" % max(3, round(len(body_md.split()) / 200)))
    try:
        _d = datetime.date.fromisoformat(date)
        iso = _d.isoformat()
        pretty = "%d %s %d" % (_d.day, _d.strftime("%b"), _d.year)
    except ValueError:
        iso = pretty = date

    listing = open(os.path.join(ROOT, "blog.html"), encoding="utf-8").read()
    nav    = extract(r'<nav class="top-nav".*?</nav>', listing)
    footer = extract(r'<footer class="site-foot".*?</footer>', listing)
    css    = open(os.path.join(ROOT, "site.css"), encoding="utf-8").read() + "\n" + \
             open(os.path.join(ROOT, "blog.css"), encoding="utf-8").read()
    if not nav or not footer:
        sys.exit("!! could not read nav/footer from blog.html")

    hero_img = ""
    if image:
        hero_img = (f'\n    <div class="post-hero-img"><img src="../{image}" '
                    f'alt="{html.escape(title, quote=True)}" loading="eager"></div>')

    art = markdown_to_html(body_md)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} &mdash; Human Skills by Sudeep Ghosh</title>
<meta name="description" content="{html.escape(excerpt, quote=True)}">
<link rel="canonical" href="{SITE}/blog/{slug}.html">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title, quote=True)}">
<meta property="og:description" content="{html.escape(excerpt, quote=True)}">
<meta property="og:url" content="{SITE}/blog/{slug}.html">"""
    if image:
        page += f'\n<meta property="og:image" content="{SITE}/{image}">'
    page += f"""
<style>{css}</style>
<script type="application/ld+json">
{{
 "@context": "https://schema.org",
 "@graph": [
  {{"@type": "BlogPosting", "@id": "{SITE}/blog/{slug}.html#post",
    "headline": "{title}",
    "description": "{html.escape(excerpt, quote=True)}",
    "datePublished": "{iso}", "dateModified": "{iso}",
    "author": {{"@id": "{SITE}/#sudeep-ghosh"}},
    "publisher": {{"@id": "{SITE}/#organization"}},
    "mainEntityOfPage": {{"@id": "{SITE}/blog/{slug}.html#webpage"}},
    "articleSection": "{category}", "inLanguage": "en-IN","""
    if image:
        page += f'\n    "image": "{SITE}/{image}",'
    page += f"""
    "isPartOf": {{"@id": "{SITE}/#website"}}}},
  {{"@type": "WebPage", "@id": "{SITE}/blog/{slug}.html#webpage",
    "url": "{SITE}/blog/{slug}.html", "name": "{title}",
    "isPartOf": {{"@id": "{SITE}/#website"}},
    "breadcrumb": {{"@id": "{SITE}/blog/{slug}.html#breadcrumb"}}, "inLanguage": "en-IN"}},
  {{"@type": "BreadcrumbList", "@id": "{SITE}/blog/{slug}.html#breadcrumb",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE}/"}},
      {{"@type": "ListItem", "position": 2, "name": "Insights", "item": "{SITE}/blog.html"}},
      {{"@type": "ListItem", "position": 3, "name": "{title}", "item": "{SITE}/blog/{slug}.html"}}]}}
 ]
}}
</script>
</head>
<body>
{nav}
<header class="blog-hero" style="padding-bottom:40px;">
  <div class="blog-wrap" style="max-width:820px;">
    <div class="blog-hero__eyebrow" style="color:var(--accent-2)">{category}</div>
    <h1 class="blog-hero__title" style="font-size:clamp(30px,4.2vw,48px);">{title}</h1>
    <div class="post-card__meta" style="border:0;padding:0;margin:0;">{pretty} &middot; {read} read</div>{hero_img}
  </div>
</header>
<article class="article">
{art}
  <div class="byline">
    <div class="byline__img"></div>
    <div>
      <div class="byline__name">Sudeep Ghosh</div>
      <div class="byline__role">Consultant Trainer &mdash; AI &amp; Human Skills</div>
    </div>
  </div>
</article>
{footer}
</body></html>"""

    os.makedirs(os.path.join(ROOT, "blog"), exist_ok=True)
    out = os.path.join(ROOT, "blog", slug + ".html")
    page = post_process(page)
    open(out, "w", encoding="utf-8").write(page)

    # ---- card into blog.html ----
    card = (f'      <article class="post-card">\n'
            f'        <div class="post-card__tag">{category}</div>\n'
            f'        <h3 class="post-card__title"><a href="blog/{slug}.html">{title}</a></h3>\n'
            f'        <p class="post-card__ex">{excerpt}</p>\n'
            f'        <div class="post-card__meta">{pretty} &middot; {read} read</div>\n'
            f'      </article>')
    if f'blog/{slug}.html' not in listing:
        if '<div class="post-grid">' in listing:
            listing = re.sub(r'(<div class="post-grid">\s*)', r'\1\n' + card + "\n", listing, count=1)
        else:
            grid = '  <div class="post-grid">\n' + card + '\n  </div>\n'
            idx = listing.rfind("</section>", 0, listing.find('<footer class="site-foot"'))
            listing = listing[:idx] + grid + listing[idx:]
        open(os.path.join(ROOT, "blog.html"), "w", encoding="utf-8").write(listing)

    # ---- sitemap ----
    sm_path = os.path.join(ROOT, "sitemap.xml")
    if os.path.exists(sm_path):
        sm = open(sm_path, encoding="utf-8").read()
        loc = f"{SITE}/blog/{slug}.html"
        if loc not in sm:
            entry = f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{iso}</lastmod>\n  </url>\n'
            sm = re.sub(r'(\s*</urlset>)', "\n" + entry + r'\1', sm, count=1)
            open(sm_path, "w", encoding="utf-8").write(sm)

    print(f"  post      : blog/{slug}.html")
    print(f"  card added: blog.html")
    print(f"  sitemap   : {SITE}/blog/{slug}.html")
    print(f"  header img: {image if image else '(none - gradient fallback)'}")


# ------------------------------------------------------------------ blog plumbing
def post_process(html):
    """A post lives in blog/, so it must borrow blog.html's chrome and push every
    root-relative path up one level."""
    def balanced(html, marker):
        i = html.index(marker); depth = 0
        for m in re.finditer(r'<div\b[^>]*>|</div>', html[i:]):
            depth += 1 if m.group(0).startswith('<div') else -1
            if depth == 0:
                return html[i:i+m.end()]
        return html[i:]

    listing = open(os.path.join(ROOT, "blog.html"), encoding="utf-8").read()

    # 1. favicon / apple-touch-icon from the listing
    icons = "\n".join(re.findall(r'<link rel="(?:icon|apple-touch-icon)"[^>]*>', listing))

    # 2. the Explore-more FAB + the site's section drawer
    fab = re.search(r'<button class="toc-fab".*?</button>', listing, re.S).group(0)
    backdrop = re.search(r'<div class="toc-backdrop"[^>]*></div>', listing).group(0)
    drawer = balanced(listing, '<div class="section-drawer" id="sectionDrawer">')
    script = re.search(r'<script>\s*if \(typeof smoothScrollTo.*?</script>', listing, re.S)
    script = script.group(0) if script else ""
    chrome = "\n<!-- Explore more -->\n" + fab + "\n" + backdrop + "\n" + drawer + "\n" + script

    # 3. byline avatar -> the portrait
    html = html.replace('<div class="byline__img"></div>',
                        '<img class="byline__img" src="images/portrait.png" alt="Sudeep Ghosh" '
                        'width="52" height="52" loading="lazy">')

    # 4. push every root-relative path up a level (anchors like #s1 are left alone)
    def fix(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r'^(https?:|mailto:|tel:|data:|#|\.\./)', url) or url == "":
            return m.group(0)
        return '%s="../%s"' % (attr, url)
    html = re.sub(r'\b(href|src)="([^"]*)"', fix, html)
    icons = re.sub(r'href="(?!http)', 'href="../', icons)
    chrome = re.sub(r'\b(href|src)="(?!http|#|\.\./)', lambda m: m.group(1) + '="../', chrome)

    html = html.replace("</head>", icons + "\n</head>", 1)
    return html.replace("</body>", chrome + "\n</body>", 1)


FAB_TEMPLATE = """
<!-- ===== Explore more FAB + drawer ===== -->
<button class="toc-fab" id="tocFab" aria-label="Open section navigation">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
  </svg>
  <span class="toc-fab__label">Explore more</span>
  <span class="toc-fab__badge" id="tocFabBadge">01</span>
</button>
<div class="toc-backdrop" id="tocBackdrop"></div>
<div class="section-drawer" id="sectionDrawer">
  <a class="section-drawer__brand" href="../index.html" style="text-decoration:none;color:inherit;display:flex;align-items:center;gap:10px;margin-bottom:22px;padding-bottom:18px;border-bottom:1px solid var(--border);">
    <span class="brand-badge brand-badge--drawer"><img src="../images/logo-mark.png" alt="Human Skills by Sudeep Ghosh logo" width="36" height="36" decoding="async"></span>
    <div class="toc-brand__name">Human Skills by Sudeep Ghosh<span>Trainer &middot; Coach</span></div>
  </a>
  <div class="section-drawer__title">In this article</div>
{links}
</div>
<script>
if (typeof smoothScrollTo !== 'function') {{
  window.smoothScrollTo = function(id) {{
    var el = document.getElementById(id);
    if (el) el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
  }};
}}
(function() {{
  var fab=document.getElementById('tocFab'), drawer=document.getElementById('sectionDrawer');
  var backdrop=document.getElementById('tocBackdrop'), badge=document.getElementById('tocFabBadge');
  if(!fab||!drawer) return;
  function open(){{drawer.classList.add('expanded'); if(backdrop)backdrop.classList.add('show');}}
  function close(){{drawer.classList.remove('expanded'); if(backdrop)backdrop.classList.remove('show');}}
  fab.addEventListener('click',open);
  if(backdrop)backdrop.addEventListener('click',close);
  drawer.querySelectorAll('a[data-section]').forEach(function(link){{
    link.addEventListener('click',function(e){{
      e.preventDefault(); var sid=link.getAttribute('data-section'); close();
      var href=link.getAttribute('href');
      if(sid==='all'||sid==='top'&&href!=='#'){{ window.location.href=href; return; }}
      if(sid!=='top'&&typeof smoothScrollTo==='function'){{ smoothScrollTo(sid); history.replaceState(null,'','#'+sid); }}
      else {{ window.scrollTo({{top:0,behavior:'smooth'}}); }}
    }});
  }});
  document.addEventListener('keydown',function(e){{ if(e.key==='Escape') close(); }});
  var links=drawer.querySelectorAll('a[data-section]');
  var secs=[]; links.forEach(function(l){{ var id=l.getAttribute('href'); if(id&&id.charAt(0)==='#'){{var el=document.getElementById(id.slice(1)); if(el)secs.push({{el:el,link:l}});}} }});
  if('IntersectionObserver' in window){{
    var io=new IntersectionObserver(function(es){{ es.forEach(function(en){{
      if(en.isIntersecting){{ links.forEach(function(l){{l.classList.remove('active');}});
        var m=secs.find(function(s){{return s.el===en.target;}});
        if(m){{ m.link.classList.add('active'); if(badge){{var n=m.link.querySelector('.num'); if(n)badge.textContent=n.textContent;}} }}
      }} }}); }},{{rootMargin:'-20% 0px -70% 0px'}});
    secs.forEach(function(s){{ io.observe(s.el); }});
  }}
}})();
</script>
"""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python3 new-post.py posts/your-post.md")
    build(sys.argv[1])
