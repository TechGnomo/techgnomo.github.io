#!/usr/bin/env python3
"""Render the static TechGnomo pages. GitHub Pages serves the HTML as-is."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://techgnomo.com"

NAV = [
    ("workshop.html", "Workshop"),
    ("hire.html", "Hire Fabio"),
    ("work-with.html", "For venues"),
    ("lab.html", "Lab"),
    ("contact.html", "Contact"),
]

MARK = """<svg class="mark" viewBox="0 0 32 32" aria-hidden="true" focusable="false"><rect x="1.2" y="1.2" width="29.6" height="29.6" rx="5" fill="none" stroke="currentColor" stroke-width="1.6"/><path fill="currentColor" d="M16 6.2l5.2 8.4H10.8L16 6.2z"/><circle cx="16" cy="18.4" r="3.2"/><path fill="currentColor" d="M11 23.4c1.5-1.7 3.1-2.4 5-2.4s3.5.7 5 2.4c-1.6 1.6-3.2 2.3-5 2.3s-3.4-.7-5-2.3z"/></svg>"""


def status(kind, label):
    return f'<span class="status status-{kind}">{label}</span>'


def nav_html(current):
    links = []
    for href, label in NAV:
        current_attr = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="/{href}"{current_attr}>{label}</a>')
    return "\n        ".join(links)


def footer():
    return f"""
  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <p class="footer-brand">{MARK} TechGnomo</p>
        <p>Fabio D’Anna’s workshop in Brisbane. A person, not a company.</p>
        <p class="footnote">The gnome is a maker’s mark. He stays in the corner on purpose.</p>
      </div>
      <div>
        <nav class="footer-nav" aria-label="Footer">
          <a href="/">Home</a>
          <a href="/workshop.html">Workshop</a>
          <a href="/hire.html">Hire Fabio</a>
          <a href="/work-with.html">For venues</a>
          <a href="/lab.html">Lab</a>
          <a href="/contact.html">Contact</a>
          <a href="/privacy.html">Privacy</a>
          <a href="mailto:gnomocode@gmail.com">gnomocode@gmail.com</a>
          <a href="https://github.com/TechGnomo" rel="noopener noreferrer">GitHub<span class="visually-hidden"> (opens in a new tab)</span></a>
          <a href="https://www.linkedin.com/in/fabio-d-anna-5083b5378/" rel="noopener noreferrer">LinkedIn<span class="visually-hidden"> (opens in a new tab)</span></a>
        </nav>
        <p class="footnote">© 2026 Fabio D’Anna</p>
      </div>
    </div>
  </footer>
"""


def render(page):
    slug = page["slug"]
    title = page["title"]
    description = page["description"]
    canonical = ORIGIN + "/" if slug == "index.html" else f"{ORIGIN}/{slug}"
    robots = page.get("robots", "index, follow, max-image-preview:large")
    nav_current = page.get("nav", slug)
    scripts = "\n    ".join(f'<script src="{src}" defer></script>' for src in page.get("scripts", []))
    extra_json = page.get("jsonld")
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
            "alternateName": "TechGnomo",
            "url": ORIGIN + "/",
            "email": "gnomocode@gmail.com",
        },
    }
    blocks = [graph]
    if extra_json:
        blocks.append(extra_json)
    jsonld = json.dumps(blocks if len(blocks) > 1 else graph, ensure_ascii=False, indent=2)
    if len(blocks) > 1:
        jsonld = json.dumps({"@context": "https://schema.org", "@graph": blocks}, ensure_ascii=False, indent=2)
        # WebPage already has no context when nested; keep @type only by rebuilding.
        graph.pop("@context", None)
        extra = dict(extra_json)
        extra.pop("@context", None)
        jsonld = json.dumps({"@context": "https://schema.org", "@graph": [graph, extra]}, ensure_ascii=False, indent=2)

    doc = f"""<!doctype html>
<html lang="en-AU" class="no-js">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <meta name="description" content="{description}" />
    <meta name="author" content="Fabio D’Anna" />
    <meta name="theme-color" content="#f4efe4" />
    <meta name="color-scheme" content="light" />
    <meta name="robots" content="{robots}" />
    <link rel="canonical" href="{canonical}" />
    <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
    <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png" />
    <link rel="manifest" href="/site.webmanifest" />
    <link rel="preload" href="/assets/fonts/fraunces-600.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="preload" href="/assets/fonts/atkinson-400.woff2" as="font" type="font/woff2" crossorigin />
    <link rel="stylesheet" href="/assets/css/site.css" />
    <meta property="og:type" content="website" />
    <meta property="og:locale" content="en_AU" />
    <meta property="og:site_name" content="TechGnomo" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:image" content="{ORIGIN}/assets/img/og.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />
    <meta name="twitter:image" content="{ORIGIN}/assets/img/og.png" />
    <script>document.documentElement.classList.replace("no-js","js");</script>
    <script type="application/ld+json">
{jsonld}
    </script>
  </head>
  <body>
    <a class="skip-link" href="#main">Skip to content</a>
    <header class="site-header">
      <div class="wrap header-bar">
        <a class="brand" href="/">
          {MARK}
          <span class="brand-text"><span class="brand-name">TechGnomo</span><span class="brand-sub">Fabio D’Anna</span></span>
        </a>
        <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
          <span class="menu-bars" aria-hidden="true"></span>
          <span class="menu-word">Menu</span>
        </button>
        <nav class="site-nav" id="site-nav" aria-label="Primary">
        {nav_html(nav_current)}
        </nav>
      </div>
    </header>
    <main id="main">
{page["body"]}
    </main>
{footer()}
    <script src="/assets/js/nav.js" defer></script>
    {scripts}
  </body>
</html>
"""
    (ROOT / slug).write_text(doc, encoding="utf-8")
    print("wrote", slug)


def pages():
    home_person = {
        "@type": "Person",
        "@id": ORIGIN + "/#fabio",
        "name": "Fabio D’Anna",
        "alternateName": "TechGnomo",
        "url": ORIGIN + "/",
        "email": "gnomocode@gmail.com",
        "image": ORIGIN + "/assets/img/fabio.webp",
        "homeLocation": {
            "@type": "Place",
            "name": "Brisbane",
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
        "description": "Hospitality professional in Brisbane moving into IT. Builds useful software under the name TechGnomo.",
    }
    scope_app = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "MVP Scope Checker",
        "url": ORIGIN + "/mvp-scope-checker.html",
        "description": "A free browser tool that reduces an app idea to a smaller first test and a short brief. Nothing is uploaded.",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Any web browser",
        "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "AUD"},
        "creator": {"@type": "Person", "name": "Fabio D’Anna", "url": ORIGIN + "/"},
    }

    return [
        {
            "slug": "index.html",
            "title": "Fabio D’Anna builds useful software | TechGnomo",
            "description": "Fabio D’Anna, Brisbane. A hospitality professional moving into IT. TechGnomo is his workshop: projects with honest labels, a web résumé, and small jobs for venues.",
            "nav": "",
            "jsonld": home_person,
            "body": f"""
      <section class="hero wrap">
        <p class="kicker">Brisbane, Australia</p>
        <h1>I build useful software for problems I’ve actually had.</h1>
        <p class="lede">I’m Fabio D’Anna. About ten years on hospitality floors, then diplomas in software development and IT networking. TechGnomo is the workshop where that work sits, labelled by how far it has got.</p>
        <p class="measure">I’m looking for a junior developer or IT support role. I also take small, specific jobs for independent cafés and restaurants. One person. Not an agency.</p>
      </section>
      <section class="wrap" aria-labelledby="doors-title">
        <h2 id="doors-title">Three ways in</h2>
        <div class="door-grid three">
          <a class="door" href="/hire.html">
            <p class="kicker">Recruiters and employers</p>
            <p class="door-title">Hire Fabio</p>
            <p>Skills, diplomas, projects, and the hospitality background that comes with them.</p>
            <span class="door-go">Read the résumé</span>
          </a>
          <a class="door" href="/work-with.html">
            <p class="kicker">Cafés, restaurants, bars</p>
            <p class="door-title">Work with TechGnomo</p>
            <p>A one-page website, or a costing and stocktake sheet. A fixed quote after a free 20-minute call.</p>
            <span class="door-go">See the two jobs I take</span>
          </a>
          <a class="door" href="/workshop.html">
            <p class="kicker">If you want to look around</p>
            <p class="door-title">Explore the workshop</p>
            <p>A pay-cycle planner in beta, a restaurant prototype, and a free tool you can use today.</p>
            <span class="door-go">See what’s on the bench</span>
          </a>
        </div>
      </section>
      <section class="section wrap" aria-labelledby="proof-title">
        <div class="section-head">
          <h2 id="proof-title">What you can actually look at</h2>
          <p>If it isn’t ready to open, the label says so. Sample numbers are sample numbers.</p>
        </div>
        <div class="card-grid three">
          <article class="card">
            <div class="card-top"><span class="code">TG–01</span>{status("beta", "Beta")}</div>
            <h3>ClearMoneyPath</h3>
            <p>What is safe to spend until payday, once bills, a debt payment and savings are set aside. Android beta. Not on a public store.</p>
            <div class="card-shot">
              <img src="/assets/img/cmp-home.webp" width="540" height="1169" alt="ClearMoneyPath home screen with sample data: safe to spend, bills due, amount saved and debt left." />
            </div>
            <p class="quiet">Top of the home screen. Sample data.</p>
            <a class="card-link" href="/clearmoneypath.html">Read the project</a>
          </article>
          <article class="card">
            <div class="card-top"><span class="code">TG–02</span>{status("prototype", "Prototype")}</div>
            <h3>GnomoRestaurant</h3>
            <p>Costing, menu prices, suppliers, stocktake, recipes and ordering. Built from venue problems I know. No public screenshots, and no public link.</p>
            <a class="card-link" href="/gnomorestaurant.html">Read what it covers</a>
          </article>
          <article class="card">
            <div class="card-top"><span class="code">TG–03</span>{status("live", "Live")}</div>
            <h3>MVP Scope Checker</h3>
            <p>A free tool in the browser. It cuts an app idea down to a first test and writes a brief. Nothing is uploaded. This is the piece anyone can open.</p>
            <a class="card-link" href="/mvp-scope-checker.html">Open the tool</a>
          </article>
        </div>
      </section>
      <section class="section wrap portrait-block">
        <figure class="portrait">
          <img src="/assets/img/fabio.webp" width="720" height="1003" alt="Portrait of Fabio D’Anna outdoors, wearing a dark shirt." />
          <figcaption>Fabio D’Anna, Brisbane.</figcaption>
        </figure>
        <div>
          <h2>Leave the career. Keep the knowledge.</h2>
          <p>Hospitality taught me service, costs, a roster, and what a Sunday stocktake does to a week. I still use that. I’m not dressing it up as a software career I haven’t had.</p>
          <p>I’m learning AI, automation and cybersecurity. I build with a lot of AI assistance, and I check the result. I don’t sell any of those as a service.</p>
          <p><a href="/hire.html">The résumé is a page, not a PDF.</a> Contact is <a href="mailto:gnomocode@gmail.com">gnomocode@gmail.com</a>.</p>
        </div>
      </section>
""",
        },
        {
            "slug": "workshop.html",
            "title": "Workshop | TechGnomo",
            "description": "ClearMoneyPath (beta), GnomoRestaurant (prototype) and the MVP Scope Checker (live). Honest labels, and links only where there is something to open.",
            "body": f"""
      <section class="wrap">
        <p class="kicker">The bench</p>
        <h1>Three things worth your time.</h1>
        <p class="lede measure">Each one started from a real problem. The label is how far it has got, not how I wish it sounded.</p>
        <ul class="legend" aria-label="Status labels in use">
          <li>{status("prototype", "Prototype")}</li>
          <li>{status("beta", "Beta")}</li>
          <li>{status("live", "Live")}</li>
        </ul>
        <p class="measure quiet">Prototype: parts of it run, and a stranger can’t open it yet. Beta: a real build other people can try, not a public release. Live: you can use it on this site today. The wider set, when I need it, is idea, experiment, alpha, mature and archived.</p>
        <div class="card-grid">
          <article class="card">
            <div class="card-top"><span class="code">TG–01</span>{status("beta", "Beta")}</div>
            <h2>ClearMoneyPath</h2>
            <p>A pay-cycle planner for the stretch between this payday and the next. Bills, debts (snowball or avalanche) and savings come out first. What’s left is the safe-to-spend number.</p>
            <p>Android beta build. Not publicly released. The screens on the project page use sample data.</p>
            <a class="card-link" href="/clearmoneypath.html">Open the project</a>
          </article>
          <article class="card">
            <div class="card-top"><span class="code">TG–02</span>{status("prototype", "Prototype")}</div>
            <h2>GnomoRestaurant</h2>
            <p>Hospitality operations: recipe and plate costing, menu pricing, suppliers, stocktake and ordering. The thing I wanted on the floor, started as software.</p>
            <p>There is no public screenshot. The project page describes the scope without inventing a picture.</p>
            <a class="card-link" href="/gnomorestaurant.html">Open the project</a>
          </article>
          <article class="card">
            <div class="card-top"><span class="code">TG–03</span>{status("live", "Live")}</div>
            <h2>MVP Scope Checker</h2>
            <p>The strongest public proof, because you can run it. It is a small heuristic, not a study. It lives in the lab.</p>
            <a class="card-link" href="/mvp-scope-checker.html">Use the checker</a>
          </article>
        </div>
      </section>
""",
        },
        {
            "slug": "clearmoneypath.html",
            "nav": "workshop.html",
            "title": "ClearMoneyPath, beta | TechGnomo",
            "description": "ClearMoneyPath is a pay-cycle planner: safe to spend until payday, with bills, debts and savings. Android beta, not publicly released. Screens use sample data.",
            "scripts": ["/assets/js/spend-sketch.js"],
            "body": f"""
      <article class="wrap">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/workshop.html">Workshop</a> <span aria-hidden="true">/</span> <span aria-current="page">ClearMoneyPath</span></nav>
        <div class="card-top"><span class="code">TG–01</span>{status("beta", "Beta")}</div>
        <h1>Know what is safe to spend until payday.</h1>
        <p class="lede measure">A bank balance is not a plan. ClearMoneyPath works in pay cycles: set aside bills, a debt payment and savings, then see what is actually free to spend.</p>
        <p class="measure">Beta means an Android build that can be tried. It is not a public release, and it is not on Google Play or the App Store. These screens use sample data, not a real person’s money.</p>

        <h2>The problem</h2>
        <p class="measure">Pay doesn’t always land on the first of the month. Bills do not care. If you only look at the balance, rent and a debt payment that fall before the next payday are still sitting in that number, pretending to be spendable.</p>
        <p class="measure">I know that week from hospitality: hours change, the pay changes with them, and the bills do not. ClearMoneyPath is the planner I wanted for that stretch.</p>

        <h2>Screens with sample data</h2>
        <div class="shot-grid">
          <figure class="shot">
            <img src="/assets/img/cmp-home.webp" width="540" height="1169" alt="ClearMoneyPath home screen with sample data. Safe to spend $1,292.23, bills due $458, saved $2,540, debt left $8,420." />
            <figcaption>Home. Safe to spend, bills due, savings and debt left. Sample data.</figcaption>
          </figure>
          <figure class="shot">
            <img src="/assets/img/cmp-money.webp" width="540" height="1169" alt="ClearMoneyPath money screen with sample data, listing income, expenses, bills and savings." />
            <figcaption>Money in and out. Sample data.</figcaption>
          </figure>
          <figure class="shot">
            <img src="/assets/img/cmp-debts.webp" width="540" height="1169" alt="ClearMoneyPath debts screen with sample data, showing snowball and avalanche and a short debt list." />
            <figcaption>Debts, with snowball or avalanche. Sample data.</figcaption>
          </figure>
          <figure class="shot">
            <img src="/assets/img/cmp-plan.webp" width="540" height="1169" alt="ClearMoneyPath payday plan with sample data: bills, savings and spending checked against safe to spend." />
            <figcaption>The payday plan. Sample data.</figcaption>
          </figure>
        </div>

        <h2>What this beta does</h2>
        <ul class="measure">
          <li>Shows a safe-to-spend figure for the current pay cycle, and the next payday.</li>
          <li>Records money in, bills, spending and savings.</li>
          <li>Tracks debts with a minimum, a rate and a payoff estimate, and lets you switch between snowball and avalanche.</li>
          <li>Lays out the cycle as a short plan: bills covered, savings set aside, spending inside the safe amount.</li>
        </ul>
        <p class="measure">Built with React Native, Expo and Firebase. I use AI assistance heavily while building. I decide the pay-cycle model, what a bill or a debt has to do, and whether a screen is telling the truth. Generated code still needs checking, especially around dates and money. The repository is not public yet, so that split is not something you can read line by line. I’m happy to walk through it.</p>

        <h2>Try the idea on this page</h2>
        <p class="measure">This box is a sketch, not the app. It only does the subtraction. The numbers stay in your browser.</p>
        <form class="sketch" id="spend-sketch">
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
          <p class="sketch-result" aria-live="polite"><span id="safe-label">Safe to spend</span> <strong id="safe-amount">$990.00</strong></p>
          <p class="help">Sample figures. Change them. If the bills and payments are bigger than the pay, it says you’re short, instead of pretending the number is zero.</p>
        </form>

        <h2>What it is not</h2>
        <ul class="measure">
          <li>Not financial advice. It doesn’t suggest loans, cards or other products. Snowball and avalanche are methods you choose.</li>
          <li>Not a public app yet. Don’t look for it on a store.</li>
          <li>Not a picture of a customer. Every figure on this page is sample data.</li>
        </ul>
        <p class="measure"><a href="/workshop.html">Back to the workshop</a> · <a href="/hire.html">Hiring? The résumé is here.</a></p>
      </article>
""",
        },
        {
            "slug": "gnomorestaurant.html",
            "nav": "workshop.html",
            "title": "GnomoRestaurant, prototype | TechGnomo",
            "description": "GnomoRestaurant is a prototype for venue costing, menu pricing, suppliers, stocktake, recipes and ordering. No public screenshots and no public build.",
            "body": f"""
      <article class="wrap">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/workshop.html">Workshop</a> <span aria-hidden="true">/</span> <span aria-current="page">GnomoRestaurant</span></nav>
        <div class="card-top"><span class="code">TG–02</span>{status("prototype", "Prototype")}</div>
        <h1>The tool I wanted on the floor.</h1>
        <p class="lede measure">GnomoRestaurant is a prototype for the unglamorous part of a venue: what a plate costs, what to charge, who supplies it, what’s in the fridge, and what to order next.</p>
        <p class="measure">Prototype means parts of it run on my machine. There is no public build, so there is no public screenshot. I’m not going to draw a fake one.</p>

        <h2>The problem, in a venue’s words</h2>
        <ul class="measure">
          <li>Stocktake eats Sunday.</li>
          <li>Plate cost is a guess once a supplier puts prices up.</li>
          <li>Ordering lives in someone’s head.</li>
          <li>The menu price and the recipe have drifted apart.</li>
        </ul>
        <p class="measure">I didn’t read that in a brief. It’s the work: about ten years in hospitality, including restaurant management, drink-list costing and talking to suppliers.</p>

        <h2>What the prototype covers</h2>
        <p class="measure">This is the scope. It is not a picture of the interface.</p>
        <ul class="measure">
          <li>Recipes, and a plate cost that moves when a supplier price moves.</li>
          <li>Menu pricing against that cost.</li>
          <li>A supplier list.</li>
          <li>Stocktake.</li>
          <li>Ordering.</li>
        </ul>

        <div class="note">
          <h2>What you can’t click</h2>
          <p>No store listing, no public repository, no screenshots. If you’re hiring and the domain matters, email me and I’ll show you the build I actually have. I won’t send a mock and call it the product.</p>
          <p><a href="mailto:gnomocode@gmail.com?subject=GnomoRestaurant%20walkthrough">gnomocode@gmail.com</a></p>
        </div>
        <p class="measure">It is not client work. Nobody has paid for it, and I don’t claim a venue is running it.</p>
        <p><a href="/workshop.html">Back to the workshop</a> · <a href="/work-with.html">Small jobs for venues, which I can do now</a></p>
      </article>
""",
        },
        {
            "slug": "hire.html",
            "title": "Hire Fabio D’Anna | TechGnomo",
            "description": "Web résumé for Fabio D’Anna, Brisbane. Junior developer and IT support. Skills with honest levels, diplomas, projects and hospitality experience. Email only.",
            "body": f"""
      <article class="wrap">
        <p class="kicker">Open to junior roles</p>
        <h1>Fabio D’Anna</h1>
        <p class="lede measure">Hospitality professional moving into IT. Junior software developer, junior web developer, or IT support. Brisbane, or remote within Australia.</p>
        <div class="portrait-block">
          <figure class="portrait">
            <img src="/assets/img/fabio.webp" width="720" height="1003" alt="Portrait of Fabio D’Anna outdoors, wearing a dark shirt." />
            <figcaption>Brisbane. Email is the contact. No phone number and no street address on this page.</figcaption>
          </figure>
          <div>
            <p>I build useful software and I can show the work: a pay-cycle app in Android beta, a hospitality prototype, a live browser tool, and this site.</p>
            <p>I use AI assistance as part of building. I decide what the software should do, and I check it. I’m still learning AI, automation and cybersecurity, and those are labelled as learning below.</p>
            <div class="button-row">
              <a class="button" href="mailto:gnomocode@gmail.com?subject=Junior%20role%20via%20TechGnomo">Email about a role</a>
              <a class="button button-quiet" href="/workshop.html">See the work</a>
            </div>
            <p>gnomocode@gmail.com · <a href="https://github.com/TechGnomo" rel="noopener noreferrer">GitHub<span class="visually-hidden"> (opens in a new tab)</span></a> · <a href="https://www.linkedin.com/in/fabio-d-anna-5083b5378/" rel="noopener noreferrer">LinkedIn<span class="visually-hidden"> (opens in a new tab)</span></a></p>
          </div>
        </div>

        <section class="section" aria-labelledby="skills-title">
          <h2 id="skills-title">Skills, with an honest level</h2>
          <ul class="skill-list">
            <li>
              <h3>HTML, CSS and accessible pages</h3>
              <p class="level">Working</p>
              <p>This site. Semantic pages, a shared type and colour system, keyboard access, and a layout that holds from a phone to a desktop.</p>
            </li>
            <li>
              <h3>JavaScript</h3>
              <p class="level">Working, on small tools</p>
              <p>The MVP Scope Checker runs entirely in the browser: form, score, brief, copy. No framework.</p>
            </li>
            <li>
              <h3>React Native and Expo</h3>
              <p class="level">In use, still learning</p>
              <p>ClearMoneyPath, the Android beta. I can walk through it. I won’t call myself senior at it.</p>
            </li>
            <li>
              <h3>Firebase</h3>
              <p class="level">In use, still learning</p>
              <p>Used on ClearMoneyPath. Same limit as above: real use, not mastery.</p>
            </li>
            <li>
              <h3>Java</h3>
              <p class="level">Diploma foundation</p>
              <p>Programming fundamentals and object-oriented work from the software development diploma. Not a language I use every week.</p>
            </li>
            <li>
              <h3>C++</h3>
              <p class="level">Diploma foundation</p>
              <p>Same as Java: studied, not a daily tool.</p>
            </li>
            <li>
              <h3>IT networking and support</h3>
              <p class="level">Diploma foundation</p>
              <p>Systems, networking fundamentals, and working a problem through with a person. Enough for junior IT support. Not a security practice.</p>
            </li>
            <li>
              <h3>AI-assisted development</h3>
              <p class="level">Daily method, still learning the limits</p>
              <p>I use it to build, then I decide what to keep and I test the result. Happy to show where I overrode it.</p>
            </li>
            <li>
              <h3>Automation</h3>
              <p class="level">Currently learning</p>
              <p>Not a service I sell.</p>
            </li>
            <li>
              <h3>Cybersecurity</h3>
              <p class="level">Currently learning</p>
              <p>Not a service I sell, and not a skill I’m claiming.</p>
            </li>
            <li>
              <h3>Hospitality operations</h3>
              <p class="level">About ten years</p>
              <p>Floor, bar and restaurant management. Service, costs, suppliers, and running a shift. This is the deep skill. Software is the newer one.</p>
            </li>
          </ul>
        </section>

        <section class="section" aria-labelledby="study-title">
          <h2 id="study-title">Diplomas</h2>
          <ul>
            <li>Diploma of Software Development. Completed.</li>
            <li>Diploma of IT Networking and Telecommunications. Completed.</li>
          </ul>
          <p class="measure quiet">Both completed. Ask if you need the provider and the year; I’ll send them with the certificates.</p>
        </section>

        <section class="section" aria-labelledby="projects-title">
          <h2 id="projects-title">Projects</h2>
          <ul>
            <li><a href="/clearmoneypath.html">ClearMoneyPath</a> — beta. Pay-cycle planner. React Native, Expo, Firebase. Android beta, sample-data screens on the site.</li>
            <li><a href="/gnomorestaurant.html">GnomoRestaurant</a> — prototype. Venue costing, pricing, suppliers, stocktake, ordering. No public build yet.</li>
            <li><a href="/mvp-scope-checker.html">MVP Scope Checker</a> — live. A browser tool on this site. HTML, CSS and JavaScript.</li>
            <li>This website — live. The pages you’re on.</li>
          </ul>
        </section>

        <section class="section" aria-labelledby="floor-title">
          <h2 id="floor-title">Hospitality, as operations</h2>
          <p class="measure">I progressed through front-of-house, bar and management. The useful parts for a junior tech role are not “I can carry plates”. They’re running a service when it gets busy, noticing when a cost has drifted, explaining a problem to someone who didn’t cause it, and keeping a standard when the room is full.</p>
          <p class="measure">I don’t publish a street address, a phone number, or a PDF of this résumé.</p>
        </section>
      </article>
""",
        },
        {
            "slug": "work-with.html",
            "title": "Small jobs for venues | TechGnomo",
            "description": "Fabio D’Anna takes two small jobs for independent cafés and restaurants: a one-page website, or a costing and stocktake spreadsheet. Indicative prices in Australian dollars.",
            "body": f"""
      <article class="wrap">
        <p class="kicker">Brisbane · independent venues</p>
        <h1>Small, specific jobs. Not a studio menu.</h1>
        <p class="lede measure">I’m Fabio. About ten years on hospitality floors, and I build the straightforward web and spreadsheet fixes a venue actually asks for. Two offers. A fixed quote after a free 20-minute call.</p>

        <h2>Problems I can take off the list</h2>
        <ul class="measure">
          <li>People message to ask if you’re open, or the menu online is the old one.</li>
          <li>You don’t know the plate cost since the supplier put prices up.</li>
          <li>Stocktake eats Sunday, and the order lives in someone’s head.</li>
        </ul>

        <div class="offer-grid">
          <article class="offer">
            <h2>A venue page, done properly</h2>
            <p>One fast page for an independent café, restaurant or bar: hours, where you are, the current menu, and links to the booking or ordering you already use.</p>
            <p class="price">Typically A$600–1,200</p>
            <p>Fixed quote after a free 20-minute call. Half to start, half when it goes live.</p>
            <h3>What you get</h3>
            <ul>
              <li>A single mobile-first page.</li>
              <li>Hours, location, menu (as HTML, or a PDF or sheet you can swap), and your existing booking or order links.</li>
              <li>Basic page title and description, so search and link previews have the right name.</li>
              <li>A check of the obvious Google Business bits: hours, menu link, website link.</li>
              <li>You own the domain and the hosting account.</li>
              <li>A one-page note on how to change the simple things, and two rounds of corrections.</li>
            </ul>
            <h3>Not included</h3>
            <ul>
              <li>Online ordering, payments, or a shop.</li>
              <li>A photo shoot. You supply the pictures.</li>
              <li>A weekly menu rewrite. That’s a separate, small update fee, agreed first.</li>
              <li>An SEO retainer.</li>
            </ul>
          </article>
          <article class="offer">
            <h2>Fix the sheet</h2>
            <p>One spreadsheet, in your Google account, for a job the floor already does badly on paper.</p>
            <p class="price">Typically A$250–600</p>
            <p>One sheet per job. Or A$45–60 an hour to tidy a sheet you already have, with a cap written on the quote.</p>
            <h3>Pick one</h3>
            <ul>
              <li>Recipe and plate cost: change a supplier price, the dishes move, and a target margin is flagged.</li>
              <li>A par-level order sheet per supplier.</li>
              <li>A stocktake count sheet that works on a phone.</li>
            </ul>
            <h3>What you get</h3>
            <ul>
              <li>The sheet, in your account.</li>
              <li>A 30-minute handover.</li>
              <li>Two weeks of fixes after handover.</li>
            </ul>
            <p>This is not a substitute for a full inventory system. If you already run stock in your till, I’ll say so on the call and we won’t build a second one for the sake of it.</p>
          </article>
        </div>

        <section class="section" aria-labelledby="how-title">
          <h2 id="how-title">How it works</h2>
          <ol class="steps measure">
            <li>A free 20-minute call. You tell me what’s messy. I tell you if it’s one of these two jobs.</li>
            <li>A fixed quote: price, what’s in, what’s out, and how long I expect. No surprise day-rate at the end.</li>
            <li>I build it and show you once while there’s still time to correct me.</li>
            <li>Handover. You own the files and the accounts. I leave the short note on how to update it.</li>
          </ol>
          <p class="measure">I still work in hospitality, so I won’t book over your service, and I won’t promise overnight.</p>
        </section>

        <section class="section" aria-labelledby="honest-title">
          <div class="note">
            <h2 id="honest-title">Early days, said plainly</h2>
            <p>I haven’t done paid client work under TechGnomo yet. The first one or two jobs can be at an introductory price, written on the quote, in exchange for permission to show the work and for honest feedback.</p>
            <p>I won’t invent a testimonial, a logo, or a “trusted by” line. If you later agree in writing, I can quote what you actually said. Not a polished version of it.</p>
          </div>
        </section>

        <section class="section" aria-labelledby="dont-title">
          <h2 id="dont-title">What I don’t do</h2>
          <p class="measure">Custom mobile apps, online shops, anything that takes card payments, SEO retainers, “AI automation”, cybersecurity, and storing your customers’ personal data beyond a link to email or a booking tool you already use.</p>
        </section>

        <section class="section" aria-labelledby="faq-title">
          <h2 id="faq-title">Questions that come up</h2>
          <div class="faq">
            <details>
              <summary>Do I own the work?</summary>
              <p>Yes. You own the files and the words and photos you supplied. The domain and hosting stay in your name.</p>
            </details>
            <details>
              <summary>What if we need a change later?</summary>
              <p>Two rounds are in the original quote. After that, menu or hours updates are a small fee we agree before I touch it. I don’t want a page that quietly becomes an unpaid job.</p>
            </details>
            <details>
              <summary>How does payment work?</summary>
              <p>Half when we start, half when I hand it over. Both amounts are on the quote.</p>
            </details>
            <details>
              <summary>Can you work around service?</summary>
              <p>Yes. I’m not going to call during a Friday night. Say the hours that are actually free.</p>
            </details>
            <details>
              <summary>Do you have an ABN?</summary>
              <p>Ask on the call if you need one on the invoice. I won’t print a number here that I haven’t put on the quote.</p>
            </details>
          </div>
        </section>

        <section class="section" aria-labelledby="ask-title">
          <h2 id="ask-title">Start with the problem</h2>
          <p class="measure">A few lines is enough: what the venue is, what’s broken, and when you’re free for 20 minutes.</p>
          <div class="button-row">
            <a class="button" href="mailto:gnomocode@gmail.com?subject=Venue%20job%20via%20TechGnomo">Email gnomocode@gmail.com</a>
          </div>
          <p class="quiet">If the button doesn’t open a mail app, copy the address. I don’t put a contact form on a server.</p>
        </section>
      </article>
""",
        },
        {
            "slug": "lab.html",
            "title": "Lab | TechGnomo",
            "description": "The TechGnomo lab: the free MVP Scope Checker, and a plain note on what Fabio is learning — AI, automation and cybersecurity.",
            "body": f"""
      <section class="wrap">
        <p class="kicker">Small, and open</p>
        <h1>The lab</h1>
        <p class="lede measure">Things you can open, and a short account of what I’m studying. Not a blog, and not a list of ideas.</p>
        <article class="card">
          <div class="card-top"><span class="code">TG–03</span>{status("live", "Live")}</div>
          <h2>MVP Scope Checker</h2>
          <p>Paste in a person, a problem and a feature list. It keeps the first three features as the test, parks the rest, flags the complicated parts, and writes a brief you can copy.</p>
          <p>The score is a fixed formula I wrote, starting high and dropping as the idea gets heavier. It is a planning nudge, not evidence that anyone wants the product. Nothing is uploaded.</p>
          <a class="card-link" href="/mvp-scope-checker.html">Open the checker</a>
        </article>

        <section class="section" aria-labelledby="learn-title">
          <h2 id="learn-title">What I’m learning</h2>
          <p class="measure">These are not offers. They’re the subjects I’m in, said at the level I’m actually at.</p>
          <ul class="skill-list">
            <li>
              <h3>AI</h3>
              <p class="level">Using it to build. Learning where it fails.</p>
              <p>I use AI assistance on most of the software I make. The part I’m studying is the failure: invented details, skipped edge cases, and a confident tone when the code is wrong. ClearMoneyPath is where that shows up, around dates and money.</p>
            </li>
            <li>
              <h3>Automation</h3>
              <p class="level">Currently learning</p>
              <p>How to take a repeated admin job — a price list, an order, a count — and make the dull part smaller without hiding the decision. The spreadsheet offer on the venues page is the honest version of this. I’m not selling an automation platform.</p>
            </li>
            <li>
              <h3>Cybersecurity</h3>
              <p class="level">Currently learning</p>
              <p>Foundations, slowly, from the networking diploma outward. I am not offering security work, and I won’t describe myself as someone who tests other people’s systems.</p>
            </li>
          </ul>
        </section>
      </section>
""",
        },
        {
            "slug": "mvp-scope-checker.html",
            "nav": "lab.html",
            "title": "MVP Scope Checker | TechGnomo",
            "description": "A free browser tool from TechGnomo. Cut an app idea down to a first test and a short brief. Nothing is uploaded.",
            "scripts": ["/assets/js/scope-checker.js"],
            "jsonld": scope_app,
            "body": f"""
      <article class="wrap">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/lab.html">Lab</a> <span aria-hidden="true">/</span> <span aria-current="page">MVP Scope Checker</span></nav>
        <div class="card-top"><span class="code">TG–03</span>{status("live", "Live")}</div>
        <h1>Make the first version smaller.</h1>
        <p class="lede measure">Name the person, the problem and the features. The checker keeps three features in the first test, parks the rest, and writes a brief. The score is a fixed formula, not market research.</p>
        <p class="quiet">Runs in your browser. Nothing is uploaded or stored, unless you choose to email the brief.</p>

        <div class="tool-grid" id="scope-workspace">
          <form class="scope-form" id="scopeForm">
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
              <p class="help" id="features-help">List behaviours, not labels like “dashboard” or “AI”. The first three lines are treated as the core.</p>
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
            <button class="button" type="submit">Generate the brief</button>
          </form>

          <section class="scope-result" aria-labelledby="result-title" aria-live="polite">
            <div class="card-top"><span class="code">First test</span><span id="resultState">Waiting</span></div>
            <div id="scopeEmpty">
              <p>The smaller scope, the risks and the next test will show up here.</p>
            </div>
            <div id="scopeContent" hidden>
              <div class="score-row">
                <strong id="scopeScore">–</strong>
                <div>
                  <p class="quiet">Scope signal out of 100. A nudge, not validation.</p>
                  <h2 id="result-title">Ready to calculate</h2>
                </div>
              </div>
              <div class="output-block">
                <h3>Core assumption</h3>
                <p id="coreAssumption"></p>
              </div>
              <div class="output-block">
                <h3>Keep in the first test</h3>
                <ol id="keepFeatures"></ol>
              </div>
              <div class="output-block">
                <h3>Move to later</h3>
                <ul id="laterFeatures"></ul>
              </div>
              <div class="output-block">
                <h3>Complexity to prove necessary</h3>
                <ul id="riskFlags"></ul>
              </div>
              <div class="output-block">
                <h3>Recommended next test</h3>
                <p id="nextTest"></p>
              </div>
              <div class="button-row">
                <button class="button" type="button" id="copyBrief">Copy brief</button>
                <button class="button button-quiet" type="button" id="emailBrief">Email this brief</button>
              </div>
              <p class="form-status" id="scopeStatus" aria-live="polite"></p>
            </div>
          </section>
        </div>

        <section class="section" aria-labelledby="how-title">
          <h2 id="how-title">How to read the result</h2>
          <div class="edu-grid">
            <article>
              <h3>One person</h3>
              <p>“Everyone” can’t tell you if the problem is real. A named first user can.</p>
            </article>
            <article>
              <h3>One outcome</h3>
              <p>The first version should move one outcome. It is not a small copy of the whole idea.</p>
            </article>
            <article>
              <h3>Earn the complicated parts</h3>
              <p>Accounts, payments, live data and AI can be necessary. They should be in version one because the test needs them, not because finished products have them.</p>
            </article>
          </div>
          <p class="measure">If you want another person to read the brief, email it. I won’t turn that email into a pitch for a large app build. I don’t sell app builds.</p>
          <p><a href="/contact.html">Contact</a> · <a href="/lab.html">Back to the lab</a></p>
        </section>
      </article>
""",
        },
        {
            "slug": "contact.html",
            "title": "Contact Fabio D’Anna | TechGnomo",
            "description": "Email Fabio D’Anna at gnomocode@gmail.com about a junior role, a venue job, or the work. No form service and no tracker.",
            "body": """
      <section class="wrap">
        <p class="kicker">One door</p>
        <h1>Email me.</h1>
        <p class="lede measure">gnomocode@gmail.com is the contact. There is no form on a server, no booking widget, and no tracker on this page. If a button doesn’t open a mail app, copy the address.</p>
        <p class="email-plate"><a href="mailto:gnomocode@gmail.com">gnomocode@gmail.com</a></p>
        <div class="button-row">
          <a class="button" href="mailto:gnomocode@gmail.com?subject=Junior%20role%20via%20TechGnomo">About a role</a>
          <a class="button button-quiet" href="mailto:gnomocode@gmail.com?subject=Venue%20job%20via%20TechGnomo">A venue job</a>
          <a class="button button-quiet" href="mailto:gnomocode@gmail.com?subject=Question%20via%20TechGnomo">A question about the work</a>
        </div>
        <h2>Also public</h2>
        <ul>
          <li><a href="https://github.com/TechGnomo" rel="noopener noreferrer">github.com/TechGnomo<span class="visually-hidden"> (opens in a new tab)</span></a></li>
          <li><a href="https://www.linkedin.com/in/fabio-d-anna-5083b5378/" rel="noopener noreferrer">LinkedIn<span class="visually-hidden"> (opens in a new tab)</span></a></li>
        </ul>
        <p class="measure">I don’t list a phone number or a home address. Brisbane is the city.</p>
        <p><a href="/privacy.html">Privacy note</a></p>
      </section>
""",
        },
        {
            "slug": "privacy.html",
            "title": "Privacy | TechGnomo",
            "description": "TechGnomo is a static website. No analytics, no accounts, and no contact form on a server. What is and isn’t collected.",
            "nav": "",
            "body": """
      <article class="wrap">
        <p class="kicker">26 September 2026</p>
        <h1>Privacy, in short.</h1>
        <p class="lede measure">This is a static website. I don’t run analytics, I don’t set a marketing cookie, and I don’t ask you to create an account.</p>
        <h2>What the pages do</h2>
        <ul class="measure">
          <li>Reading a page does not send me your name or your email.</li>
          <li>The MVP Scope Checker and the safe-to-spend sketch calculate in your browser. I don’t receive the numbers or the brief unless you email them.</li>
          <li>Email links open whatever mail app you use. The message reaches gnomocode@gmail.com only if you send it. I then have what you chose to write, and I use it to reply.</li>
          <li>ClearMoneyPath screenshots on this site are sample data, not a customer’s finances.</li>
        </ul>
        <h2>The host</h2>
        <p class="measure">The site is hosted on GitHub Pages. GitHub may keep ordinary connection logs, such as an IP address and the page requested. I don’t get a copy of those logs, and I don’t use them to market anything. GitHub’s own privacy notice covers that hosting.</p>
        <h2>What I don’t add</h2>
        <p class="measure">No third-party analytics, no advertising tags, no embedded chat, and no contact-form company in the middle.</p>
        <p class="measure">Questions: <a href="mailto:gnomocode@gmail.com?subject=Privacy%20question">gnomocode@gmail.com</a>.</p>
      </article>
""",
        },
        {
            "slug": "404.html",
            "title": "Page not found | TechGnomo",
            "description": "That address isn’t a page on techgnomo.com.",
            "robots": "noindex",
            "nav": "",
            "body": """
      <section class="wrap error-main">
        <p class="kicker">404</p>
        <h1>This page isn’t in the workshop.</h1>
        <p class="measure">The address doesn’t match a page on techgnomo.com. The old portfolio and the résumé PDF aren’t served from here.</p>
        <div class="button-row">
          <a class="button" href="/">Home</a>
          <a class="button button-quiet" href="/workshop.html">Workshop</a>
          <a class="button button-quiet" href="/hire.html">Hire Fabio</a>
          <a class="button button-quiet" href="/contact.html">Contact</a>
        </div>
      </section>
""",
        },
    ]


def sitemap(slugs):
    urls = []
    for slug in slugs:
        if slug == "404.html":
            continue
        loc = ORIGIN + "/" if slug == "index.html" else f"{ORIGIN}/{slug}"
        urls.append(
            f"""  <url>
    <loc>{loc}</loc>
    <lastmod>2026-09-26</lastmod>
  </url>"""
        )
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
""" + "\n".join(urls) + "\n</urlset>\n"
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")


def main():
    rendered = pages()
    for page in rendered:
        render(page)
    sitemap([p["slug"] for p in rendered])


if __name__ == "__main__":
    main()
