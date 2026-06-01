"""
Generates all inner HTML pages for the WVCAC local site.
Run: python3 build_pages.py
"""

NAV_LINKS = [
    ("HOME",            "index.html",                  []),
    ("ANNUAL REPORTS",  "annual-reports.html",         []),
    ("HEAD START",      "head-start.html",             [
        ("Head Start Centers",       "head-start-centers.html"),
        ("EHS Policy Council",       "head-start-ehs-policy-council.html"),
        ("Enrollment Application",   "enrollment-application.html"),
    ]),
    ("SERVICES",        "services.html",               [
        ("Transit",          "transit.html"),
        ("Weatherization",   "weatherization.html"),
        ("Housing",          "housing.html"),
    ]),
    ("BOARD",           "board-of-directors.html",     []),
    ("AGENCY FORMS",    "agency-forms.html",           []),
    ("CAREERS",         "job-openings.html",           []),
    ("STAFF",           "staff.html",                  []),
    ("ABOUT",           "about-us.html",               []),
]

SHARED_CSS = """
    :root{--navy:#1a4f8a;--navy-d:#133a66;--gold:#f59e0b;--bg:#f4f6fa;--white:#ffffff;--text:#1a1a2e;--muted:#4a5568;--border:#d1d9e6;--radius:10px;--shadow:0 4px 20px rgba(0,0,0,.10);--nav-h:68px;}
    /* Logo bar */
    .logo-bar{background:var(--white);border-bottom:3px solid var(--gold);padding:1rem 1.5rem;display:flex;align-items:center;justify-content:center;}
    .logo-bar img{height:95px;width:auto;display:block;}
    @media(max-width:600px){.logo-bar img{height:68px;}}
    *,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
    html{scroll-behavior:smooth;}
    body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;}
    img{max-width:100%;display:block;}
    a{color:inherit;text-decoration:none;}
    :focus-visible{outline:3px solid var(--gold);outline-offset:3px;border-radius:4px;}
    .skip-link{position:absolute;top:-100%;left:1rem;background:var(--navy);color:#fff;padding:.5rem 1.1rem;border-radius:0 0 8px 8px;font-weight:700;font-size:1rem;z-index:9999;transition:top .2s;}
    .skip-link:focus{top:0;}
    /* Navbar */
    .navbar{position:sticky;top:0;z-index:100;background:var(--navy);box-shadow:0 2px 12px rgba(0,0,0,.25);height:var(--nav-h);display:flex;align-items:center;}
    .nav-inner{width:100%;max-width:1200px;margin-inline:auto;padding-inline:1.5rem;display:flex;align-items:center;gap:1rem;}
    .nav-menu{list-style:none;display:flex;align-items:center;gap:.1rem;margin-inline:auto;}
    .nav-item{position:relative;}
    .nav-link{display:flex;align-items:center;gap:.3rem;color:rgba(255,255,255,.92);padding:.55rem .85rem;border-radius:6px;font-size:1rem;font-weight:600;letter-spacing:.04em;white-space:nowrap;transition:background .2s,color .2s;cursor:pointer;background:none;border:none;font-family:inherit;}
    .nav-link:hover,.nav-link:focus-visible,.nav-item:hover>.nav-link{background:rgba(255,255,255,.15);color:#fff;}
    .nav-link.active{background:rgba(255,255,255,.22);color:#fff;}
    .nav-link svg{flex-shrink:0;transition:transform .2s;}
    .nav-item:hover>.nav-link svg{transform:rotate(180deg);}
    .dropdown{display:none;position:absolute;top:calc(100% + 6px);left:0;min-width:220px;background:var(--white);border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--shadow);list-style:none;overflow:hidden;z-index:200;}
    .nav-item:hover .dropdown,.nav-item:focus-within .dropdown{display:block;}
    .dropdown a{display:block;padding:.65rem 1.1rem;font-size:1rem;font-weight:500;color:var(--text);transition:background .15s;}
    .dropdown a:hover,.dropdown a:focus-visible{background:#e8f0fb;color:var(--navy);}
    .dropdown-divider{height:1px;background:var(--border);}
    .hamburger{display:none;margin-left:auto;background:none;border:2px solid rgba(255,255,255,.6);border-radius:6px;color:#fff;padding:.4rem .55rem;cursor:pointer;font-size:1.3rem;line-height:1;}
    @media(max-width:899px){
      .nav-menu{display:none;flex-direction:column;align-items:stretch;position:absolute;top:var(--nav-h);left:0;right:0;background:var(--navy-d);padding:1rem 0;gap:0;box-shadow:0 6px 20px rgba(0,0,0,.3);}
      .nav-menu.open{display:flex;}
      .nav-link{border-radius:0;font-size:1rem;padding:.75rem 1.5rem;}
      .dropdown{position:static;box-shadow:none;border:none;border-radius:0;background:rgba(0,0,0,.2);}
      .dropdown a{color:rgba(255,255,255,.85);padding-left:2.5rem;}
      .dropdown a:hover{background:rgba(255,255,255,.1);color:#fff;}
      .nav-item:hover .dropdown{display:none;}
      .nav-item.open .dropdown{display:block;}
      .hamburger{display:flex;align-items:center;}
    }
    /* Page hero banner */
    .page-hero{background:linear-gradient(135deg,var(--navy) 0%,#2563a8 100%);color:#fff;padding:3.5rem 1.5rem 3rem;text-align:center;}
    .page-hero h1{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:900;line-height:1.15;margin-bottom:.5rem;}
    .page-hero p{font-size:1.05rem;color:rgba(255,255,255,.9);max-width:620px;margin-inline:auto;}
    /* Main content */
    .page-body{max-width:1100px;margin-inline:auto;padding:3rem 1.5rem 4rem;}
    .content-card{background:var(--white);border:1px solid var(--border);border-radius:var(--radius);padding:2rem 2.25rem;box-shadow:var(--shadow);margin-bottom:2rem;}
    .content-card h2{font-size:1.3rem;font-weight:800;color:var(--navy);margin-bottom:1rem;padding-bottom:.6rem;border-bottom:3px solid var(--gold);}
    .content-card h3{font-size:1.1rem;font-weight:700;color:var(--navy);margin:1.25rem 0 .5rem;}
    .content-card p{font-size:1rem;color:var(--muted);margin-bottom:.75rem;line-height:1.7;}
    .content-card ul{padding-left:1.4rem;color:var(--muted);font-size:1rem;display:flex;flex-direction:column;gap:.4rem;margin-bottom:.75rem;}
    .content-card li{line-height:1.6;}
    .info-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.5rem;margin-top:1rem;}
    .info-box{background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem 1.5rem;}
    .info-box h3{font-size:1rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;color:var(--navy);margin-bottom:.5rem;}
    .info-box p{font-size:1rem;color:var(--muted);line-height:1.6;}
    .img-block{border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);margin-bottom:1.5rem;}
    .img-block img{width:100%;height:auto;display:block;}
    .two-col{display:grid;grid-template-columns:1fr 1fr;gap:2rem;align-items:start;}
    @media(max-width:700px){.two-col{grid-template-columns:1fr;}}
    .alert{background:#e8f0fb;border-left:4px solid var(--navy);border-radius:0 var(--radius) var(--radius) 0;padding:1rem 1.25rem;font-size:1rem;color:var(--text);margin-bottom:1.5rem;}
    .btn{display:inline-flex;align-items:center;gap:.4rem;padding:.7rem 1.4rem;border-radius:8px;font-size:1rem;font-weight:700;transition:.2s;cursor:pointer;border:none;font-family:inherit;}
    .btn-primary{background:var(--navy);color:#fff;}
    .btn-primary:hover{background:var(--navy-d);}
    /* Footer */
    footer{background:#111827;color:#d1d5db;padding:2.5rem 1.5rem 1.5rem;}
    .footer-inner{max-width:1200px;margin-inline:auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:2rem;margin-bottom:2rem;}
    .footer-col h3{color:#fff;font-size:1rem;font-weight:700;margin-bottom:.75rem;}
    .footer-col ul{list-style:none;display:flex;flex-direction:column;gap:.5rem;}
    .footer-col ul a{font-size:1rem;color:#d1d5db;transition:color .15s;}
    .footer-col ul a:hover{color:#fff;text-decoration:underline;}
    .footer-fb-link{display:inline-flex;align-items:center;gap:.6rem;font-size:1rem;color:#d1d5db;min-height:44px;padding:.25rem 0;transition:color .15s;}
    .footer-fb-link:hover{color:#fff;text-decoration:underline;}
    .footer-fb-link svg{flex-shrink:0;width:28px;height:28px;}
    .footer-bottom{max-width:1200px;margin-inline:auto;border-top:1px solid #374151;padding-top:1.25rem;display:flex;flex-wrap:wrap;gap:.75rem;justify-content:space-between;align-items:center;font-size:1rem;color:#9ca3af;}
"""

NAV_JS = """
    const hamburger=document.getElementById('hamburger');
    const navMenu=document.getElementById('nav-menu');
    hamburger.addEventListener('click',()=>{const o=navMenu.classList.toggle('open');hamburger.setAttribute('aria-expanded',o);});
    document.querySelectorAll('.nav-link[aria-haspopup]').forEach(btn=>{
      btn.addEventListener('click',()=>{if(window.innerWidth<900){const li=btn.closest('.nav-item');li.classList.toggle('open');btn.setAttribute('aria-expanded',li.classList.contains('open'));}});
    });
"""

LOGO_BAR = """
  <div class="logo-bar" role="banner" aria-label="Washita Valley CAC">
    <a href="index.html" aria-label="Go to home page">
      <img
        src="https://static.wixstatic.com/media/bf0d32_f4373b43f45c4ef384f3b734eeb4f77a~mv2.jpg/v1/fill/w_880,h_170,al_c,q_90,enc_avif,quality_auto/WVCAC%202.jpg"
        alt="Washita Valley Community Action Council — Helping People, Changing Lives"
        width="440" height="85"
      />
    </a>
  </div>"""

def nav_html(active_href):
    items_html = ""
    for label, href, children in NAV_LINKS:
        is_active = "active" if href == active_href else ""
        if children:
            dd_id = f"dd-{href.replace('.html','')}"
            dd_items = f'<li><a href="{href}">{label} Overview</a></li><li class="dropdown-divider" role="separator"></li>'
            for child_label, child_href in children:
                dd_items += f'<li><a href="{child_href}">{child_label}</a></li>'
            items_html += f"""
          <li class="nav-item" role="listitem">
            <button class="nav-link {is_active}" aria-haspopup="true" aria-expanded="false" aria-controls="{dd_id}">
              {label}
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>
            </button>
            <ul class="dropdown" id="{dd_id}" role="list">{dd_items}</ul>
          </li>"""
        else:
            items_html += f"""
          <li class="nav-item" role="listitem">
            <a class="nav-link {is_active}" href="{href}">{label}</a>
          </li>"""
    return f"""
  <header role="banner">
    <nav class="navbar" aria-label="Main navigation">
      <div class="nav-inner">
        <button class="hamburger" id="hamburger" aria-controls="nav-menu" aria-expanded="false" aria-label="Open navigation menu">&#9776;</button>
        <ul class="nav-menu" id="nav-menu" role="list">{items_html}
        </ul>
      </div>
    </nav>
  </header>"""

FOOTER_HTML = """
  <footer role="contentinfo">
    <div class="footer-inner">
      <div class="footer-col">
        <h3>Programs</h3>
        <ul>
          <li><a href="head-start.html">Head Start</a></li>
          <li><a href="transit.html">Transit</a></li>
          <li><a href="weatherization.html">Weatherization</a></li>
          <li><a href="housing.html">Housing</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>Organization</h3>
        <ul>
          <li><a href="about-us.html">About Us</a></li>
          <li><a href="board-of-directors.html">Board of Directors</a></li>
          <li><a href="staff.html">Staff</a></li>
          <li><a href="job-openings.html">Job Openings</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>Resources</h3>
        <ul>
          <li><a href="agency-forms.html">Agency Forms</a></li>
          <li><a href="annual-reports.html">Annual Reports</a></li>
          <li><a href="mailto:info@washitavalleycac.com">Contact Us</a></li>
          <li>
            <a class="footer-fb-link" href="https://www.facebook.com/search/top?q=washita%20valley%20community%20action%20council" target="_blank" rel="noopener" aria-label="Visit Washita Valley CAC on Facebook (opens in new tab)">
              <svg viewBox="0 0 24 24" fill="#1877f2" aria-hidden="true"><path d="M24 12.073C24 5.405 18.627 0 12 0S0 5.405 0 12.073C0 18.1 4.388 23.094 10.125 24v-8.437H7.078v-3.49h3.047V9.41c0-3.025 1.792-4.697 4.533-4.697 1.312 0 2.686.235 2.686.235v2.97h-1.513c-1.491 0-1.956.93-1.956 1.886v2.269h3.328l-.532 3.49h-2.796V24C19.612 23.094 24 18.1 24 12.073z"/></svg>
              Facebook
            </a>
          </li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Washita Valley Community Action Council. All rights reserved.</span>
      <span>WCAG 2.1 AA Compliant</span>
    </div>
  </footer>"""

def page(filename, title, description, hero_subtitle, body_html):
    active = filename
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <meta name="description" content="{description}"/>
  <title>{title} — Washita Valley CAC</title>
  <style>{SHARED_CSS}</style>
</head>
<body>
  <a class="skip-link" href="#main">Skip to main content</a>
  {LOGO_BAR}
  {nav_html(active)}
  <section class="page-hero" aria-label="Page header">
    <h1>{title}</h1>
    <p>{hero_subtitle}</p>
  </section>
  <main id="main" class="page-body">
    {body_html}
  </main>
  {FOOTER_HTML}
  <script src="accessibility.js"></script>
  <script>{NAV_JS}</script>
</body>
</html>"""


# ─── Page definitions ────────────────────────────────────────────────

pages = {}

# ABOUT US
pages["about-us.html"] = page(
    "about-us.html", "About Us",
    "Washita Valley Community Action Council — serving Grady and Caddo Counties since 1968.",
    "Private non-profit serving Grady and Caddo Counties since 1968.",
    """
    <style>
      /* About Us custom layout */
      .about-hero {
        position: relative; border-radius: var(--radius); overflow: hidden;
        margin-bottom: 2.5rem; min-height: 280px;
        display: flex; align-items: center; justify-content: center;
      }
      .about-hero-bg {
        position: absolute; inset: 0; width: 100%; height: 100%;
        object-fit: cover; object-position: center top;
      }
      .about-hero::after {
        content: ''; position: absolute; inset: 0;
        background: rgba(30, 50, 40, .55);
      }
      .about-hero-inner {
        position: relative; z-index: 1; padding: 3rem 2.5rem;
        text-align: center; color: #fff; max-width: 820px;
      }
      .about-hero-inner h2 {
        font-size: 1.6rem; font-weight: 300; letter-spacing: .22em;
        text-transform: uppercase; margin-bottom: 1.25rem;
      }
      .about-hero-inner p {
        font-size: .97rem; line-height: 1.8; opacity: .95;
      }
      .about-body { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
      @media(max-width:700px){ .about-body { grid-template-columns: 1fr; } }
      .about-section-title {
        font-size: .8rem; font-weight: 700; letter-spacing: .15em;
        text-transform: uppercase; color: var(--navy);
        text-align: center; margin-bottom: .5rem;
      }
      .about-section-divider {
        width: 32px; height: 2px; background: var(--navy);
        margin: 0 auto 1.1rem;
      }
      .about-section-text { font-size: .92rem; color: var(--muted); text-align: center; line-height: 1.75; }
      /* Contact form */
      .contact-form { display: flex; flex-direction: column; gap: .75rem; }
      .contact-form label { font-size: .82rem; font-weight: 700; color: var(--text); }
      .contact-form input,
      .contact-form textarea {
        width: 100%; border: 1px solid var(--border); border-radius: 6px;
        padding: .55rem .8rem; font-size: .9rem; font-family: inherit;
        background: #fff; color: var(--text); transition: border .2s;
      }
      .contact-form input:focus,
      .contact-form textarea:focus { outline: none; border-color: var(--navy); }
      .contact-form textarea { min-height: 110px; resize: vertical; }
      .contact-form .send-btn {
        align-self: flex-end; background: var(--navy); color: #fff;
        border: none; border-radius: 6px; padding: .55rem 1.6rem;
        font-size: .9rem; font-weight: 700; cursor: pointer;
        font-family: inherit; transition: background .2s;
      }
      .contact-form .send-btn:hover { background: var(--navy-d); }
      /* Contact bar */
      .contact-bar {
        display: grid; grid-template-columns: repeat(3, 1fr);
        gap: 1rem; margin-top: 2rem; text-align: center;
      }
      @media(max-width:600px){ .contact-bar { grid-template-columns: 1fr; } }
      .contact-bar-item { display: flex; flex-direction: column; align-items: center; gap: .5rem; }
      .contact-bar-icon { color: var(--muted); }
      .contact-bar-item p { font-size: .85rem; color: var(--muted); line-height: 1.6; }
      .contact-bar-item a { color: var(--navy); }
    </style>

    <!-- HERO BANNER -->
    <div class="about-hero" role="img" aria-label="Oklahoma landscape — golden grasses representing the Washita Valley region">
      <img class="about-hero-bg"
        src="https://static.wixstatic.com/media/9156348f9b554babaa4d6c009ce2db0f.jpg/v1/fill/w_1400,h_600,al_c,q_85,enc_avif,quality_auto/9156348f9b554babaa4d6c009ce2db0f.jpg"
        alt="" aria-hidden="true" width="1400" height="600" loading="eager"/>
      <div class="about-hero-inner">
        <h2>About Us</h2>
        <p>Washita Valley Community Action Council is a private non-profit corporation, incorporated in 1968 to serve Grady and Caddo Counties. The agency is governed by a twelve member tripartite Board of Directors, with four members representing the low-income sector, four members representing the public sector, and four members representing the private sector. With the low-income representation on the Board, the low-income have a role in the planning, evaluation, and decision making of all agency programs.</p>
      </div>
    </div>

    <!-- TWO-COLUMN BODY -->
    <div class="about-body">

      <!-- LEFT: Vision + Map -->
      <div style="display:flex;flex-direction:column;gap:1.5rem;">
        <div class="content-card" style="text-align:center;">
          <div class="about-section-title">Our Vision</div>
          <div class="about-section-divider" aria-hidden="true"></div>
          <p class="about-section-text">To assist individuals and families in our communities through public and private partnerships to improve the quality of their lives by minimizing the effects of poverty, promoting self-sufficiency and advocating for social change.</p>
        </div>
        <div style="border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);">
          <iframe
            title="Washita Valley CAC — 1000 West Minnesota Ave, Chickasha, OK 73018"
            src="https://maps.google.com/maps?q=1000+W+Minnesota+Ave,+Chickasha,+OK+73018&output=embed"
            width="100%" height="340" style="border:0;display:block;"
            allowfullscreen="" loading="lazy"
            referrerpolicy="no-referrer-when-downgrade">
          </iframe>
        </div>
      </div>

      <!-- RIGHT: Community + Contact Form -->
      <div style="display:flex;flex-direction:column;gap:1.5rem;">
        <div class="content-card" style="text-align:center;">
          <div class="about-section-title">Our Community</div>
          <div class="about-section-divider" aria-hidden="true"></div>
          <p class="about-section-text">Washita Valley Community Action Council provides services for Grady and Caddo Counties.</p>
        </div>
        <div class="content-card">
          <div class="about-section-title" style="text-align:left;margin-bottom:.75rem;">Contact Us</div>
          <form class="contact-form" action="mailto:info@washitavalleycac.com" method="get" enctype="text/plain" aria-label="Contact form">
            <div>
              <label for="contact-name">Name: <span aria-hidden="true">*</span></label>
              <input type="text" id="contact-name" name="name" required autocomplete="name" placeholder=" "/>
            </div>
            <div>
              <label for="contact-email">Email: <span aria-hidden="true">*</span></label>
              <input type="email" id="contact-email" name="email" required autocomplete="email" placeholder=" "/>
            </div>
            <div>
              <label for="contact-message">Message:</label>
              <textarea id="contact-message" name="body" placeholder=" "></textarea>
            </div>
            <button type="submit" class="send-btn">Send</button>
          </form>
        </div>
      </div>
    </div>

    <!-- CONTACT BAR -->
    <div class="contact-bar" role="contentinfo" aria-label="Contact information">
      <div class="contact-bar-item">
        <svg class="contact-bar-icon" width="36" height="36" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12 19.79 19.79 0 0 1 1.62 3.4 2 2 0 0 1 3.6 1.22h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 8.85a16 16 0 0 0 6.07 6.07l.95-.95a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        <p>Tel: (405) 224-5831<br>Fax: (405) 222-4303<br>Operator Assisted Relay 711</p>
      </div>
      <div class="contact-bar-item">
        <svg class="contact-bar-icon" width="36" height="36" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        <p>1000 West Minnesota Ave.<br>Chickasha, OK 73018</p>
      </div>
      <div class="contact-bar-item">
        <svg class="contact-bar-icon" width="36" height="36" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
        <p><a href="mailto:info@washitavalleycac.com">info@washitavalleycac.com</a></p>
      </div>
    </div>"""
)

# ANNUAL REPORTS
pages["annual-reports.html"] = page(
    "annual-reports.html", "Annual Reports",
    "Annual reports from Washita Valley Community Action Council.",
    "Transparency and accountability to our community.",
    """
    <div class="two-col">
      <div>
        <div class="img-block">
          <img
            src="https://static.wixstatic.com/media/bf0d32_6f4edbc18264487eabc018bb6b6dab4a~mv2.gif"
            alt="Illustration of stacked annual report documents and a tablet displaying charts and financial data"
            loading="lazy" width="900" height="234"
            style="background:#f97316;"
          />
        </div>
        <div class="content-card">
          <h2>Request a Printed Copy</h2>
          <p>To request a printed copy of any annual report, contact us at:</p>
          <div class="info-grid">
            <div class="info-box"><h3>Email</h3><p><a href="mailto:info@washitavalleycac.com" style="color:var(--navy);">info@washitavalleycac.com</a></p></div>
            <div class="info-box"><h3>Phone</h3><p>(405) 224-5831</p></div>
          </div>
        </div>
      </div>
      <div>
        <div class="content-card">
          <h2>Download Annual Reports</h2>
          <p>Washita Valley CAC is committed to transparency. Our annual reports provide a full accounting of our programs, outcomes, and financials each year.</p>
          <div style="display:flex;flex-direction:column;gap:1rem;margin-top:1.25rem;">
            <a href="https://www.washitavalleycac.com/_files/ugd/01a535_94e879b931504882af0ca3e03736c0a0.pdf"
               target="_blank" rel="noopener"
               style="display:flex;align-items:center;gap:1rem;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:1rem 1.25rem;color:var(--navy);font-weight:700;transition:.2s;"
               onmouseover="this.style.background='#e8f0fb'" onmouseout="this.style.background='var(--bg)'">
              <span style="font-size:1.75rem;" aria-hidden="true">📄</span>
              <span>
                <span style="display:block;font-size:1rem;">WVCAC Annual Report 2024–2025</span>
                <span style="font-size:1rem;font-weight:400;color:var(--muted);">PDF — Click to open</span>
              </span>
            </a>
            <a href="https://www.washitavalleycac.com/_files/ugd/01a535_0d4df3c7ab334ddbbf0011714ae4c62e.pdf"
               target="_blank" rel="noopener"
               style="display:flex;align-items:center;gap:1rem;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:1rem 1.25rem;color:var(--navy);font-weight:700;transition:.2s;"
               onmouseover="this.style.background='#e8f0fb'" onmouseout="this.style.background='var(--bg)'">
              <span style="font-size:1.75rem;" aria-hidden="true">📄</span>
              <span>
                <span style="display:block;font-size:1rem;">WVCAC Annual Report 2023–2024</span>
                <span style="font-size:1rem;font-weight:400;color:var(--muted);">PDF — Click to open</span>
              </span>
            </a>
            <a href="https://www.washitavalleycac.com/_files/ugd/01a535_fa598653f5b84bf4ad6f3946bc417e51.pdf"
               target="_blank" rel="noopener"
               style="display:flex;align-items:center;gap:1rem;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:1rem 1.25rem;color:var(--navy);font-weight:700;transition:.2s;"
               onmouseover="this.style.background='#e8f0fb'" onmouseout="this.style.background='var(--bg)'">
              <span style="font-size:1.75rem;" aria-hidden="true">📄</span>
              <span>
                <span style="display:block;font-size:1rem;">WVCAC Annual Report 2022–2023</span>
                <span style="font-size:1rem;font-weight:400;color:var(--muted);">PDF — Click to open</span>
              </span>
            </a>
            <a href="annual-report-2020-2021.pdf"
               target="_blank" rel="noopener"
               style="display:flex;align-items:center;gap:1rem;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius);padding:1rem 1.25rem;color:var(--navy);font-weight:700;transition:.2s;"
               onmouseover="this.style.background='#e8f0fb'" onmouseout="this.style.background='var(--bg)'">
              <span style="font-size:1.75rem;" aria-hidden="true">📄</span>
              <span>
                <span style="display:block;font-size:1rem;">WVCAC Annual Report 2020–2021</span>
                <span style="font-size:1rem;font-weight:400;color:var(--muted);">PDF — Click to open</span>
              </span>
            </a>
          </div>
        </div>
      </div>
    </div>"""
)

# HEAD START
pages["head-start.html"] = page(
    "head-start.html", "Head Start",
    "WVCAC Head Start — early childhood education and family support for children ages 0–5.",
    "Inspire and equip children and families to excel today, and soar tomorrow.",
    """
    <div class="content-card">
      <h2>Our Vision</h2>
      <p>Washita Valley Community Action Council Head Start's vision is to provide a premier early childhood program with highly qualified staff that partner with families to ensure school readiness and lifelong success for every child.</p>
    </div>
    <div class="two-col">
      <div class="content-card">
        <h2>Our Philosophy</h2>
        <p>Washita Valley CAC Head Start's philosophy is that parents are the child's first and most important teacher. Parents are encouraged to be active participants in their child's education and development.</p>
      </div>
      <div class="content-card">
        <h2>Content Areas</h2>
        <ul>
          <li>Family &amp; Community Partnerships</li>
          <li>Early Childhood Education</li>
          <li>Health &amp; Nutrition Services</li>
          <li>Disability &amp; Mental Health Services</li>
        </ul>
      </div>
    </div>
    <div class="content-card">
      <h2>Quick Links</h2>
      <div class="info-grid">
        <div class="info-box"><h3>Centers</h3><p><a href="head-start-centers.html" style="color:var(--navy);font-weight:700;">Find a Head Start Center →</a></p></div>
        <div class="info-box"><h3>Policy Council</h3><p><a href="head-start-ehs-policy-council.html" style="color:var(--navy);font-weight:700;">EHS Policy Council →</a></p></div>
        <div class="info-box"><h3>Enrollment</h3><p><a href="enrollment-application.html" style="color:var(--navy);font-weight:700;">Apply for Enrollment →</a></p></div>
      </div>
    </div>"""
)

# HEAD START CENTERS
pages["head-start-centers.html"] = page(
    "head-start-centers.html", "Head Start Centers",
    "Locations for WVCAC Head Start and Early Head Start centers in Anadarko and Chickasha.",
    "Head Start and Early Head Start centers across Grady and Caddo Counties.",
    """
    <div class="content-card">
      <h2>All Centers</h2>
      <p style="margin-bottom:1.25rem;">7 centers serving families across Grady and Caddo Counties. <a href="enrollment-application.html" style="color:var(--navy);font-weight:700;">Enroll your child →</a></p>
      <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;font-size:1rem;">
          <thead>
            <tr style="background:var(--navy);color:#fff;text-align:left;">
              <th style="padding:.65rem 1rem;border-radius:8px 0 0 0;">Center</th>
              <th style="padding:.65rem 1rem;">Address</th>
              <th style="padding:.65rem 1rem;">Phone</th>
              <th style="padding:.65rem 1rem;border-radius:0 8px 0 0;">Staff</th>
            </tr>
          </thead>
          <tbody>
            <tr style="background:#fff;border-bottom:1px solid var(--border);">
              <td style="padding:.75rem 1rem;font-weight:700;color:var(--navy);">Anadarko HS &amp; EHS</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">315 NE 3rd St<br>Anadarko, OK 73005</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">405-247-6745</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">Dir: Renee Hill<br>Advocate: Robin Taylor</td>
            </tr>
            <tr style="background:var(--bg);border-bottom:1px solid var(--border);">
              <td style="padding:.75rem 1rem;font-weight:700;color:var(--navy);">Chickasha HS &amp; EHS</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">1000 W Minnesota Ave<br>Chickasha, OK 73018</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">405-222-0172</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">Dir: Nicole Porter<br>Asst Dir: Savana Rainer</td>
            </tr>
            <tr style="background:#fff;border-bottom:1px solid var(--border);">
              <td style="padding:.75rem 1rem;font-weight:700;color:var(--navy);">Chickasha Head Start</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">1304 S 6th St<br>Chickasha, OK 73018</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">405-224-3471</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">Dir: Malinda Wolfe</td>
            </tr>
            <tr style="background:var(--bg);border-bottom:1px solid var(--border);">
              <td style="padding:.75rem 1rem;font-weight:700;color:var(--navy);">Cyril Head Start</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">Cyril Elementary School<br>103 S 4th St, Cyril, OK 73029</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">580-464-2536</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">Dir: Daisy Burger<br>Advocate: Kristina Gomez</td>
            </tr>
            <tr style="background:#fff;border-bottom:1px solid var(--border);">
              <td style="padding:.75rem 1rem;font-weight:700;color:var(--navy);">Fort Cobb Head Start</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">Caddo Kiowa Tech Center<br>100 Career Tech Rd, Fort Cobb, OK 73038</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">405-643-5314</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">Dir: Carla Worcester</td>
            </tr>
            <tr style="background:var(--bg);border-bottom:1px solid var(--border);">
              <td style="padding:.75rem 1rem;font-weight:700;color:var(--navy);">Fort Cobb Early HS</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">Caddo-Kiowa Vo-Tech<br>100 Career Tech Rd, Fort Cobb, OK 73038</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">405-643-3247 / 3248</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">Dir: Amy Cowan<br>Advocate: Felicia Gallegos</td>
            </tr>
            <tr style="background:#fff;">
              <td style="padding:.75rem 1rem;font-weight:700;color:var(--navy);">Lookeba Head Start</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">Lookeba-Sickles Elementary<br>307 W Sickles Ave, Lookeba, OK 73053</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">405-457-6493</td>
              <td style="padding:.75rem 1rem;color:var(--muted);">Dir: Leticia Rodriguez</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="content-card">
      <h2>Main Office</h2>
      <div class="info-grid">
        <div class="info-box"><h3>Address</h3><p>1000 West Minnesota Ave<br>Chickasha, OK 73018</p></div>
        <div class="info-box"><h3>Phone</h3><p>(405) 224-5831</p></div>
        <div class="info-box"><h3>Email</h3><p><a href="mailto:info@washitavalleycac.com" style="color:var(--navy);">info@washitavalleycac.com</a></p></div>
      </div>
    </div>"""
)

# EHS POLICY COUNCIL
pages["head-start-ehs-policy-council.html"] = page(
    "head-start-ehs-policy-council.html", "Head Start / EHS Policy Council",
    "Head Start and Early Head Start Policy Council — WVCAC parent and community governance body.",
    "Parent and community voice in the Head Start program.",
    """
    <div class="two-col" style="align-items:start;">
      <div>
        <div class="content-card">
          <h2>About the Policy Council</h2>
          <p>The Head Start / Early Head Start Policy Council is a governance body made up of parents and community representatives. It plays a vital role in the planning, operation, and oversight of WVCAC Head Start programs.</p>
          <p>Policy Council members have a say in decisions about program design, staff hiring, and budgeting — ensuring the program serves families the way families need it to.</p>
        </div>
        <div class="content-card">
          <h2>Get Involved</h2>
          <p>If you are a parent or guardian of a Head Start child and would like to get involved with the Policy Council, contact your center director or reach us at:</p>
          <div class="info-grid">
            <div class="info-box"><h3>Phone</h3><p>(405) 224-5831</p></div>
            <div class="info-box"><h3>Email</h3><p><a href="mailto:info@washitavalleycac.com" style="color:var(--navy);">info@washitavalleycac.com</a></p></div>
          </div>
        </div>
      </div>

      <!-- CALENDAR COLUMN -->
      <div>
        <div class="content-card">
          <h2>Meeting Calendar</h2>
          <p style="margin-bottom:1rem;font-size:1rem;color:var(--muted);">
            Upcoming Policy Council meetings — updated automatically from our internal schedule.
          </p>

          <!-- ── HOW TO UPDATE (staff only — remove this box once live) ──
               1. Open your Google Sheet.
               2. File → Share → Publish to web → Sheet1 → CSV → Publish.
               3. Copy the URL and paste it into SHEET_CSV_URL below in the <script>.
               Sheet columns must be: Date | Time | Title | Description
               Date format: MM/DD/YYYY   e.g. 07/15/2025
          ── -->

          <div id="calendar-loading" style="text-align:center;padding:2rem;color:var(--muted);font-size:1rem;">
            Loading meetings&hellip;
          </div>
          <div id="calendar-error" style="display:none;" class="alert">
            Calendar could not be loaded. Please contact the office for upcoming meeting dates.
          </div>
          <ul id="calendar-list" style="list-style:none;display:flex;flex-direction:column;gap:.75rem;"></ul>
          <p id="calendar-empty" style="display:none;color:var(--muted);font-size:1rem;">No upcoming meetings scheduled.</p>
        </div>

        <!-- ADMIN SETUP CARD — visible to staff, explains how to connect the sheet -->
        <div class="content-card" style="border:2px dashed var(--gold);background:#fffbeb;">
          <h2 style="color:#92400e;">&#9998; Staff Setup — Connect Your Google Sheet</h2>
          <ol style="padding-left:1.25rem;color:var(--muted);font-size:1rem;line-height:1.9;margin-bottom:1rem;">
            <li>Open your Google Sheet with meeting dates.</li>
            <li>Make sure columns are in this exact order:<br>
              <code style="background:#f3f4f6;padding:.1rem .4rem;border-radius:4px;font-size:1rem;">Date &nbsp;|&nbsp; Time &nbsp;|&nbsp; Title &nbsp;|&nbsp; Description</code><br>
              Date format: <strong>MM/DD/YYYY</strong> &nbsp; e.g. <em>07/15/2025</em>
            </li>
            <li>In Google Sheets: <strong>File → Share → Publish to web</strong></li>
            <li>Choose <strong>Sheet1</strong> and format <strong>CSV</strong>, then click <strong>Publish</strong>.</li>
            <li>Copy the URL Google gives you.</li>
            <li>Open <code style="background:#f3f4f6;padding:.1rem .4rem;border-radius:4px;font-size:1rem;">build_pages.py</code> and find this line:<br>
              <code style="background:#f3f4f6;padding:.1rem .4rem;border-radius:4px;font-size:1rem;">const SHEET_CSV_URL = ...</code><br>
              Replace the placeholder with your URL, then run <code style="background:#f3f4f6;padding:.1rem .4rem;border-radius:4px;font-size:1rem;">python3 build_pages.py</code>.
            </li>
          </ol>
          <p style="font-size:1rem;color:#92400e;"><strong>After setup:</strong> Just edit the Google Sheet — the calendar updates automatically. No code needed.</p>
        </div>
      </div>
    </div>

    <script>
    // ── PASTE YOUR PUBLISHED GOOGLE SHEET CSV URL BELOW ──────────────────
    const SHEET_CSV_URL = "";
    // ─────────────────────────────────────────────────────────────────────

    (function () {
      const list    = document.getElementById("calendar-list");
      const loading = document.getElementById("calendar-loading");
      const error   = document.getElementById("calendar-error");
      const empty   = document.getElementById("calendar-empty");

      if (!SHEET_CSV_URL) {
        loading.style.display = "none";
        error.style.display   = "block";
        error.textContent     = "Calendar not yet connected. See staff setup instructions below.";
        return;
      }

      fetch(SHEET_CSV_URL)
        .then(r => { if (!r.ok) throw new Error(); return r.text(); })
        .then(csv => {
          loading.style.display = "none";
          const rows = csv.trim().split("\\n").slice(1) // skip header row
            .map(row => row.split(",").map(c => c.replace(/^"|"$/g, "").trim()))
            .filter(r => r[0])
            .map(r => ({ date: new Date(r[0]), time: r[1] || "", title: r[2] || "", desc: r[3] || "" }))
            .filter(r => !isNaN(r.date) && r.date >= new Date(new Date().toDateString())) // upcoming only
            .sort((a, b) => a.date - b.date);

          if (!rows.length) { empty.style.display = "block"; return; }

          const months = ["January","February","March","April","May","June","July","August","September","October","November","December"];
          const days   = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];

          rows.forEach(ev => {
            const li = document.createElement("li");
            li.style.cssText = "display:flex;gap:1rem;align-items:flex-start;padding:.9rem 1rem;background:var(--bg);border:1px solid var(--border);border-radius:8px;";
            li.innerHTML = \`
              <div style="min-width:52px;text-align:center;background:var(--navy);color:#fff;border-radius:8px;padding:.4rem .5rem;flex-shrink:0;">
                <div style="font-size:.875rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;opacity:.8;">\${months[ev.date.getMonth()].slice(0,3)}</div>
                <div style="font-size:1.5rem;font-weight:900;line-height:1;">\${ev.date.getDate()}</div>
                <div style="font-size:.875rem;color:rgba(255,255,255,.82);">\${days[ev.date.getDay()]}</div>
              </div>
              <div>
                <div style="font-weight:700;color:var(--navy);font-size:1rem;">\${ev.title}</div>
                \${ev.time ? \`<div style="font-size:1rem;color:var(--muted);">&#128337; \${ev.time}</div>\` : ""}
                \${ev.desc ? \`<div style="font-size:1rem;color:var(--muted);margin-top:.2rem;">\${ev.desc}</div>\` : ""}
              </div>\`;
            list.appendChild(li);
          });
        })
        .catch(() => {
          loading.style.display = "none";
          error.style.display   = "block";
        });
    })();
    </script>"""
)

# ENROLLMENT APPLICATION
pages["enrollment-application.html"] = page(
    "enrollment-application.html", "Enrollment Application",
    "Head Start and Early Head Start enrollment application — WVCAC.",
    "Apply for Head Start or Early Head Start today.",
    """
    <div class="content-card">
      <h2>Washita Valley Community Action Council<br>Head Start / Early Head Start Enrollment Application</h2>
      <p>In addition to completing the online enrollment application, the following documents are needed to complete the enrollment process:</p>
      <ul style="margin-top:.75rem;">
        <li><strong>Proof of Date of Birth</strong> — Copy of birth certificate, hospital record or other official document with the date of the child's birth. <em>(required)</em></li>
        <li><strong>Income for 12 month period</strong> — Income tax statement (Federal 1040 only), prior year W-2, check stubs with year-to-date income, SSI document, TANF, SNAP, child support statements, OR employer Statement on letterhead. <em>(ONE of these is required)</em></li>
        <li><strong>Immunization Record/Exemption</strong> — Refer to appendix II, immunizations, in Requirements for Child Care Programs for immunization and exemption procedures.</li>
        <li><strong>Completed Consent Page</strong> — Must contain parent/guardian signature. <em>(required)</em></li>
        <li><strong>Health Insurance Card</strong> — Attach a copy, if available. <em>(not required)</em></li>
        <li><strong>Social Security Card</strong> — Attach a copy, if available. <em>(not required)</em></li>
        <li><strong>Parent and Staff Signatures</strong> — <em>Required.</em></li>
      </ul>
    </div>

    <div class="content-card">
      <h2>Immunizations</h2>
      <ul>
        <li>Attach a copy of the child's immunization record. An immunization record or exemption is obtained prior to the first day of attendance and is to be kept updated when the child receives additional vaccines.</li>
        <li>Parent/Guardian must provide a copy of the current immunization record to the child care program. Refer to appendix II, Immunizations, in Requirements for Child Care Programs for immunization and exemption procedure.</li>
        <li>Selecting Child Care Programs, DHS publication "A Parent Guide" 87-91, Licensing Requirements for Child Care Programs, DHS publication 14-05, and the program compliance file are all made accessible to parents in a prominent location.</li>
      </ul>
    </div>

    <div class="content-card">
      <h2>Application Process</h2>
      <ol style="padding-left:1.25rem;display:flex;flex-direction:column;gap:.75rem;color:var(--muted);font-size:1rem;">
        <li>
          Fill out the web-based Application
          <a href="https://na4.documents.adobe.com/public/esignWidget?wid=CBFCIBAA3AAABLblqZhA8osJppai-32RY_0PTlpLkdXXytSetFn8rqOwsuxUsxIu_Zakc7faUvGp20EcRzfI*"
             target="_blank" rel="noopener"
             style="color:var(--navy);font-weight:700;margin-left:.25rem;">HERE ↗</a>
        </li>
        <li>Attach the application and any other documentation required.</li>
        <li>
          <strong>Turn in Application and Documents:</strong>
          <ul style="margin-top:.4rem;">
            <li>By scanning and sending via email to: <a href="mailto:ersea@washitavalleycac.com" style="color:var(--navy);">ersea@washitavalleycac.com</a></li>
            <li>By mail to: PO Box 747, Chickasha, OK 73023</li>
            <li>Drop off: 1000 W. Minnesota Ave., Chickasha, OK 73018</li>
          </ul>
        </li>
      </ol>
    </div>"""
)

# SERVICES
pages["services.html"] = page(
    "services.html", "Services",
    "Services offered by Washita Valley Community Action Council including Transit, Weatherization, and Housing.",
    "Connecting families to the services they need.",
    """
    <div class="info-grid">
      <div class="content-card">
        <h2>Transit</h2>
        <p>Affordable public transportation for Grady County residents — connecting people to medical appointments, employment, and essential services.</p>
        <a href="transit.html" class="btn btn-primary" style="margin-top:.5rem;">Learn More</a>
      </div>
      <div class="content-card">
        <h2>Weatherization</h2>
        <p>Free home energy improvements for income-qualifying households — insulation, air sealing, and heating system upgrades funded by the U.S. Department of Energy.</p>
        <a href="weatherization.html" class="btn btn-primary" style="margin-top:.5rem;">Learn More</a>
      </div>
      <div class="content-card">
        <h2>Housing</h2>
        <p>Housing counseling, advocacy, and assistance to help qualifying families find and maintain safe, stable, affordable housing.</p>
        <a href="housing.html" class="btn btn-primary" style="margin-top:.5rem;">Learn More</a>
      </div>
    </div>"""
)

# TRANSIT
pages["transit.html"] = page(
    "transit.html", "Transit",
    "WVCAC public transit services for Grady County — affordable rides to medical, employment, and essential destinations.",
    "Affordable public transportation across Grady County.",
    """
    <div class="two-col">
      <div>
        <div class="img-block">
          <img src="https://static.wixstatic.com/media/bf0d32_61ea4223d8f14c549980c624fccc4181~mv2_d_3264_2448_s_4_2.jpg/v1/fill/w_900,h_675,al_c,q_85,enc_avif,quality_auto/bf0d32_61ea4223d8f14c549980c624fccc4181~mv2_d_3264_2448_s_4_2.jpg"
               alt="White transit bus sponsored by local organizations serving Grady County residents"
               loading="lazy" width="900" height="675"/>
        </div>
        <div class="img-block">
          <img src="https://static.wixstatic.com/media/bf0d32_63c2e5ece3b6406e8c0e8e7a235fd1b6~mv2.jpg/v1/fill/w_900,h_600,al_c,q_85,enc_avif,quality_auto/bf0d32_63c2e5ece3b6406e8c0e8e7a235fd1b6~mv2.jpg"
               alt="Map of Grady County Oklahoma showing transit routes and cities served"
               loading="lazy" width="900" height="600"/>
        </div>
      </div>
      <div>
        <div class="content-card">
          <h2>Fares</h2>
          <div class="info-box" style="margin-bottom:1rem;"><h3>Outside Chickasha</h3><p><strong>$5.00 each way</strong></p></div>
          <div class="info-box"><h3>Children Under 12</h3><p>Must be accompanied by a parent or guardian at all times.</p></div>
        </div>
        <div class="content-card">
          <h2>Public Outreach</h2>
          <ul>
            <li>All public meetings advertised in the local newspaper.</li>
            <li>Notices posted at local churches, community centers, and businesses.</li>
            <li>Fliers about transit services posted throughout the community.</li>
          </ul>
        </div>
        <div class="content-card">
          <h2>Contact</h2>
          <div class="info-grid">
            <div class="info-box"><h3>Phone</h3><p>(405) 224-5831</p></div>
            <div class="info-box"><h3>Email</h3><p><a href="mailto:info@washitavalleycac.com" style="color:var(--navy);">info@washitavalleycac.com</a></p></div>
          </div>
        </div>
      </div>
    </div>"""
)

# WEATHERIZATION
pages["weatherization.html"] = page(
    "weatherization.html", "Weatherization",
    "Free home weatherization services for low-income families in Oklahoma — funded by the U.S. Department of Energy.",
    "Reducing energy costs and improving home comfort for low-income families.",
    """
    <div class="two-col">
      <div>
        <div class="img-block">
          <img src="https://static.wixstatic.com/media/bf0d32_5d23246228b74514b3119f1982ed0bd6~mv2.jpg/v1/fill/w_900,h_600,al_c,q_85,enc_avif,quality_auto/bf0d32_5d23246228b74514b3119f1982ed0bd6~mv2.jpg"
               alt="Three light bulbs reflecting blue sky and clouds — symbolizing energy efficiency"
               loading="lazy" width="900" height="600"/>
        </div>
        <div class="content-card">
          <h2>Fredrick Office Contact</h2>
          <div class="info-box" style="margin-bottom:.75rem;"><h3>Address</h3><p>105 S. Main, Fredrick, OK 73542</p></div>
          <div class="info-box"><h3>Phone</h3><p>(580) 335-5588</p></div>
          <p style="margin-top:.75rem;font-size:1rem;color:var(--muted);">This is the contact for the Community Action that will be performing the weatherization services.</p>
        </div>
      </div>
      <div>
        <div class="content-card">
          <h2>What Is the Weatherization Program?</h2>
          <p>This is a program funded and guided by the U.S. Department of Energy to assist low-income families in saving energy and reducing utility costs. Improvements are made at no cost to qualifying households.</p>
        </div>
        <div class="content-card">
          <h2>Energy Saving Tips</h2>
          <ul>
            <li><strong>Drapes</strong> — Where windows face the sun, keep drapes open during the day and close them at night.</li>
            <li><strong>Programmable Thermostat</strong> — Use one to automatically control the heat at night and when you are not at home.</li>
            <li><strong>Air Sealing</strong> — Seal gaps around doors and windows to prevent drafts.</li>
            <li><strong>Insulation</strong> — Proper attic and wall insulation significantly reduces heating and cooling costs.</li>
          </ul>
        </div>
        <div class="content-card">
          <h2>Apply for Services</h2>
          <p>To find out if you qualify for weatherization assistance, contact our main office:</p>
          <div class="info-grid">
            <div class="info-box"><h3>Phone</h3><p>(405) 224-5831</p></div>
            <div class="info-box"><h3>Email</h3><p><a href="mailto:info@washitavalleycac.com" style="color:var(--navy);">info@washitavalleycac.com</a></p></div>
          </div>
        </div>
      </div>
    </div>"""
)

# HOUSING
pages["housing.html"] = page(
    "housing.html", "Housing",
    "Housing assistance and fair housing services from Washita Valley Community Action Council.",
    "Helping families find and maintain safe, affordable housing.",
    """
    <div class="two-col">
      <div>
        <div class="img-block">
          <img src="https://static.wixstatic.com/media/bf0d32_65830ba07f0344afb20f1efe9d57ef48~mv2.jpg/v1/fill/w_900,h_600,al_c,q_85,enc_avif,quality_auto/bf0d32_65830ba07f0344afb20f1efe9d57ef48~mv2.jpg"
               alt="Colorful illustrated neighborhood of homes representing fair housing opportunity for all families"
               loading="lazy" width="900" height="600"/>
        </div>
        <div class="img-block">
          <img src="https://static.wixstatic.com/media/bf0d32_c1b44aa8bf844647a2f781645089f09a~mv2.jpg/v1/fill/w_300,h_300,al_c,q_85,enc_avif,quality_auto/bf0d32_c1b44aa8bf844647a2f781645089f09a~mv2.jpg"
               alt="Equal Housing Opportunity logo"
               loading="lazy" width="300" height="300"
               style="max-width:160px;margin:0 auto;"/>
        </div>
      </div>
      <div>
        <div class="content-card">
          <h2>Housing Assistance</h2>
          <p>Washita Valley CAC provides housing counseling, advocacy, and direct assistance to help qualifying families find and maintain safe, affordable housing in our community.</p>
          <p>We are an Equal Housing Opportunity provider committed to fair housing for all.</p>
        </div>
        <div class="content-card">
          <h2>Contact for Housing</h2>
          <div class="alert">For Housing Information, please contact <strong>Dillon Duke</strong> directly.</div>
          <div class="info-grid">
            <div class="info-box"><h3>Phone</h3><p>(405) 224-5831 ext. 132</p></div>
            <div class="info-box"><h3>Address</h3><p>1000 West Minnesota Ave.<br>Chickasha, OK 73018</p></div>
          </div>
        </div>
      </div>
    </div>"""
)

# BOARD OF DIRECTORS
pages["board-of-directors.html"] = page(
    "board-of-directors.html", "Board of Directors",
    "Washita Valley Community Action Council Board of Directors.",
    "Governance and leadership of WVCAC.",
    """
    <div class="two-col" style="align-items:start;">

      <!-- Left: About + Contact -->
      <div>
        <div class="content-card">
          <h2>Board of Directors</h2>
          <p>The Washita Valley CAC Board of Directors provides oversight and strategic leadership for the organization, ensuring our programs remain aligned with our mission to assist individuals and families in Grady and Caddo Counties.</p>
          <p>For information about the Board of Directors, please contact us:</p>
          <div class="info-grid" style="margin-top:.75rem;">
            <div class="info-box"><h3>Phone</h3><p>(405) 224-5831</p></div>
            <div class="info-box"><h3>Email</h3><p><a href="mailto:info@washitavalleycac.com" style="color:var(--navy);">info@washitavalleycac.com</a></p></div>
            <div class="info-box"><h3>Address</h3><p>1000 West Minnesota Ave.<br>Chickasha, OK 73018</p></div>
          </div>
        </div>
      </div>

      <!-- Right: Board Agenda -->
      <div>
        <div class="content-card">
          <h2>Board Agenda</h2>
          <p style="font-size:1rem;color:var(--muted);margin-bottom:1.25rem;">
            Current board meeting agenda — updated automatically from our internal schedule.
          </p>

          <div id="agenda-loading" style="text-align:center;padding:2rem;color:var(--muted);font-size:1rem;">Loading agenda&hellip;</div>
          <div id="agenda-error" class="alert" style="display:none;">Agenda not yet available. Please contact the office for meeting details.</div>
          <div id="agenda-wrap" style="display:none;">
            <div id="agenda-header" style="background:var(--navy);color:#fff;border-radius:8px 8px 0 0;padding:1rem 1.25rem;margin-bottom:0;">
              <div style="font-size:.875rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.82);margin-bottom:.2rem;">Board Meeting</div>
              <div id="agenda-meeting-title" style="font-size:1.1rem;font-weight:800;"></div>
              <div id="agenda-meeting-meta"  style="font-size:1rem;color:rgba(255,255,255,.88);margin-top:.2rem;"></div>
            </div>
            <ol id="agenda-list" style="list-style:none;border:1px solid var(--border);border-top:none;border-radius:0 0 8px 8px;overflow:hidden;"></ol>
          </div>
          <p id="agenda-empty" style="display:none;color:var(--muted);font-size:1rem;">No agenda items available at this time.</p>
        </div>

        <!-- Staff setup card -->
        <div class="content-card" style="border:2px dashed var(--gold);background:#fffbeb;">
          <h2 style="color:#92400e;">&#9998; Staff Setup — Connect Your Google Sheet</h2>
          <p style="font-size:1rem;color:var(--muted);margin-bottom:.75rem;">Set up your Google Sheet with these exact columns in row 1:</p>
          <div style="overflow-x:auto;margin-bottom:1rem;">
            <table style="width:100%;border-collapse:collapse;font-size:1rem;border:1px solid var(--border);border-radius:6px;overflow:hidden;">
              <thead>
                <tr style="background:var(--navy);color:#fff;">
                  <th style="padding:.5rem .75rem;text-align:left;">A — Meeting</th>
                  <th style="padding:.5rem .75rem;text-align:left;">B — Date</th>
                  <th style="padding:.5rem .75rem;text-align:left;">C — Time</th>
                  <th style="padding:.5rem .75rem;text-align:left;">D — Location</th>
                  <th style="padding:.5rem .75rem;text-align:left;">E — Item #</th>
                  <th style="padding:.5rem .75rem;text-align:left;">F — Topic</th>
                  <th style="padding:.5rem .75rem;text-align:left;">G — Notes</th>
                </tr>
              </thead>
              <tbody>
                <tr style="background:#fff;font-size:1rem;color:var(--muted);">
                  <td style="padding:.45rem .75rem;">June 2025 Meeting</td>
                  <td style="padding:.45rem .75rem;">06/18/2025</td>
                  <td style="padding:.45rem .75rem;">9:00 AM</td>
                  <td style="padding:.45rem .75rem;">Main Office</td>
                  <td style="padding:.45rem .75rem;">1</td>
                  <td style="padding:.45rem .75rem;">Call to Order</td>
                  <td style="padding:.45rem .75rem;"></td>
                </tr>
              </tbody>
            </table>
          </div>
          <ol style="padding-left:1.25rem;color:var(--muted);font-size:1rem;line-height:1.9;margin-bottom:1rem;">
            <li>Each row = one agenda item. Repeat Meeting, Date, Time, Location on every row.</li>
            <li>In Google Sheets: <strong>File → Share → Publish to web → Sheet1 → CSV → Publish</strong></li>
            <li>Copy the published URL and paste it into <code style="background:#f3f4f6;padding:.1rem .4rem;border-radius:4px;">build_pages.py</code> in the line:<br>
              <code style="background:#f3f4f6;padding:.1rem .4rem;border-radius:4px;">const AGENDA_CSV_URL = ""</code>
            </li>
            <li>Run <code style="background:#f3f4f6;padding:.1rem .4rem;border-radius:4px;">python3 build_pages.py</code> once to apply.</li>
          </ol>
          <p style="font-size:1rem;color:#92400e;"><strong>After setup:</strong> Edit the sheet anytime — the agenda updates automatically. No code needed.</p>
        </div>
      </div>
    </div>

    <script>
    // ── PASTE YOUR PUBLISHED GOOGLE SHEET CSV URL BELOW ──────────────────
    const AGENDA_CSV_URL = "";
    // ─────────────────────────────────────────────────────────────────────

    (function () {
      const loading = document.getElementById("agenda-loading");
      const error   = document.getElementById("agenda-error");
      const wrap    = document.getElementById("agenda-wrap");
      const list    = document.getElementById("agenda-list");
      const empty   = document.getElementById("agenda-empty");
      const title   = document.getElementById("agenda-meeting-title");
      const meta    = document.getElementById("agenda-meeting-meta");

      if (!AGENDA_CSV_URL) {
        loading.style.display = "none";
        error.style.display   = "block";
        error.textContent     = "Agenda not yet connected. See staff setup instructions below.";
        return;
      }

      fetch(AGENDA_CSV_URL)
        .then(r => { if (!r.ok) throw new Error(); return r.text(); })
        .then(csv => {
          loading.style.display = "none";
          const rows = csv.trim().split("\\n").slice(1)
            .map(row => {
              // handle quoted CSV fields
              const cols = [];
              let cur = "", inQ = false;
              for (const ch of row) {
                if (ch === '"') { inQ = !inQ; }
                else if (ch === "," && !inQ) { cols.push(cur.trim()); cur = ""; }
                else cur += ch;
              }
              cols.push(cur.trim());
              return cols;
            })
            .filter(r => r[5]); // must have a Topic

          if (!rows.length) { empty.style.display = "block"; return; }

          // Use first row for meeting header
          const meeting  = rows[0][0] || "Board Meeting";
          const dateStr  = rows[0][1] || "";
          const timeStr  = rows[0][2] || "";
          const location = rows[0][3] || "";

          title.textContent = meeting;
          const metaParts = [];
          if (dateStr) { const d = new Date(dateStr); metaParts.push(isNaN(d) ? dateStr : d.toLocaleDateString("en-US",{weekday:"long",year:"numeric",month:"long",day:"numeric"})); }
          if (timeStr)  metaParts.push("&#128337; " + timeStr);
          if (location) metaParts.push("&#128205; " + location);
          meta.innerHTML = metaParts.join(" &nbsp;&bull;&nbsp; ");

          wrap.style.display = "block";

          rows.forEach((r, i) => {
            const itemNum = r[4] || (i + 1);
            const topic   = r[5] || "";
            const notes   = r[6] || "";
            const li = document.createElement("li");
            li.style.cssText = \`display:flex;gap:1rem;align-items:flex-start;padding:.85rem 1.25rem;background:\${i%2===0?"#fff":"var(--bg)"};border-top:\${i===0?"none":"1px solid var(--border)"};\`;
            li.innerHTML = \`
              <span style="min-width:28px;height:28px;background:var(--navy);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.875rem;font-weight:800;flex-shrink:0;margin-top:.1rem;">\${itemNum}</span>
              <span>
                <span style="font-weight:700;color:var(--text);font-size:.92rem;">\${topic}</span>
                \${notes ? \`<span style="display:block;font-size:1rem;color:var(--muted);margin-top:.15rem;">\${notes}</span>\` : ""}
              </span>\`;
            list.appendChild(li);
          });
        })
        .catch(() => {
          loading.style.display = "none";
          error.style.display   = "block";
        });
    })();
    </script>"""
)

# AGENCY FORMS
pages["agency-forms.html"] = page(
    "agency-forms.html", "Agency Forms",
    "Official forms and documents from Washita Valley Community Action Council.",
    "Secure access to agency documents and forms.",
    """
    <!-- ── MSAL.js — Microsoft Authentication Library ── -->
    <script src="https://alcdn.msauth.net/browser/2.38.3/js/msal-browser.min.js"></script>

    <style>
      /* Login wall */
      #login-wall{display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:340px;gap:1.5rem;text-align:center;}
      #login-wall h2{color:var(--navy);font-size:1.4rem;font-weight:800;}
      #login-wall p{color:var(--muted);font-size:1rem;max-width:420px;}
      .ms-btn{display:inline-flex;align-items:center;gap:.75rem;background:#fff;border:1.5px solid #d1d5db;border-radius:6px;padding:.7rem 1.4rem;font-size:1rem;font-weight:600;color:#111827;cursor:pointer;transition:.2s;font-family:inherit;box-shadow:0 1px 4px rgba(0,0,0,.08);}
      .ms-btn:hover{background:#f3f4f6;box-shadow:0 2px 8px rgba(0,0,0,.12);}
      .ms-btn img{width:20px;height:20px;}
      #login-error{color:#b91c1c;background:#fef2f2;border:1px solid #fca5a5;border-radius:8px;padding:.65rem 1rem;font-size:1rem;display:none;}
      /* User bar */
      #user-bar{display:none;align-items:center;justify-content:space-between;gap:1rem;background:var(--bg);border:1px solid var(--border);border-radius:10px;padding:.75rem 1.25rem;margin-bottom:1.5rem;flex-wrap:wrap;}
      #user-bar-name{font-weight:700;color:var(--navy);font-size:.92rem;}
      #user-bar-email{font-size:1rem;color:var(--muted);}
      .logout-btn{background:none;border:1.5px solid var(--border);border-radius:6px;padding:.5rem 1rem;min-height:44px;font-size:1rem;font-weight:600;color:var(--muted);cursor:pointer;font-family:inherit;transition:.2s;}
      .logout-btn:hover{border-color:#b91c1c;color:#b91c1c;}
      /* Forms content */
      #forms-content{display:none;}
      .form-row{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.85rem 1.1rem;border-bottom:1px solid var(--border);flex-wrap:wrap;}
      .form-row:last-child{border-bottom:none;}
      .form-row:nth-child(even){background:var(--bg);}
      .form-name{font-weight:600;color:var(--text);font-size:.92rem;}
      .form-desc{font-size:1rem;color:var(--muted);margin-top:.15rem;}
      .form-dl-btn{display:inline-flex;align-items:center;gap:.35rem;background:var(--navy);color:#fff;border-radius:6px;padding:.6rem 1rem;min-height:44px;font-size:1rem;font-weight:700;white-space:nowrap;transition:.2s;text-decoration:none;flex-shrink:0;}
      .form-dl-btn:hover{background:var(--navy-d);}
    </style>

    <!-- LOGIN WALL -->
    <div id="login-wall" class="content-card">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--navy)" stroke-width="1.5" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
      <h2>Agency Forms — Staff Access Only</h2>
      <p>This section is restricted to Washita Valley CAC staff. Sign in with your Microsoft work account to continue.</p>
      <div id="login-error" role="alert"></div>
      <button class="ms-btn" id="login-btn" aria-label="Sign in with Microsoft">
        <img src="https://learn.microsoft.com/en-us/azure/active-directory/develop/media/howto-add-branding-in-apps/ms-symbollockup_mssymbol_19.png" alt="" aria-hidden="true"/>
        Sign in with Microsoft
      </button>
    </div>

    <!-- AUTHENTICATED VIEW -->
    <div id="user-bar" role="status" aria-live="polite">
      <div>
        <div id="user-bar-name"></div>
        <div id="user-bar-email"></div>
      </div>
      <button class="logout-btn" id="logout-btn">Sign out</button>
    </div>

    <div id="forms-content">
      <div class="content-card">
        <h2>Agency Forms</h2>
        <p style="margin-bottom:1rem;font-size:1rem;color:var(--muted);">Download or complete official WVCAC forms below. Contact the office if a form you need is missing.</p>
        <div>
          <div class="form-row">
            <div>
              <div class="form-name">Head Start / EHS Enrollment Application</div>
              <div class="form-desc">Complete online via Adobe Sign</div>
            </div>
            <a class="form-dl-btn" href="https://na4.documents.adobe.com/public/esignWidget?wid=CBFCIBAA3AAABLblqZhA8osJppai-32RY_0PTlpLkdXXytSetFn8rqOwsuxUsxIu_Zakc7faUvGp20EcRzfI*" target="_blank" rel="noopener">
              Open ↗
            </a>
          </div>
          <div class="form-row">
            <div>
              <div class="form-name">Economic Impact Report</div>
              <div class="form-desc">PDF — Annual community impact summary</div>
            </div>
            <a class="form-dl-btn" href="https://www.washitavalleycac.com/_files/ugd/bf0d32_65e17de209994b9384d633b8fc1d7980.pdf" target="_blank" rel="noopener">
              ↓ Download
            </a>
          </div>
          <div class="form-row">
            <div>
              <div class="form-name">Community Survey</div>
              <div class="form-desc">Client satisfaction and needs assessment</div>
            </div>
            <a class="form-dl-btn" href="https://capaz6.capsystems.com/OKAMS//05/Ques.aspx?surID=932e5dca-468f-4707-bbe0-c11434115f41&Agy=05&Type=WEB-LINK" target="_blank" rel="noopener">
              Open ↗
            </a>
          </div>
        </div>
      </div>

      <div class="content-card">
        <h2>Need Help?</h2>
        <div class="info-grid">
          <div class="info-box"><h3>Phone</h3><p>(405) 224-5831</p></div>
          <div class="info-box"><h3>Email</h3><p><a href="mailto:info@washitavalleycac.com" style="color:var(--navy);">info@washitavalleycac.com</a></p></div>
          <div class="info-box"><h3>Office Hours</h3><p>Monday – Friday<br>8:00 AM – 5:00 PM</p></div>
        </div>
      </div>
    </div>

    <!-- AZURE SETUP CARD (remove once live) -->
    <div class="content-card" style="border:2px dashed var(--gold);background:#fffbeb;margin-top:1.5rem;">
      <h2 style="color:#92400e;">&#9998; IT Setup — Connect Azure SSO</h2>
      <p style="font-size:1rem;color:var(--muted);margin-bottom:.75rem;">A Microsoft Azure admin needs to do this once:</p>
      <ol style="padding-left:1.25rem;color:var(--muted);font-size:1rem;line-height:2;margin-bottom:1rem;">
        <li>Go to <strong>portal.azure.com</strong> → <strong>Azure Active Directory → App registrations → New registration</strong></li>
        <li>Name it <em>"WVCAC Agency Forms"</em>, set account type to <strong>Accounts in this organizational directory only</strong></li>
        <li>Under <strong>Redirect URI</strong>, choose <strong>Single-page application (SPA)</strong> and enter the full URL of this page (e.g. <code style="background:#f3f4f6;padding:.1rem .4rem;border-radius:4px;">https://yourdomain.com/agency-forms.html</code>)</li>
        <li>Click <strong>Register</strong>. Copy the <strong>Application (client) ID</strong> and <strong>Directory (tenant) ID</strong>.</li>
        <li>Open <code style="background:#f3f4f6;padding:.1rem .4rem;border-radius:4px;">build_pages.py</code> and find:<br>
          <code style="background:#f3f4f6;padding:.1rem .4rem;border-radius:4px;display:block;margin:.3rem 0;">const AZURE_CLIENT_ID = "";<br>const AZURE_TENANT_ID = "";</code>
          Paste your IDs, then run <code style="background:#f3f4f6;padding:.1rem .4rem;border-radius:4px;">python3 build_pages.py</code>.
        </li>
      </ol>
      <p style="font-size:1rem;color:#92400e;"><strong>After setup:</strong> Staff sign in with their @washitavalleycac.com Microsoft account. No passwords to manage — Azure handles everything.</p>
    </div>

    <script>
    // ── PASTE YOUR AZURE APP REGISTRATION VALUES BELOW ───────────────────
    const AZURE_CLIENT_ID = "";   // Application (client) ID
    const AZURE_TENANT_ID = "";   // Directory (tenant) ID
    // ─────────────────────────────────────────────────────────────────────

    (function () {
      const loginWall   = document.getElementById("login-wall");
      const loginBtn    = document.getElementById("login-btn");
      const loginErr    = document.getElementById("login-error");
      const userBar     = document.getElementById("user-bar");
      const formsContent= document.getElementById("forms-content");
      const userName    = document.getElementById("user-bar-name");
      const userEmail   = document.getElementById("user-bar-email");
      const logoutBtn   = document.getElementById("logout-btn");

      if (!AZURE_CLIENT_ID || !AZURE_TENANT_ID) {
        loginBtn.disabled = true;
        loginErr.style.display = "block";
        loginErr.textContent = "Azure SSO not yet configured. See IT setup instructions below.";
        return;
      }

      const msalConfig = {
        auth: {
          clientId: AZURE_CLIENT_ID,
          authority: "https://login.microsoftonline.com/" + AZURE_TENANT_ID,
          redirectUri: window.location.href.split("?")[0],
        },
        cache: { cacheLocation: "sessionStorage" }
      };

      const msalInstance = new msal.PublicClientApplication(msalConfig);

      function showForms(account) {
        loginWall.style.display   = "none";
        userBar.style.display     = "flex";
        formsContent.style.display= "block";
        userName.textContent  = account.name || account.username;
        userEmail.textContent = account.username;
      }

      // Check if already signed in
      msalInstance.handleRedirectPromise().then(response => {
        if (response) { showForms(response.account); return; }
        const accounts = msalInstance.getAllAccounts();
        if (accounts.length) showForms(accounts[0]);
      }).catch(e => {
        loginErr.style.display = "block";
        loginErr.textContent = "Sign-in error: " + (e.message || "Please try again.");
      });

      loginBtn.addEventListener("click", () => {
        loginErr.style.display = "none";
        msalInstance.loginPopup({ scopes: ["User.Read"] })
          .then(resp => showForms(resp.account))
          .catch(e => {
            if (e.errorCode !== "user_cancelled") {
              loginErr.style.display = "block";
              loginErr.textContent = "Sign-in failed: " + (e.message || "Please try again.");
            }
          });
      });

      logoutBtn.addEventListener("click", () => {
        msalInstance.logoutPopup().then(() => {
          userBar.style.display      = "none";
          formsContent.style.display = "none";
          loginWall.style.display    = "flex";
        });
      });
    })();
    </script>"""
)

# JOB OPENINGS
pages["job-openings.html"] = page(
    "job-openings.html", "Job Openings",
    "Current employment opportunities at Washita Valley Community Action Council.",
    "Join the Washita Valley CAC team — current openings listed below.",
    """
    <div class="content-card">
      <h2>Current Openings</h2>
      <div class="alert" style="margin-bottom:1.5rem;">
        <strong>ALL EMPLOYMENT APPLICATIONS MUST BE SUBMITTED WITH A CURRENT RESUME BEFORE WVCAC CAN SET UP AN INTERVIEW.</strong>
      </div>
      <div style="display:flex;flex-direction:column;gap:0;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;">

        <div style="padding:1.25rem 1.5rem;background:#fff;border-bottom:1px solid var(--border);">
          <div style="display:flex;align-items:flex-start;gap:.75rem;">
            <span style="min-width:32px;height:32px;background:var(--navy);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1rem;font-weight:800;flex-shrink:0;margin-top:.1rem;">1</span>
            <div>
              <div style="font-weight:800;color:var(--navy);font-size:1rem;">HS Teacher Assistant (PD/PY) — Chickasha &amp; Anadarko</div>
              <p style="font-size:1rem;color:var(--muted);margin-top:.35rem;">CDA required (we will help you to obtain); experience with preschool children preferred.</p>
            </div>
          </div>
        </div>

        <div style="padding:1.25rem 1.5rem;background:var(--bg);border-bottom:1px solid var(--border);">
          <div style="display:flex;align-items:flex-start;gap:.75rem;">
            <span style="min-width:32px;height:32px;background:var(--navy);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1rem;font-weight:800;flex-shrink:0;margin-top:.1rem;">2</span>
            <div>
              <div style="font-weight:800;color:var(--navy);font-size:1rem;">Pre-School Teacher w/State Certification — Chickasha</div>
              <p style="font-size:1rem;color:var(--muted);margin-top:.35rem;">Bachelor's degree in ECE and State Certification required. Experience with preschool children preferred.</p>
            </div>
          </div>
        </div>

        <div style="padding:1.25rem 1.5rem;background:#fff;border-bottom:1px solid var(--border);">
          <div style="display:flex;align-items:flex-start;gap:.75rem;">
            <span style="min-width:32px;height:32px;background:var(--navy);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1rem;font-weight:800;flex-shrink:0;margin-top:.1rem;">3</span>
            <div>
              <div style="font-weight:800;color:var(--navy);font-size:1rem;">HS/EHS Cook Assistant — Anadarko</div>
              <p style="font-size:1rem;color:var(--muted);margin-top:.35rem;">High school graduate or GED. Food handlers certification required (Agency will help obtain).</p>
            </div>
          </div>
        </div>

        <div style="padding:1.25rem 1.5rem;background:var(--bg);">
          <div style="display:flex;align-items:flex-start;gap:.75rem;">
            <span style="min-width:32px;height:32px;background:var(--navy);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1rem;font-weight:800;flex-shrink:0;margin-top:.1rem;">4</span>
            <div>
              <div style="font-weight:800;color:var(--navy);font-size:1rem;">EHS Multi-Purpose Aide — Anadarko</div>
              <p style="font-size:1rem;color:var(--muted);margin-top:.35rem;">Infant/Toddler CDA required (but we will help you obtain).</p>
            </div>
          </div>
        </div>

      </div>
      <p style="margin-top:1rem;font-size:1rem;color:var(--muted);">Washita Valley Community Action Council is an Equal Opportunity and ADA Employer.</p>
    </div>

    <div class="content-card">
      <h2>Job Application Process</h2>
      <ol style="padding-left:1.25rem;display:flex;flex-direction:column;gap:.85rem;color:var(--muted);font-size:1rem;">
        <li>
          Fill out the Application
          <a href="https://www.washitavalleycac.com/job-openings" target="_blank" rel="noopener"
             style="color:var(--navy);font-weight:700;margin-left:.25rem;">HERE ↗</a>
        </li>
        <li>Attach Resume, Transcripts, and any certification/training documentation.</li>
        <li>
          <strong>Turn in Application and Documents:</strong>
          <ul style="margin-top:.4rem;">
            <li>By scanning and sending via email to: <a href="mailto:info@washitavalleycac.com" style="color:var(--navy);">info@washitavalleycac.com</a></li>
            <li>By mail to: PO Box 747, Chickasha, OK 73023</li>
            <li>Drop off: 1000 W. Minnesota Ave., Chickasha, OK 73018</li>
          </ul>
        </li>
      </ol>
    </div>"""
)

# STAFF
pages["staff.html"] = page(
    "staff.html", "Staff",
    "Meet the staff of Washita Valley Community Action Council.",
    "Meet the dedicated team behind WVCAC programs and services.",
    """
    <script src="https://alcdn.msauth.net/browser/2.38.3/js/msal-browser.min.js" onerror="void(0)"></script>
    <style>
      .staff-section{background:#d6d6d6;padding:2.5rem 2rem;border-radius:var(--radius);}
      .staff-section-title{text-align:center;font-size:1.6rem;font-weight:300;letter-spacing:.18em;text-transform:uppercase;color:var(--text);margin-bottom:.5rem;}
      .staff-divider{width:40px;height:2px;background:var(--text);margin:.5rem auto 2rem;}
      .staff-cols{display:grid;grid-template-columns:1fr 1fr;gap:0 3rem;}
      @media(max-width:600px){.staff-cols{grid-template-columns:1fr;}}
      .staff-entry{padding:1rem 0;border-bottom:none;}
      .staff-entry-name{font-size:1.2rem;font-weight:400;color:var(--text);margin-bottom:.2rem;}
      .staff-entry-title{font-size:1rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--text);margin-bottom:.25rem;}
      .staff-entry-email a{font-size:1rem;color:#1a4f8a;text-decoration:underline;}
      #staff-loading{text-align:center;padding:2rem;color:var(--muted);display:none;}
      #staff-error{display:none;}
      #staff-static{display:grid;}
      #staff-dynamic{display:none;}
    </style>

    <div class="content-card" style="padding:0;overflow:hidden;">
      <div class="staff-section">
        <div class="staff-section-title">Central Office Staff</div>
        <div class="staff-divider" aria-hidden="true"></div>
        <div id="staff-loading">Loading staff directory&hellip;</div>
        <div id="staff-error" class="alert" style="margin:1rem;"></div>

        <!-- STATIC (always shown until sheet connected) -->
        <div id="staff-static" class="staff-cols">
          <div class="staff-entry">
            <div class="staff-entry-name">Liane Howell</div>
            <div class="staff-entry-title">Executive Director - HS/EHS Director</div>
            <div class="staff-entry-email"><a href="mailto:lhowell@washitavalleycac.com">lhowell@washitavalleycac.com</a></div>
          </div>
          <div class="staff-entry">
            <div class="staff-entry-name">Challena Franks</div>
            <div class="staff-entry-title">Associate Director</div>
            <div class="staff-entry-email"><a href="mailto:adm@washitavalleycac.com">adm@washitavalleycac.com</a></div>
          </div>
          <div class="staff-entry">
            <div class="staff-entry-name">Brandie Samaniego</div>
            <div class="staff-entry-title">Human Resources Director</div>
            <div class="staff-entry-email"><a href="mailto:hr@washitavalleycac.com">hr@washitavalleycac.com</a></div>
          </div>
          <div class="staff-entry">
            <div class="staff-entry-name">Karleen Spenser</div>
            <div class="staff-entry-title">HS/EHS Financial Assistant</div>
            <div class="staff-entry-email"><a href="mailto:finance@washitavalleycac.com">finance@washitavalleycac.com</a></div>
          </div>
          <div class="staff-entry">
            <div class="staff-entry-name">Lisa Dover</div>
            <div class="staff-entry-title">Payroll Clerk/ Executive Assistant</div>
            <div class="staff-entry-email"><a href="mailto:payrollclerk@washitavalleycac.com">payrollclerk@washitavalleycac.com</a></div>
          </div>
          <div class="staff-entry">
            <div class="staff-entry-name">Dillon Duke</div>
            <div class="staff-entry-title">Housing Director/ Procurement</div>
            <div class="staff-entry-email"><a href="mailto:home@washitavalleycac.com">home@washitavalleycac.com</a></div>
          </div>
          <div class="staff-entry">
            <div class="staff-entry-name">Melissa Vallee</div>
            <div class="staff-entry-title">HS/EHS Education Manager</div>
            <div class="staff-entry-email"><a href="mailto:education@washitavalleycac.com">education@washitavalleycac.com</a></div>
          </div>
          <div class="staff-entry">
            <div class="staff-entry-name">Brandy Edghill</div>
            <div class="staff-entry-title">Health Manager</div>
            <div class="staff-entry-email"><a href="mailto:health@washitavalleycac.com">health@washitavalleycac.com</a></div>
          </div>
          <div class="staff-entry">
            <div class="staff-entry-name">Stephanie Dalton</div>
            <div class="staff-entry-title">HS/EHS Family/ Special Services Manager</div>
            <div class="staff-entry-email"><a href="mailto:fs@washitavalleycac.com">fs@washitavalleycac.com</a></div>
          </div>
          <div class="staff-entry">
            <div class="staff-entry-name">Linda Sain</div>
            <div class="staff-entry-title">HS/EHS Coach</div>
            <div class="staff-entry-email"><a href="mailto:coach@washitavalleycac.com">coach@washitavalleycac.com</a></div>
          </div>
          <div class="staff-entry">
            <div class="staff-entry-name">Alisa Kennell</div>
            <div class="staff-entry-title">HS/EHS ERSEA</div>
            <div class="staff-entry-email"><a href="mailto:ersea@washitavalleycac.com">ersea@washitavalleycac.com</a></div>
          </div>
          <div class="staff-entry">
            <div class="staff-entry-name">Abby Bauman</div>
            <div class="staff-entry-title">Mentor</div>
            <div class="staff-entry-email"><a href="mailto:mentor@washitavalleycac.com">mentor@washitavalleycac.com</a></div>
          </div>
          <div class="staff-entry">
            <div class="staff-entry-name">Terri Moore</div>
            <div class="staff-entry-title">Transit Route Supervisor</div>
            <div class="staff-entry-email"><a href="mailto:tmoore@washitavalleycac.com">tmoore@washitavalleycac.com</a></div>
          </div>
        </div>

        <!-- DYNAMIC (replaces static when sheet connected) -->
        <div id="staff-dynamic" class="staff-cols"></div>
      </div>
    </div>

    <div class="content-card">
      <h2>Contact the Office</h2>
      <div class="info-grid">
        <div class="info-box"><h3>Phone</h3><p>(405) 224-5831</p></div>
        <div class="info-box"><h3>Email</h3><p><a href="mailto:info@washitavalleycac.com" style="color:var(--navy);">info@washitavalleycac.com</a></p></div>
        <div class="info-box"><h3>Address</h3><p>1000 West Minnesota Ave.<br>Chickasha, OK 73018</p></div>
      </div>
      <p style="margin-top:1rem;font-size:1rem;">Interested in joining us? <a href="job-openings.html" style="color:var(--navy);font-weight:700;">View current career openings →</a></p>
    </div>

    <!-- STAFF SETUP CARD -->
    <div class="content-card" style="border:2px dashed var(--gold);background:#fffbeb;">
      <h2 style="color:#92400e;">&#9998; Staff Setup — Keep This Directory Up to Date with Google Sheets</h2>
      <p style="font-size:1rem;color:var(--muted);margin-bottom:.75rem;">
        Once connected, anyone can update the staff directory just by editing a Google Sheet — no code, no IT required.
      </p>
      <div style="overflow-x:auto;margin-bottom:1rem;">
        <table style="width:100%;border-collapse:collapse;font-size:1rem;border:1px solid var(--border);border-radius:6px;overflow:hidden;">
          <thead>
            <tr style="background:var(--navy);color:#fff;">
              <th style="padding:.5rem .75rem;text-align:left;">A — Name</th>
              <th style="padding:.5rem .75rem;text-align:left;">B — Title</th>
              <th style="padding:.5rem .75rem;text-align:left;">C — Email</th>
              <th style="padding:.5rem .75rem;text-align:left;">D — Phone (optional)</th>
            </tr>
          </thead>
          <tbody>
            <tr style="background:#fff;font-size:1rem;color:var(--muted);">
              <td style="padding:.45rem .75rem;">Liane Howell</td>
              <td style="padding:.45rem .75rem;">Executive Director · HS/EHS Director</td>
              <td style="padding:.45rem .75rem;">lhowell@washitavalleycac.com</td>
              <td style="padding:.45rem .75rem;">(405) 224-5831</td>
            </tr>
          </tbody>
        </table>
      </div>
      <ol style="padding-left:1.25rem;color:var(--muted);font-size:1rem;line-height:2;margin-bottom:1rem;">
        <li>Create a Google Sheet with the columns above. Add one row per staff member.</li>
        <li>Go to <strong>File → Share → Publish to web → Sheet1 → CSV → Publish</strong>.</li>
        <li>Copy the URL and open <code style="background:#f3f4f6;padding:.1rem .4rem;border-radius:4px;">build_pages.py</code>. Find:<br>
          <code style="background:#f3f4f6;padding:.1rem .4rem;border-radius:4px;">const STAFF_CSV_URL = ""</code><br>
          Paste your URL inside the quotes, then run <code style="background:#f3f4f6;padding:.1rem .4rem;border-radius:4px;">python3 build_pages.py</code>.
        </li>
      </ol>
      <p style="font-size:1rem;color:#92400e;"><strong>After setup:</strong> The staff list on this page updates automatically whenever anyone edits the sheet. The current list above will be replaced by the live sheet data.</p>
    </div>

    <script>
    // ── PASTE YOUR PUBLISHED GOOGLE SHEET CSV URL BELOW ──────────────────
    const STAFF_CSV_URL = "";
    // ─────────────────────────────────────────────────────────────────────

    (function () {
      if (!STAFF_CSV_URL) return; // keep static fallback

      const staticGrid  = document.getElementById("staff-static");
      const dynamicGrid = document.getElementById("staff-dynamic");
      const loading     = document.getElementById("staff-loading");
      const error       = document.getElementById("staff-error");

      loading.style.display = "block";
      staticGrid.style.display = "none";

      fetch(STAFF_CSV_URL)
        .then(r => { if (!r.ok) throw new Error(); return r.text(); })
        .then(csv => {
          loading.style.display = "none";
          const rows = csv.trim().split("\\n").slice(1)
            .map(row => {
              const cols = []; let cur = "", inQ = false;
              for (const ch of row) {
                if (ch === '"') { inQ = !inQ; }
                else if (ch === "," && !inQ) { cols.push(cur.trim()); cur = ""; }
                else cur += ch;
              }
              cols.push(cur.trim());
              return cols;
            })
            .filter(r => r[0]);

          if (!rows.length) { staticGrid.style.display = "grid"; return; }

          rows.forEach(r => {
            const name  = r[0] || "";
            const title = r[1] || "";
            const email = r[2] || "";
            const phone = r[3] || "";
            const card  = document.createElement("div");
            card.className = "staff-card";
            card.innerHTML = \`
              \${title ? \`<span class="staff-title">\${title}</span>\` : ""}
              <div class="staff-name">\${name}</div>
              \${email ? \`<div class="staff-email"><a href="mailto:\${email}">\${email}</a></div>\` : ""}
              \${phone ? \`<div class="staff-email">\${phone}</div>\` : ""}\`;
            dynamicGrid.appendChild(card);
          });
          dynamicGrid.style.display = "grid";
        })
        .catch(() => {
          loading.style.display = "none";
          staticGrid.style.display = "grid"; // fall back to static
          error.style.display = "block";
          error.textContent = "Could not load live staff directory. Showing cached data.";
        });
    })();
    </script>"""
)


# ─── Write all pages ────────────────────────────────────────────────
import os
out_dir = os.path.dirname(os.path.abspath(__file__))
for filename, html in pages.items():
    path = os.path.join(out_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  wrote {filename}")

print(f"\nDone — {len(pages)} pages generated.")
