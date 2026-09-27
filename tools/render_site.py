#!/usr/bin/env python3
"""Render the TechGnomo hub. GitHub Pages serves the HTML as-is."""

import html
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://techgnomo.com"
BRISBANE = ZoneInfo("Australia/Brisbane")

NAV = [
    ("/", "TechGnomo", "home"),
    ("/about/", "About", "about"),
    ("/news/", "News", "news"),
    ("/products/", "Products", "products"),
]

STATUSES = ("AVAILABLE", "BETA", "COMING SOON", "IN DEVELOPMENT")
STATUS_LABEL = {
    "available": "Available",
    "beta": "Beta",
    "coming-soon": "Coming soon",
    "in-development": "In development",
}


def load_json(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def post_moment(iso):
    if len(iso) == 10:
        # Unknown clock time. Sort at noon so the post stays on that day.
        # format_when does not print an hour for a date-only value.
        return datetime.fromisoformat(iso + "T12:00:00").replace(tzinfo=BRISBANE)
    return datetime.fromisoformat(iso).astimezone(BRISBANE)


def format_when(iso):
    moment = post_moment(iso)
    if len(iso) == 10:
        label = f"{moment.day} {moment.strftime('%B')} {moment.year}"
    else:
        hour = str(int(moment.strftime("%I")))
        label = f"{moment.day} {moment.strftime('%B')} {moment.year}, {hour}:{moment.strftime('%M')} {moment.strftime('%p').lower()}"
    return label


def news_posts():
    posts = load_json("news.json")
    return sorted(posts, key=lambda post: post_moment(post["datetime"]), reverse=True)


def products():
    return load_json("products.json")


def products_by_slug():
    return {item["slug"]: item for item in products()}


def announced_products():
    return [item for item in products() if item.get("announced")]


def nav_links(section):
    links = []
    for href, label, key in NAV:
        if key == "home":
            continue
        current = ' aria-current="page"' if key == section else ""
        links.append(f'<a href="{href}"{current}>{label}</a>')
    return "\n            ".join(links)


def header(section):
    home_current = ' aria-current="page"' if section == "home" else ""
    return f"""
    <header class="site-header">
      <div class="header-bar">
        <nav class="site-nav" id="site-nav" aria-label="Primary">
          <a class="home-name" href="/"{home_current}>TechGnomo</a>
          <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav-panel" aria-label="Open menu">
            <span class="menu-word">Menu</span>
          </button>
          <div class="nav-panel" id="nav-panel">
            {nav_links(section)}
          </div>
        </nav>
      </div>
    </header>"""


def footer(with_mark=True):
    mark = '<span class="mark" aria-hidden="true"></span>' if with_mark else ""
    return f"""
    <footer class="foot">
      {mark}
      <span class="foot-sign">TechGnomo · Brisbane</span>
      <nav class="foot-nav" aria-label="Footer">
        <a href="/studio/">Studio</a>
        <a href="/lab/">Lab</a>
        <a href="/contact/">Contact</a>
        <a href="/privacy/">Privacy</a>
      </nav>
      <a href="mailto:gnomocode@gmail.com">gnomocode@gmail.com</a>
    </footer>
    <div class="sill" aria-hidden="true"></div>"""


def post_html(post, catalogue):
    when = format_when(post["datetime"])
    status = post.get("status") or ""
    status_html = f'<span class="post-status">{html.escape(status)}</span>' if status else ""
    product = catalogue.get(post.get("product") or "")
    product_html = ""
    if product and product.get("announced"):
        product_html = (
            f'<p class="post-product"><a href="{html.escape(product["url"])}">'
            f'{html.escape(product["name"])}</a></p>'
        )
    image_html = ""
    if post.get("image"):
        alt = html.escape(post.get("imageAlt") or "")
        width = int(post.get("imageWidth") or 0)
        height = int(post.get("imageHeight") or 0)
        dims = f' width="{width}" height="{height}"' if width and height else ""
        image_html = (
            f'<img class="post-media" src="{html.escape(post["image"])}"{dims} '
            f'alt="{alt}" loading="lazy" decoding="async" />'
        )
    permalink = f'/news/#{html.escape(post["id"])}'
    return f"""
        <article class="post" id="{html.escape(post["id"])}">
          <p class="post-meta">
            <time datetime="{html.escape(post["datetime"])}">{when}</time>
            {status_html}
            <a class="permalink" href="{permalink}">Permalink <span class="sr">for {html.escape(when)}</span></a>
          </p>
          <p class="post-text">{html.escape(post["text"])}</p>
          {image_html}
          {product_html}
        </article>"""


def feed_html(posts, catalogue):
    return "\n".join(post_html(post, catalogue) for post in posts)


def product_window(item, heading="h2"):
    phrase = html.escape(item.get("phrase") or STATUS_LABEL.get(item["status"], item["status"]))
    return f"""
      <article class="window" style="--window-surface:{item["surface"]};--window-card:{item["card"]};--window-accent:{item["accent"]};--window-ink:{item["ink"]};--window-rule:{item["rule"]}">
        <div class="window-copy">
          <p class="status">{phrase}</p>
          <{heading}>{html.escape(item["name"])}</{heading}>
          <p>{html.escape(item["summary"])}</p>
          <p class="actions"><a href="{html.escape(item["url"])}">See {html.escape(item["name"])}</a></p>
        </div>
        <div class="window-screen">
          <img src="{html.escape(item["image"])}" width="{int(item["imageWidth"])}" height="{int(item["imageHeight"])}" alt="{html.escape(item["imageAlt"])}" loading="lazy" decoding="async" />
        </div>
      </article>"""


def page(spec):
    slug = spec["path"]
    title = spec["title"]
    description = spec["description"]
    canonical = ORIGIN + spec["url"]
    robots = spec.get("robots", "index, follow, max-image-preview:large")
    scripts = "\n    ".join(f'<script src="{src}" defer></script>' for src in spec.get("scripts", []))
    section = spec.get("section", "")
    head_extra = ""
    if spec.get("italic"):
        head_extra = """
    <link rel="preload" href="/assets/fonts/fraunces-latin-opsz-italic.woff2" as="font" type="font/woff2" crossorigin />"""
    head_html = spec.get("head_html") or ""
    graph = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": description,
        "url": canonical,
        "inLanguage": "en-AU",
        "isPartOf": {"@type": "WebSite", "name": "TechGnomo", "url": ORIGIN + "/"},
        "author": {
            "@type": "Person",
            "name": "Fabio D’Anna",
            "url": ORIGIN + "/about/",
        },
    }
    blocks = [graph]
    if spec.get("jsonld"):
        extra = dict(spec["jsonld"])
        extra.pop("@context", None)
        graph.pop("@context", None)
        blocks = [{"@context": "https://schema.org", "@graph": [graph, extra]}]
        jsonld = json.dumps(blocks[0], ensure_ascii=False, indent=2)
    else:
        jsonld = json.dumps(graph, ensure_ascii=False, indent=2)

    shell_header = header(section)
    doc = f"""<!doctype html>
<html lang="en-AU" class="no-js">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <meta name="description" content="{description}" />
    <meta name="author" content="Fabio D’Anna" />
    <meta name="theme-color" content="#f1eadc" />
    <meta name="color-scheme" content="light" />
    <meta name="robots" content="{robots}" />
    <link rel="canonical" href="{canonical}" />
    <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
    <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png" />
    <link rel="manifest" href="/site.webmanifest" />
    <link rel="preload" href="/assets/fonts/fraunces-latin-opsz-normal.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="preload" href="/assets/fonts/source-sans-3-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin />{head_extra}
    <link rel="stylesheet" href="/assets/css/tokens.css" />
    <link rel="stylesheet" href="/assets/css/site.css" />{head_html}
    <meta property="og:type" content="website" />
    <meta property="og:locale" content="en_AU" />
    <meta property="og:site_name" content="TechGnomo" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:image" content="{ORIGIN}/assets/img/og-v1b.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />
    <meta name="twitter:image" content="{ORIGIN}/assets/img/og-v1b.png" />
    <script>document.documentElement.classList.replace("no-js","js");</script>
    <script type="application/ld+json">
{jsonld}
    </script>
  </head>
  <body{spec.get("body_open", ' class="is-hub"' if spec.get("hub") else "")}>
    <a class="skip" href="#main">Skip to content</a>{shell_header}
    <main id="main" class="{spec.get("main_class", "page")}">
{spec["body"]}
    </main>
{footer(True)}
    <script src="/assets/js/nav.js" defer></script>
    {scripts}
  </body>
</html>
"""
    dest = ROOT / slug
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")
    print("wrote", slug)


def redirect(src, target, label):
    html = f"""<!doctype html>
<html lang="en-AU">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{label} | TechGnomo</title>
    <link rel="canonical" href="{ORIGIN}{target}" />
    <meta name="robots" content="noindex" />
    <meta http-equiv="refresh" content="0; url={target}" />
    <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
    <link rel="stylesheet" href="/assets/css/tokens.css" />
    <link rel="stylesheet" href="/assets/css/site.css" />
  </head>
  <body>
    <main class="page page-narrow">
      <p><a href="{target}">{label}</a> has moved.</p>
    </main>
  </body>
</html>
"""
    (ROOT / src).write_text(html, encoding="utf-8")
    print("redirect", src, "->", target)


def pages():
    person = {
        "@type": "Person",
        "name": "Fabio D’Anna",
        "url": ORIGIN + "/about/",
        "email": "gnomocode@gmail.com",
        "image": ORIGIN + "/assets/img/fabio.webp",
        "homeLocation": {
            "@type": "Place",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Brisbane",
                "addressRegion": "QLD",
                "addressCountry": "AU",
            },
        },
        "sameAs": [
            "https://github.com/TechGnomo",
            "https://www.linkedin.com/in/fabio-d-anna-5083b5378/",
        ],
    }
    website = {
        "@type": "WebSite",
        "name": "TechGnomo",
        "url": ORIGIN + "/",
        "description": "TechGnomo builds practical digital products. ClearMoneyPath is coming in 3 weeks.",
        "publisher": {"@type": "Person", "name": "Fabio D’Anna", "url": ORIGIN + "/about/"},
    }
    cmp = {
        "@type": "SoftwareApplication",
        "name": "ClearMoneyPath",
        "url": ORIGIN + "/products/clearmoneypath/",
        "description": "A TechGnomo product. Pay-cycle planner, coming in 3 weeks. Not for sale. A web version is being built.",
        "creator": {"@type": "Person", "name": "Fabio D’Anna", "url": ORIGIN + "/about/"},
        "isPartOf": {"@type": "WebSite", "name": "TechGnomo", "url": ORIGIN + "/"},
    }
    scope = {
        "@type": "WebApplication",
        "name": "MVP Scope Checker",
        "url": ORIGIN + "/lab/scope-checker/",
        "description": "A free browser experiment from the TechGnomo lab. Nothing is uploaded.",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Any web browser",
        "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "AUD"},
        "creator": {"@type": "Person", "name": "Fabio D’Anna", "url": ORIGIN + "/about/"},
    }
    catalogue = products_by_slug()
    posts = news_posts()
    latest = feed_html(posts[:3], catalogue)
    gallery = "\n".join(product_window(item, "h2") for item in announced_products())
    featured = product_window(catalogue["clearmoneypath"], "h3")
    cmp_log = feed_html([post for post in posts if post.get("product") == "clearmoneypath"], catalogue)
    news_feed = feed_html(posts, catalogue)
    return [
        {
            "path": "index.html",
            "url": "/",
            "title": "TechGnomo",
            "description": "TechGnomo builds practical digital products. ClearMoneyPath, a pay-cycle planner, is coming in 3 weeks.",
            "section": "home",
            "hub": True,
            "italic": True,
            "main_class": "page hub",
            "jsonld": website,
            "body": f"""
      <div class="plate arrive">
        <p class="mark-slot"><span class="mark" aria-hidden="true"></span></p>
        <p class="kicker">Welcome to</p>
        <h1 class="wordmark">TechGnomo</h1>
        <p class="line">A workshop for practical digital products.</p>
      </div>
      <div class="hub-rest">
        <p class="hub-lead">It exists so each product can solve its own problem, and still belong somewhere.</p>
        <section class="section" aria-labelledby="build">
          <h2 id="build">What we build</h2>
          <ul class="build">
            <li>Products that can look nothing like each other.</li>
            <li>Experiments, including <a href="/lab/">tools you can open</a>.</li>
            <li>Small digital tools, when a smaller thing is the honest answer.</li>
          </ul>
        </section>
        <section class="section" aria-labelledby="now">
          <h2 id="now">Now</h2>
          {featured}
        </section>
        <section class="section" aria-labelledby="latest">
          <h2 id="latest">Latest</h2>
          <div class="feed">
            {latest}
          </div>
          <p class="actions"><a href="/news/">All news</a></p>
        </section>
        <p class="explore"><a href="/products/">Explore products</a></p>
      </div>
""",
        },
        {
            "path": "about/index.html",
            "url": "/about/",
            "title": "About | TechGnomo",
            "description": "TechGnomo builds practical digital products. Fabio D’Anna is the founder, in Brisbane.",
            "section": "about",
            "jsonld": person,
            "body": """
      <p class="kicker">About</p>
      <h1>The workshop, and the person who runs it.</h1>
      <p class="lede">TechGnomo builds practical digital products, tries ideas, and ships the ones that solve a specific problem.</p>
      <p class="measure">The products can look nothing like each other. Each one has its own problem, so each one has its own face. TechGnomo is the parent that connects them.</p>
      <div class="split">
        <figure class="portrait">
          <img src="/assets/img/fabio.webp" width="720" height="1003" alt="Portrait of Fabio D’Anna outdoors, wearing a dark shirt." />
          <figcaption>Fabio D’Anna, Brisbane.</figcaption>
        </figure>
        <div>
          <h2>Fabio</h2>
          <p>Fabio D’Anna is the founder. About ten years in hospitality, then software. He decides what a product should do, and he checks the work, including when a machine helped write it.</p>
          <p>He is open to junior developer and IT support roles, in Brisbane or remote within Australia.</p>
          <p>Diploma of Software Development. Diploma of IT Networking and Telecommunications. Both completed. Details on request.</p>
          <p>gnomocode@gmail.com · <a href="https://github.com/TechGnomo">GitHub</a> · <a href="https://www.linkedin.com/in/fabio-d-anna-5083b5378/">LinkedIn</a></p>
          <p class="actions"><a href="/contact/">Contact</a></p>
        </div>
      </div>
      <section class="section" aria-labelledby="level">
        <h2 id="level">At an honest level</h2>
        <ul class="measure">
          <li>HTML, CSS and accessible pages. Working. This site.</li>
          <li>JavaScript. Working, on small tools. The scope checker runs in the browser.</li>
          <li>React Native, Expo and Firebase. In use on ClearMoneyPath, still learning.</li>
          <li>Java and C++. Diploma foundation, not daily tools.</li>
          <li>IT networking and support. Diploma foundation. Enough for junior IT support, not a security practice.</li>
          <li>AI-assisted development. A daily method. He decides what to keep.</li>
          <li>Automation and cybersecurity. Currently learning. Not services.</li>
          <li>Hospitality operations. About ten years. The deep skill. Software is the newer one.</li>
        </ul>
      </section>
""",
        },
        {
            "path": "news/index.html",
            "url": "/news/",
            "title": "News | TechGnomo",
            "description": "A short TechGnomo log: build notes, fixes, and product news. Not a blog archive.",
            "section": "news",
            "body": f"""
      <p class="kicker">News</p>
      <h1>The log</h1>
      <p class="lede">Build notes, fixes, and the occasional announcement. Short on purpose.</p>
      <div class="feed">
        {news_feed}
      </div>
""",
        },
        {
            "path": "products/index.html",
            "url": "/products/",
            "title": "Products | TechGnomo",
            "description": "Products from TechGnomo. ClearMoneyPath is coming in 3 weeks. Nothing else is announced.",
            "section": "products",
            "body": f"""
      <p class="kicker">TechGnomo</p>
      <h1>Products</h1>
      <p class="lede">What the workshop is shipping, and what is still on the way. Only announced work is on this page.</p>
      <div class="gallery">
        {gallery}
      </div>
      <section class="section" aria-labelledby="next">
        <h2 id="next">What’s next</h2>
        <p class="measure">More in the workshop. Nothing else is announced.</p>
      </section>
""",
        },
        {
            "path": "products/clearmoneypath/index.html",
            "url": "/products/clearmoneypath/",
            "title": "ClearMoneyPath | TechGnomo",
            "description": "ClearMoneyPath is a TechGnomo product: a pay-cycle planner coming in 3 weeks. Not for sale. Screens use sample data.",
            "section": "products",
            "body_open": ' data-product="clearmoneypath" data-product-theme="/assets/css/themes/clearmoneypath.css"',
            "head_html": """
    <style>
      [data-product="clearmoneypath"] .shot {
        background: #06101e;
        color: #f7faff;
        border: 1px solid #1f2d43;
        border-radius: 22px;
        padding: var(--space-3);
      }
      [data-product="clearmoneypath"] .shot img {
        border: 0;
        background: transparent;
        border-radius: 16px;
      }
      [data-product="clearmoneypath"] .shot figcaption {
        color: #7f90a8;
      }
    </style>
    <noscript>
      <link rel="stylesheet" href="/assets/css/product-transition.css" />
      <link rel="stylesheet" href="/assets/css/themes/clearmoneypath.css" />
    </noscript>""",
            "scripts": ["/assets/js/spend-sketch.js", "/assets/js/product-transition.js"],
            "jsonld": cmp,
            "body": f"""
      <div data-stage="parent">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/products/">Products</a> <span aria-hidden="true">/</span> <span aria-current="page">ClearMoneyPath</span></nav>
      <p class="kicker">A TechGnomo product</p>
      <h1>ClearMoneyPath</h1>
      <p class="status">Coming in 3 weeks</p>
      <p class="lede">A pay-cycle planner for the stretch between paydays. Bills, a debt payment and savings come out first. What remains is left this cycle.</p>
      <p class="measure">An Android beta exists. It is not a public release, and it is not on Google Play or the App Store. A web version is being built. There is nothing to buy.</p>
      <p class="actions">
        <a href="#sketch-title">Try the sketch</a>
        <a href="/news/#cmp-three-weeks">Follow progress in News</a>
        <a href="/contact/">Contact</a>
      </p>
      </div>

      <section class="section" data-stage="approach" aria-labelledby="problem">
        <h2 id="problem">The problem</h2>
        <p class="measure">A bank balance is not a plan. Pay does not always land on the first of the month, and bills do not wait. Rent and a debt payment that fall before the next payday are still sitting in that balance, pretending to be spendable.</p>
        <p class="measure">I know that week from hospitality: the hours change, the pay changes, the bills do not. ClearMoneyPath is the planner for that stretch.</p>
      </section>

      <section class="section" data-stage="crossover" aria-labelledby="screens">
        <h2 id="screens">Screens with sample data</h2>
        <p class="measure quiet">From the Android beta, which is not a public release. These figures are sample data, not a person’s accounts.</p>
        <div class="shots">
          <figure class="shot">
            <img src="/assets/img/cmp-home.webp" width="780" height="1688" alt="ClearMoneyPath home with sample data. Left this cycle is shown, with a line that this is general information, not personal financial advice." loading="lazy" decoding="async" />
            <figcaption>Home. Sample data.</figcaption>
          </figure>
          <figure class="shot">
            <img src="/assets/img/cmp-money.webp" width="780" height="1688" alt="ClearMoneyPath money screen with sample data, split into money in and money out." loading="lazy" decoding="async" />
            <figcaption>Money in and out. Sample data.</figcaption>
          </figure>
          <figure class="shot">
            <img src="/assets/img/cmp-debts.webp" width="780" height="1688" alt="ClearMoneyPath debts screen with sample data. Snowball is selected, and the first debt in snowball order is marked." loading="lazy" decoding="async" />
            <figcaption>Debt order: snowball, avalanche or your own. Sample data.</figcaption>
          </figure>
          <figure class="shot">
            <img src="/assets/img/cmp-plan.webp" width="780" height="1688" alt="ClearMoneyPath payday plan with sample data. The cycle closes when payday arrives." loading="lazy" decoding="async" />
            <figcaption>The payday plan. Sample data.</figcaption>
          </figure>
        </div>
        <p class="measure">General information only, not personal financial advice.</p>
      </section>

      <div data-stage="product">
      <section class="section" aria-labelledby="does">
        <h2 id="does">What it does</h2>
        <ul class="measure">
          <li>Shows what is left this cycle, and the next payday. A weekly cycle closes when payday arrives.</li>
          <li>Records money in, bills, spending and savings.</li>
          <li>Tracks each debt’s balance, minimum and rate, and lists debts in snowball order, avalanche order, or your order.</li>
          <li>Lays the cycle out as a short plan: bills covered, savings set aside, spending inside what is left.</li>
        </ul>
        <p class="measure">Built with React Native, Expo and Firebase. I use AI assistance heavily while building. I decide the pay-cycle model, what a bill or a debt has to do, and whether a screen is telling the truth. Generated code still needs checking, especially around dates and money. The repository is not public yet. I’m happy to walk through it.</p>
      </section>

      <section class="section" aria-labelledby="sketch-title">
        <p class="kicker">A TechGnomo product</p>
        <h2 id="sketch-title">Try the idea on this page</h2>
        <p class="measure">This is a sketch of the subtraction, not the product, and not for sale. The numbers stay in your browser.</p>
        <form id="spend-sketch">
          <div class="sketch-grid">
            <div class="field">
              <label for="pay"><span>Pay this cycle (A$)</span></label>
              <input id="pay" name="pay" type="number" inputmode="decimal" min="0" step="0.01" value="1840" />
            </div>
            <div class="field">
              <label for="bills"><span>Bills due before next payday</span></label>
              <input id="bills" name="bills" type="number" inputmode="decimal" min="0" step="0.01" value="620" />
            </div>
            <div class="field">
              <label for="debt"><span>Debt payment this cycle</span></label>
              <input id="debt" name="debt" type="number" inputmode="decimal" min="0" step="0.01" value="150" />
            </div>
            <div class="field">
              <label for="save"><span>Set aside for savings</span></label>
              <input id="save" name="save" type="number" inputmode="decimal" min="0" step="0.01" value="80" />
            </div>
          </div>
          <p class="sketch-result" aria-live="polite"><span id="left-label">Left this cycle</span> <strong id="left-amount">$990.00</strong> <span class="advice">General information only, not personal financial advice.</span></p>
          <p class="help">Sample figures. If the bills and payments are larger than the pay, it says you are short.</p>
        </form>
      </section>

      <section class="section" aria-labelledby="not">
        <h2 id="not">What it is not</h2>
        <ul class="measure">
          <li>Not for sale. No checkout, no waitlist price, no “founding licence”.</li>
          <li>Not financial advice, and it does not suggest loans, cards or other products.</li>
          <li>Not a public app yet. The screens on this page use sample data.</li>
        </ul>
        <p class="actions">
          <a href="/products/">All products</a>
          <a href="/news/">News</a>
          <a href="/contact/">Contact</a>
        </p>
      </section>
      <section class="section" aria-labelledby="log">
        <h2 id="log">From the log</h2>
        <div class="feed">
          {cmp_log}
        </div>
      </section>
      </div>
""",
        },
        {
            "path": "products/gnomorestaurant/index.html",
            "url": "/products/gnomorestaurant/",
            "title": "GnomoRestaurant | TechGnomo",
            "description": "GnomoRestaurant is a TechGnomo product: a prototype for venue costing, menu pricing, suppliers, stocktake and ordering. No public build.",
            "robots": "noindex, follow",
            "section": "products",
            "body": """
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/products/">Products</a> <span aria-hidden="true">/</span> <span aria-current="page">GnomoRestaurant</span></nav>
      <p class="kicker">A TechGnomo product</p>
      <h1>GnomoRestaurant</h1>
      <p class="status">Prototype</p>
      <p class="lede">The unglamorous part of a venue: what a plate costs, what to charge, who supplies it, what is in the fridge, and what to order next.</p>
      <p class="measure">Prototype means parts of it run on my machine. There is no public build, so there is no screenshot. I am not going to draw one.</p>

      <h2>From the floor</h2>
      <ul class="measure">
        <li>Stocktake eats Sunday.</li>
        <li>Plate cost is a guess once a supplier puts prices up.</li>
        <li>Ordering lives in someone’s head.</li>
        <li>The menu price and the recipe have drifted apart.</li>
      </ul>
      <p class="measure">That list is from the floor: about ten years in hospitality, including restaurant management, drink-list costing and talking to suppliers.</p>

      <h2>What the prototype covers</h2>
      <p class="measure">This is the scope. It is not a picture of the interface.</p>
      <ul class="measure">
        <li>Recipes, and a plate cost that moves when a supplier price moves.</li>
        <li>Menu pricing against that cost.</li>
        <li>Suppliers, stocktake and ordering.</li>
      </ul>
      <div class="note">
        <h2>Nothing to open yet</h2>
        <p>No store listing and no public repository. If you are hiring and the domain matters, email me and I will show you the build I actually have.</p>
        <p><a href="mailto:gnomocode@gmail.com?subject=GnomoRestaurant">gnomocode@gmail.com</a></p>
      </div>
      <p>It is not client work, and it is not for sale. The jobs I can take for a venue today are on the <a href="/studio/">studio</a> page.</p>
""",
        },
        {
            "path": "studio/index.html",
            "url": "/studio/",
            "title": "Studio | TechGnomo",
            "description": "TechGnomo Studio: two small fixed-price jobs for independent cafés and restaurants. A one-page website, or a costing and stocktake sheet.",
            "section": "studio",
            "body": """
      <p class="kicker">TechGnomo Studio · Brisbane</p>
      <h1>Small jobs for independent venues.</h1>
      <p class="lede">Studio is the name for work TechGnomo does for someone else. Two offers. A fixed quote after a free 20-minute call. Not an agency, and not a menu of apps.</p>
      <p class="measure">I’m Fabio. About ten years on hospitality floors. These are the straightforward fixes a venue actually asks for.</p>

      <h2>What I can take off the list</h2>
      <ul class="measure">
        <li>People message to ask if you’re open, or the menu online is the old one.</li>
        <li>You don’t know the plate cost since the supplier put prices up.</li>
        <li>Stocktake eats Sunday, and the order lives in someone’s head.</li>
      </ul>

      <article class="offer">
        <h2>A venue page</h2>
        <p>One fast page for an independent café, restaurant or bar: hours, where you are, the current menu, and links to the booking or ordering you already use.</p>
        <p>Typically A$600–1,200. Indicative. The quote is the price.</p>
        <p>Fixed quote after a free 20-minute call. Half to start, half when it goes live.</p>
        <h3>What you get</h3>
        <ul>
          <li>A single mobile-first page.</li>
          <li>Hours, location, menu, and your existing booking or order links.</li>
          <li>A proper page title and description.</li>
          <li>A check of the obvious Google Business bits: hours, menu link, website link.</li>
          <li>The domain and hosting stay in your name.</li>
          <li>A one-page note on simple updates, and two rounds of corrections.</li>
        </ul>
        <h3>Not included</h3>
        <ul>
          <li>Online ordering, payments, or a shop.</li>
          <li>A photo shoot. You supply the pictures.</li>
          <li>A weekly menu rewrite. That is a separate small fee, agreed first.</li>
          <li>An SEO retainer.</li>
        </ul>
      </article>

      <article class="offer">
        <h2>Fix the sheet</h2>
        <p>One spreadsheet, in your Google account, for a job the floor already does on paper.</p>
        <p>Typically A$250–600. Indicative. The quote is the price.</p>
        <p>One sheet per job. Or A$45–60 an hour to tidy a sheet you already have, with a cap on the quote.</p>
        <h3>Pick one</h3>
        <ul>
          <li>Recipe and plate cost: change a supplier price, the dishes move, a target margin is flagged.</li>
          <li>A par-level order sheet per supplier.</li>
          <li>A stocktake count sheet that works on a phone.</li>
        </ul>
        <p>You get the sheet, a 30-minute handover, and two weeks of fixes. This does not replace a full inventory system. If the till already runs your stock, I will say so on the call.</p>
      </article>

      <section class="section" aria-labelledby="how">
        <h2 id="how">How it works</h2>
        <ol class="steps measure">
          <li>A free 20-minute call. You say what is messy. I say whether it is one of these two jobs.</li>
          <li>A fixed quote: price, what is in, what is out, and how long I expect.</li>
          <li>I build it and show you once while there is still time to correct me.</li>
          <li>Handover. You own the files and the accounts.</li>
        </ol>
        <p class="measure">I still work in hospitality, so I won’t book over your service, and I won’t promise overnight.</p>
      </section>

      <div class="note">
        <h2>Early days</h2>
        <p>I haven’t done paid client work under TechGnomo yet. The first one or two jobs can be at an introductory price, written on the quote, in exchange for permission to show the work and for honest feedback. I won’t invent a testimonial.</p>
      </div>

      <section class="section" aria-labelledby="dont">
        <h2 id="dont">What I don’t do</h2>
        <p class="measure">Custom mobile apps, online shops, card payments, SEO retainers, AI automation, cybersecurity, and storing your customers’ personal data beyond a link to email or a booking tool you already use.</p>
      </section>

      <section class="section" aria-labelledby="faq">
        <h2 id="faq">Questions that come up</h2>
        <details>
          <summary>Do I own the work?</summary>
          <p>Yes. You own the files, and the words and photos you supplied. The domain and hosting stay in your name.</p>
        </details>
        <details>
          <summary>What if we need a change later?</summary>
          <p>Two rounds are in the quote. After that, updates are a small fee we agree before I start.</p>
        </details>
        <details>
          <summary>How does payment work?</summary>
          <p>Half when we start, half when I hand it over. Both amounts are on the quote.</p>
        </details>
        <details>
          <summary>Can you work around service?</summary>
          <p>Yes. I won’t call during a Friday night.</p>
        </details>
        <details>
          <summary>Do you have an ABN?</summary>
          <p>Ask on the call if you need one on the invoice.</p>
        </details>
      </section>

      <section class="section">
        <h2>Start with the problem</h2>
        <p class="measure">A few lines is enough: the venue, what is broken, and when you are free for 20 minutes.</p>
        <p class="actions"><a href="mailto:gnomocode@gmail.com?subject=Studio%20job%20via%20TechGnomo">gnomocode@gmail.com</a></p>
        <p class="quiet">If the link doesn’t open a mail app, copy the address. There is no form on a server.</p>
      </section>
""",
        },
        {
            "path": "lab/index.html",
            "url": "/lab/",
            "title": "Lab | TechGnomo",
            "description": "The TechGnomo lab: experiments, including the free MVP Scope Checker, and what Fabio is actually learning.",
            "section": "lab",
            "body": """
      <p class="kicker">TechGnomo</p>
      <h1>Lab</h1>
      <p class="lede">Where a test can live without being asked to be a product. One thing here you can open.</p>
      <article class="section">
        <p class="status">Live · experiment</p>
        <h2><a href="/lab/scope-checker/">MVP Scope Checker</a></h2>
        <p class="measure">A browser tool that cuts an app idea down to a first test and writes a brief. The score is a fixed formula, not research. Nothing is uploaded.</p>
      </article>
      <section class="section" aria-labelledby="learn">
        <h2 id="learn">What I’m learning</h2>
        <p class="measure">These are not offers.</p>
        <ul class="skill-list">
          <li>
            <h3>AI</h3>
            <p class="level">Using it to build. Learning where it fails.</p>
            <p>I use AI assistance on most of the software I make. The part I’m studying is the failure: invented detail, skipped edge cases, a confident tone when the code is wrong.</p>
          </li>
          <li>
            <h3>Automation</h3>
            <p class="level">Currently learning</p>
            <p>How to make a repeated admin job smaller without hiding the decision. The sheet on the studio page is the honest version of this. I am not selling an automation platform.</p>
          </li>
          <li>
            <h3>Cybersecurity</h3>
            <p class="level">Currently learning</p>
            <p>Foundations, slowly. I am not offering security work.</p>
          </li>
        </ul>
        <p class="measure quiet">Notes from the work will be published when a piece is finished. There is no media section until then.</p>
      </section>
""",
        },
        {
            "path": "lab/scope-checker/index.html",
            "url": "/lab/scope-checker/",
            "title": "MVP Scope Checker | TechGnomo",
            "description": "A free browser experiment from the TechGnomo lab. Cut an app idea down to a first test. Nothing is uploaded.",
            "section": "lab",
            "scripts": ["/assets/js/scope-checker.js"],
            "jsonld": scope,
            "body": """
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/lab/">Lab</a> <span aria-hidden="true">/</span> <span aria-current="page">MVP Scope Checker</span></nav>
      <p class="status">Live · experiment</p>
      <h1>Make the first version smaller.</h1>
      <p class="lede">Name the person, the problem and the features. The checker keeps three features in the first test, parks the rest, and writes a brief. The score is a fixed formula, not market research.</p>
      <p class="quiet">Runs in your browser. Nothing is uploaded unless you choose to email the brief.</p>
      <div class="tool-grid" id="scope-workspace">
        <form id="scopeForm">
          <div class="field">
            <label for="productName"><span>Working product name</span></label>
            <input id="productName" name="productName" type="text" autocomplete="off" maxlength="80" required placeholder="e.g. ShiftMate" />
          </div>
          <div class="field">
            <label for="targetUser"><span>Who is the first specific person?</span></label>
            <input id="targetUser" name="targetUser" type="text" autocomplete="off" maxlength="160" required placeholder="e.g. Independent restaurant managers" />
          </div>
          <div class="field">
            <label for="problem"><span>What recurring problem do they have?</span></label>
            <textarea id="problem" name="problem" rows="4" maxlength="600" required placeholder="Describe what happens now, not the app you want to build."></textarea>
          </div>
          <div class="field">
            <label for="outcome"><span>What single outcome should improve?</span></label>
            <input id="outcome" name="outcome" type="text" autocomplete="off" maxlength="220" required placeholder="e.g. Fill an uncovered shift in under 10 minutes" />
          </div>
          <div class="field">
            <label for="features"><span>Proposed features, one per line</span></label>
            <textarea id="features" name="features" rows="7" maxlength="1400" required aria-describedby="features-help" placeholder="Create a shift&#10;Notify available staff&#10;Let one person accept&#10;Manager confirms"></textarea>
            <p class="help" id="features-help">The first three lines are treated as the core.</p>
          </div>
          <fieldset>
            <legend>Does version one require any of these?</legend>
            <div class="check-list">
              <label><input type="checkbox" name="complexity" value="User accounts and authentication" /> User accounts and authentication</label>
              <label><input type="checkbox" name="complexity" value="Payments or subscriptions" /> Payments or subscriptions</label>
              <label><input type="checkbox" name="complexity" value="Real-time chat or live updates" /> Real-time chat or live updates</label>
              <label><input type="checkbox" name="complexity" value="Sensitive personal or financial data" /> Sensitive personal or financial data</label>
              <label><input type="checkbox" name="complexity" value="Multiple roles or admin permissions" /> Multiple roles or admin permissions</label>
              <label><input type="checkbox" name="complexity" value="AI-generated decisions or content" /> AI-generated decisions or content</label>
            </div>
          </fieldset>
          <div class="field">
            <label for="validationMethod"><span>Best available first test</span></label>
            <select id="validationMethod" name="validationMethod" required>
              <option value="">Choose one</option>
              <option value="interviews">User interviews</option>
              <option value="prototype">Clickable prototype</option>
              <option value="manual">Manual or concierge test</option>
              <option value="waitlist">Landing page or waitlist</option>
              <option value="unsure">Not sure yet</option>
            </select>
          </div>
          <button class="quiet-button" type="submit">Generate the brief</button>
        </form>
        <section aria-labelledby="result-title" aria-live="polite">
          <p class="kicker">First test <span id="resultState">Waiting</span></p>
          <div id="scopeEmpty"><p>The smaller scope, the risks and the next test will show up here.</p></div>
          <div id="scopeContent" hidden>
            <h2 id="result-title">The brief</h2>
            <h3>Core assumption</h3>
            <p id="coreAssumption"></p>
            <h3>Keep in the first test</h3>
            <ol id="keepFeatures"></ol>
            <h3>Move to later</h3>
            <ul id="laterFeatures"></ul>
            <h3>Complexity to prove necessary</h3>
            <ul id="riskFlags"></ul>
            <h3>Recommended next test</h3>
            <p id="nextTest"></p>
            <p class="heuristic" id="scoreNote"></p>
            <p class="actions">
              <button class="quiet-button" type="button" id="copyBrief">Copy brief</button>
              <button class="quiet-button" type="button" id="emailBrief">Email this brief</button>
            </p>
            <p class="form-status" id="scopeStatus" aria-live="polite"></p>
          </div>
        </section>
      </div>
      <section class="section" aria-labelledby="read">
        <h2 id="read">How to read the result</h2>
        <h3>One person</h3>
        <p>“Everyone” can’t tell you if the problem is real.</p>
        <h3>One outcome</h3>
        <p>The first version should move one outcome.</p>
        <h3>Earn the complicated parts</h3>
        <p>Accounts, payments, live data and AI belong in version one only if the test needs them.</p>
        <p>If you want another person to read the brief, email it. I don’t sell app builds.</p>
      </section>
""",
        },
        {
            "path": "contact/index.html",
            "url": "/contact/",
            "title": "Contact | TechGnomo",
            "description": "Email Fabio D’Anna at gnomocode@gmail.com. No form service and no tracker.",
            "section": "contact",
            "body": """
      <p class="kicker">TechGnomo</p>
      <h1>Email Fabio.</h1>
      <p class="lede">gnomocode@gmail.com is the contact. There is no form on a server and no tracker on this page.</p>
      <p class="email-plate"><a href="mailto:gnomocode@gmail.com">gnomocode@gmail.com</a></p>
      <p class="actions">
        <a href="mailto:gnomocode@gmail.com?subject=Junior%20role%20via%20TechGnomo">About a role</a>
        <a href="mailto:gnomocode@gmail.com?subject=Studio%20job%20via%20TechGnomo">A studio job</a>
        <a href="mailto:gnomocode@gmail.com?subject=A%20TechGnomo%20product">A question about a product</a>
      </p>
      <h2>Also public</h2>
      <ul>
        <li><a href="https://github.com/TechGnomo">github.com/TechGnomo</a></li>
        <li><a href="https://www.linkedin.com/in/fabio-d-anna-5083b5378/">LinkedIn</a></li>
      </ul>
      <p>I don’t list a phone number or a home address. Brisbane is the city.</p>
      <p><a href="/privacy/">Privacy</a></p>
""",
        },
        {
            "path": "privacy/index.html",
            "url": "/privacy/",
            "title": "Privacy | TechGnomo",
            "description": "TechGnomo is a static website. No analytics and no accounts. What is and isn’t collected.",
            "section": "",
            "body": """
      <p class="kicker">26 September 2026</p>
      <h1>Privacy</h1>
      <p class="lede">This is a static website. I don’t run analytics, I don’t set a marketing cookie, and I don’t ask you to create an account.</p>
      <h2>What the pages do</h2>
      <ul class="measure">
        <li>Reading a page does not send me your name or your email.</li>
        <li>The scope checker and the pay-cycle sketch calculate in your browser. I don’t receive them unless you email them.</li>
        <li>Email links open your mail app. The message reaches gnomocode@gmail.com only if you send it.</li>
        <li>ClearMoneyPath screenshots on this site are sample data.</li>
      </ul>
      <h2>The host</h2>
      <p class="measure">The site is hosted on GitHub Pages. GitHub may keep ordinary connection logs. I don’t get a copy of those logs, and I don’t use them to market anything.</p>
      <p class="measure">Emails sent via the contact links go to a Gmail inbox (Google, which may store data outside Australia) and are read only by Fabio D’Anna. He doesn’t sell or share them.</p>
      <p class="measure">Questions: <a href="mailto:gnomocode@gmail.com?subject=Privacy">gnomocode@gmail.com</a>.</p>
""",
        },
        {
            "path": "404.html",
            "url": "/404.html",
            "title": "Page not found | TechGnomo",
            "description": "That address isn’t a page on techgnomo.com.",
            "robots": "noindex",
            "section": "",
            "main_class": "page page-narrow error-main",
            "body": """
      <p class="kicker">404</p>
      <h1>This page isn’t in the workshop.</h1>
      <p>The address doesn’t match a TechGnomo page.</p>
      <p class="actions">
        <a href="/">Home</a>
        <a href="/about/">About</a>
        <a href="/news/">News</a>
        <a href="/products/">Products</a>
        <a href="/contact/">Contact</a>
      </p>
""",
        },
    ]


def sitemap(items):
    urls = []
    for spec in items:
        if spec["path"] == "404.html":
            continue
        if str(spec.get("robots", "")).startswith("noindex"):
            continue
        urls.append(
            f"""  <url>\n    <loc>{ORIGIN}{spec["url"]}</loc>\n    <lastmod>2026-09-27</lastmod>\n  </url>"""
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")


def validate():
    allowed_posts = {"BUILDING", "SHIPPING", "UPDATE", "TEASER"}
    slugs = set(products_by_slug())
    for item in products():
        if item.get("status") not in STATUS_LABEL:
            raise SystemExit(f"Unknown product status on {item.get('slug')}: {item.get('status')}")
    for post in load_json("news.json"):
        if post.get("status") and post["status"] not in allowed_posts:
            raise SystemExit(f"Unknown news status on {post.get('id')}: {post.get('status')}")
        for key in ("id", "datetime", "text"):
            if not post.get(key):
                raise SystemExit(f"News post missing {key}: {post.get('id')}")
        product = post.get("product")
        if product and product not in slugs:
            raise SystemExit(f"News post {post['id']} tags unknown product {product}")


def main():
    validate()
    rendered = pages()
    for spec in rendered:
        page(spec)
    sitemap(rendered)
    redirect("clearmoneypath.html", "/products/clearmoneypath/", "ClearMoneyPath")
    redirect("mvp-scope-checker.html", "/lab/scope-checker/", "MVP Scope Checker")
    redirect("fabio/index.html", "/about/", "About")
    release = {"name": "TechGnomo", "release": "v1"}
    (ROOT / "release.json").write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")
    print("wrote release.json")


if __name__ == "__main__":
    main()
