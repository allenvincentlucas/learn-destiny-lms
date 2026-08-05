import pickle, sys, html as htmllib
sys.path.insert(0, '.')
from docx_to_html import convert_blocks
from site_data import MODULE_META, GLOSSARY
from module_content import MODULES as MC

blocks = pickle.load(open('blocks.pkl', 'rb'))
ranges = pickle.load(open('ranges.pkl', 'rb'))

SITE_URL = 'https://allenvincentlucas.github.io/learn-destiny-lms/'

CHECK_SVG = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M4 12l5 5L20 6" stroke="#2A4B8D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def esc(s):
    return htmllib.escape(s, quote=True)

# ---------------------------------------------------------------
# Shared head / topbar / footer
# ---------------------------------------------------------------
def head(title, desc, prefix='', canonical_path='', og_image='assets/img/og/home.png'):
    canonical_url = SITE_URL + canonical_path
    og_image_url = SITE_URL + og_image
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(canonical_url)}">

<!-- Favicons -->
<link rel="icon" href="{prefix}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{prefix}favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{prefix}favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="{prefix}apple-touch-icon.png">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Destiny Training Curriculum">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical_url)}">
<meta property="og:image" content="{esc(og_image_url)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(og_image_url)}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
</head>
<body>
'''

def topbar(prefix=''):
    return f'''<div class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="{prefix}index.html"><span class="brand-mark">FD</span> Destiny Training Curriculum</a>
    <nav>
      <a href="{prefix}index.html#modules">Modules</a>
      <a href="{prefix}glossary.html">Glossary</a>
    </nav>
  </div>
</div>
'''

# ---------------------------------------------------------------
# Social sharing bar (Facebook, X, Instagram-copy-link)
# ---------------------------------------------------------------
import urllib.parse

def share_bar_html(page_url, title):
    enc_url = urllib.parse.quote(page_url, safe='')
    enc_text = urllib.parse.quote(title, safe='')
    fb_url = f'https://www.facebook.com/sharer/sharer.php?u={enc_url}'
    x_url = f'https://twitter.com/intent/tweet?url={enc_url}&text={enc_text}'
    return f'''<div class="share-bar">
  <span class="share-label mono">Share this module</span>
  <a class="share-btn share-fb" href="{fb_url}" target="_blank" rel="noopener noreferrer" aria-label="Share on Facebook" title="Share on Facebook">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><path d="M15 8.5h2.5V5.2c-.43-.06-1.93-.2-3.67-.2-3.64 0-6.13 2.29-6.13 6.49v3.06H4v3.7h3.7V22h3.8v-3.75h3.55l.56-3.7h-4.1v-2.56c0-1.07.29-1.8 1.83-1.8Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>
  </a>
  <a class="share-btn share-x" href="{x_url}" target="_blank" rel="noopener noreferrer" aria-label="Share on X" title="Share on X">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M18.3 3H21l-6.4 7.3L22 21h-6.6l-5.2-6.6L4 21H1.3l6.9-7.8L1 3h6.7l4.7 6.1L18.3 3Zm-1.1 16.2h1.5L7 4.7H5.4l11.8 14.5Z" fill="currentColor"/></svg>
  </a>
  <button class="share-btn share-ig" type="button" data-share-url="{esc(page_url)}" onclick="shareInstagram(this)" aria-label="Copy link for Instagram" title="Copy link for Instagram">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="18" height="18" rx="5" stroke="currentColor" stroke-width="1.6"/><circle cx="12" cy="12" r="4" stroke="currentColor" stroke-width="1.6"/><circle cx="17.2" cy="6.8" r="1.1" fill="currentColor"/></svg>
  </button>
  <span class="share-toast" role="status" aria-live="polite">Link copied &mdash; paste it into your Instagram Story or post.</span>
</div>
<script>
function shareInstagram(btn) {{
  var url = btn.getAttribute('data-share-url');
  var toast = btn.parentElement.querySelector('.share-toast');
  function showToast() {{
    toast.classList.add('show');
    setTimeout(function(){{ toast.classList.remove('show'); }}, 2800);
  }}
  if (navigator.clipboard && navigator.clipboard.writeText) {{
    navigator.clipboard.writeText(url).then(showToast, showToast);
  }} else {{
    var ta = document.createElement('textarea');
    ta.value = url; document.body.appendChild(ta); ta.select();
    try {{ document.execCommand('copy'); }} catch(e) {{}}
    document.body.removeChild(ta);
    showToast();
  }}
}}
</script>
'''

def footer(prefix=''):
    return f'''<footer>
  <div class="wrap footer-inner">
    <a class="brand" href="{prefix}index.html"><span class="brand-mark">FD</span> Destiny Training Curriculum</a>
    <div class="fmeta">A free, independent training resource for Follett Destiny users &middot; Not affiliated with Follett Software</div>
  </div>
</footer>
</body>
</html>
'''

# ---------------------------------------------------------------
# Knowledge check widget (from module_content.py structured data)
# ---------------------------------------------------------------
def knowledge_check_html(m):
    mc = MC[m]
    parts = ['<div class="kcheck">', '<h2>Knowledge Check</h2>',
             '<p>Answer each question, then click to reveal the answer. Short-answer questions show key points to check your response against.</p>']
    for i, (q, opts, ans) in enumerate(mc['mcq'], 1):
        parts.append('<div class="kc-q">')
        parts.append(f'<p class="q-text">Q{i}. {esc(q)}</p>')
        parts.append('<ul>' + ''.join(f'<li>{esc(o)}</li>' for o in opts) + '</ul>')
        parts.append(f'<details class="reveal"><summary>Show answer</summary><div class="answer">Correct answer: <strong>{esc(ans)}</strong></div></details>')
        parts.append('</div>')
    n_start = len(mc['mcq']) + 1
    for i, (q, ans) in enumerate(mc['short_answer'], n_start):
        parts.append('<div class="kc-q">')
        parts.append(f'<p class="q-text">Q{i}. {esc(q)}</p>')
        parts.append(f'<details class="reveal"><summary>Show key points</summary><div class="answer">{esc(ans)}</div></details>')
        parts.append('</div>')

    parts.append('<div class="completion-box">')
    parts.append(f'<p><strong>Self-check threshold:</strong> aim for at least 7 of 8 points (80%) before moving to the next module.</p>')
    parts.append('<p><strong>Hands-on checklist</strong> — if you have access to a Destiny sandbox or live site, confirm you can do each of these:</p>')
    parts.append('<ul>')
    for item in mc['checklist']:
        parts.append(f'<li>☐ {esc(item)}</li>')
    parts.append('</ul>')
    parts.append('</div>')
    parts.append('</div>')
    return '\n'.join(parts)

# ---------------------------------------------------------------
# Works Cited
# ---------------------------------------------------------------
def works_cited_html(m):
    start, end = ranges[m]['wc']
    body = convert_blocks(blocks, start + 1, end)  # skip the "Module N Works Cited" heading itself
    return f'<div class="works-cited"><h2>Works Cited</h2>\n{body}\n</div>'

# ---------------------------------------------------------------
# Objectives box
# ---------------------------------------------------------------
def objectives_html(m):
    mc = MC[m]
    items = ''.join(f'<li>{CHECK_SVG}<span>{esc(o)}</span></li>' for o in mc['objectives'])
    return f'''<div class="objectives-box">
<h2>What You'll Learn</h2>
<ul>{items}</ul>
</div>'''

def meta_row_html(m, time_est):
    return f'''<div class="meta-row">
  <div class="meta-item"><span class="meta-label mono">Est. Time</span><span class="meta-value">{esc(time_est)}</span></div>
  <div class="meta-item"><span class="meta-label mono">Format</span><span class="meta-value">Self-paced reading + knowledge check</span></div>
</div>'''

# ---------------------------------------------------------------
# Video block
# ---------------------------------------------------------------
def video_html(videos):
    if not videos:
        return ''
    if len(videos) == 1:
        vid, vtitle = videos[0]
        return f'''<div class="video-block">
<div class="video-wrap"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{esc(vtitle)}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
<div class="video-caption">{esc(vtitle)}</div>
</div>'''
    cells = []
    for vid, vtitle in videos:
        cells.append(f'''<div>
<div class="video-wrap"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{esc(vtitle)}" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
<div class="video-caption">{esc(vtitle)}</div>
</div>''')
    return f'<div class="video-block"><div class="video-grid">{"".join(cells)}</div></div>'

# ---------------------------------------------------------------
# Module page
# ---------------------------------------------------------------
def build_module_page(m):
    meta = MODULE_META[m]
    mc = MC[m]
    intro_start, intro_end = ranges[m]['intro']
    core_start, core_end = ranges[m]['core']
    intro_html = convert_blocks(blocks, intro_start, intro_end)
    core_html = convert_blocks(blocks, core_start, core_end)

    prev_link = f'module-{m-1}.html' if m > 1 else None
    next_link = f'module-{m+1}.html' if m < 9 else None
    prev_title = MODULE_META[m-1]['title'] if m > 1 else None
    next_title = MODULE_META[m+1]['title'] if m < 9 else None

    nav_html = '<div class="module-nav">'
    if prev_link:
        nav_html += f'<a href="{prev_link}"><span class="nav-label">&larr; Previous</span><span class="nav-title">Module {m-1}: {esc(prev_title)}</span></a>'
    else:
        nav_html += '<div class="nav-spacer"></div>'
    if next_link:
        nav_html += f'<a href="{next_link}" class="nav-next"><span class="nav-label">Next &rarr;</span><span class="nav-title">Module {m+1}: {esc(next_title)}</span></a>'
    else:
        nav_html += '<a href="../glossary.html" class="nav-next"><span class="nav-label">Next &rarr;</span><span class="nav-title">Glossary of Key Terms</span></a>'
    nav_html += '</div>'

    time_est = mc['objectives'] and None
    # pull time/prereq text from module_content module_meta pattern used earlier isn't present; reconstruct simple map
    TIME_MAP = {1:"1.5 hours",2:"2 hours",3:"2.5 hours",4:"3 hours",5:"2 hours",6:"2 hours",7:"1.5 hours",8:"1.5 hours",9:"1 hour"}
    PREREQ_MAP = {1:"None",2:"Module 1",3:"Modules 1\u20132",4:"Modules 1\u20133",5:"Modules 1\u20134",6:"Modules 1\u20135",7:"Modules 1\u20136",8:"Modules 1\u20137",9:"Modules 1\u20138"}

    page = []
    page_url = f'modules/module-{m}.html'
    page.append(head(f"Module {m}: {meta['title']} — Destiny Training Curriculum",
                      meta['desc'], prefix='../',
                      canonical_path=page_url, og_image=f'assets/img/og/module-{m}.png'))
    page.append(topbar(prefix='../'))
    page.append(f'<div class="wrap breadcrumb"><a href="../index.html">Home</a> / <a href="../index.html#modules">Modules</a> / Module {m}</div>')
    page.append(f'''<div class="wrap module-header">
  <div class="call-no mono">CALL NO. {esc(meta["call"])}</div>
  <h1>Module {m}: {esc(meta["title"])}</h1>
  <p style="color:var(--ink-soft);font-size:15.5px;max-width:70ch;">{esc(meta["desc"])}</p>
  <div class="meta-row">
    <div class="meta-item"><span class="meta-label mono">Prerequisites</span><span class="meta-value">{esc(PREREQ_MAP[m])}</span></div>
    <div class="meta-item"><span class="meta-label mono">Est. Time</span><span class="meta-value">{esc(TIME_MAP[m])}</span></div>
    <div class="meta-item"><span class="meta-label mono">Format</span><span class="meta-value">Self-paced reading + knowledge check</span></div>
  </div>
  ''' + share_bar_html(SITE_URL + page_url, f"Module {m}: {meta['title']} — Destiny Training Curriculum") + '''
</div>''')
    page.append('<div class="wrap-narrow">')
    page.append(f'<div class="content-prose">{intro_html}</div>')
    page.append(objectives_html(m))
    page.append(video_html(meta['videos']))
    page.append(f'<div class="content-prose">{core_html}</div>')
    page.append(knowledge_check_html(m))
    page.append(works_cited_html(m))
    page.append(nav_html)
    page.append('</div>')
    page.append(footer(prefix='../'))
    return ''.join(page)

# ---------------------------------------------------------------
# Homepage
# ---------------------------------------------------------------
def build_index():
    cards = []
    for m in range(1, 10):
        meta = MODULE_META[m]
        TIME_MAP = {1:"1.5 hrs",2:"2 hrs",3:"2.5 hrs",4:"3 hrs",5:"2 hrs",6:"2 hrs",7:"1.5 hrs",8:"1.5 hrs",9:"1 hr"}
        cards.append(f'''<a class="module-card" href="modules/module-{m}.html">
  <div class="mc-top"><span class="mc-num mono">MODULE 0{m}</span><span class="mc-time">{TIME_MAP[m]}</span></div>
  <h3>{esc(meta["title"])}</h3>
  <p>{esc(meta["desc"])}</p>
  <span class="mc-cta">Start module &rarr;</span>
</a>''')

    page = []
    page.append(head("Follett Destiny LMS Training Curriculum — Free Resource for School Librarians",
                      "A free, independent 9-module Follett Destiny training curriculum for school librarians, updated for Destiny 24.0/23.5.",
                      prefix='', canonical_path='index.html', og_image='assets/img/og/home.png'))
    page.append(topbar(prefix=''))
    page.append('''<header class="hero">
  <div class="wrap">
    <span class="eyebrow"><span class="dot"></span>Free resource for school librarians</span>
    <h1>Learn Follett Destiny,<br><em>one module at a time.</em></h1>
    <p class="lede">A complete, independent 9-module training curriculum for Follett Destiny &mdash; updated for Destiny 24.0/23.5 &mdash; with learning objectives, video walkthroughs, self-check knowledge checks, and a glossary. Free to use, module by module.</p>
    <div class="hero-ctas">
      <a href="modules/module-1.html" class="btn btn-primary">Start with Module 1</a>
      <a href="#modules" class="btn btn-ghost">Browse all 9 modules &darr;</a>
    </div>
    <div class="hero-meta">
      <span><span class="dot"></span>9 structured modules</span>
      <span><span class="dot"></span>Video walkthroughs</span>
      <span><span class="dot"></span>Self-check knowledge checks</span>
      <span><span class="dot"></span>Glossary of key terms</span>
    </div>
  </div>
</header>''')

    page.append(f'''<section class="wrap" id="modules">
  <div class="section-head">
    <span class="eyebrow">The curriculum</span>
    <h2>Nine modules, start to finish</h2>
    <p>Work through them in order, or jump straight to the topic you need.</p>
  </div>
  <div class="module-grid">
    {"".join(cards)}
  </div>
</section>''')

    page.append('''<section class="wrap" style="border-top:1px solid var(--stone-line);">
  <div class="section-head">
    <span class="eyebrow">What's included</span>
    <h2>More than a manual</h2>
  </div>
  <div class="included-grid">
    <div class="included-item"><div class="ii-icon">''' + CHECK_SVG.replace('#2A4B8D','#191B1F') + '''</div><div><h4>Measurable learning objectives</h4><p>Every module opens with concrete, checkable outcomes.</p></div></div>
    <div class="included-item"><div class="ii-icon">''' + CHECK_SVG.replace('#2A4B8D','#191B1F') + '''</div><div><h4>Video walkthroughs</h4><p>Real tutorial videos embedded alongside the written material.</p></div></div>
    <div class="included-item"><div class="ii-icon">''' + CHECK_SVG.replace('#2A4B8D','#191B1F') + '''</div><div><h4>Self-check knowledge checks</h4><p>Multiple-choice and scenario questions with answers you can reveal on demand.</p></div></div>
    <div class="included-item"><div class="ii-icon">''' + CHECK_SVG.replace('#2A4B8D','#191B1F') + '''</div><div><h4>Glossary of key terms</h4><p>MARC, SIS, FERPA, WCAG, CREW/MUSTIE and more, defined in one place.</p></div></div>
  </div>
</section>''')

    page.append('''<section class="wrap" style="border-top:1px solid var(--stone-line);">
  <div class="section-head">
    <span class="eyebrow">Who it's for</span>
    <h2>Built for the library, not just the librarian</h2>
  </div>
  <div class="who-grid">
    <div class="who-card"><h3>New school librarians</h3><p>Onboarding into Destiny for the first time &mdash; IB or non-IB, single-site or district.</p></div>
    <div class="who-card"><h3>Library directors &amp; coordinators</h3><p>Standardizing training across multiple sites so every hire gets the same bar.</p></div>
    <div class="who-card"><h3>Library assistants &amp; substitutes</h3><p>Anyone who needs working fluency in circulation, patrons, or cataloging.</p></div>
  </div>
</section>''')

    page.append('''<section class="wrap-narrow" style="border-top:1px solid var(--stone-line);">
  <div class="section-head">
    <span class="eyebrow">About the creator</span>
    <h2>Written by a working school librarian</h2>
  </div>
  <div style="background:#fff;border:1px solid var(--stone-line);border-radius:var(--radius);padding:26px 28px;box-shadow:var(--card-shadow);">
    <p style="color:var(--ink-soft);font-size:15px;margin:0;">This curriculum was written by a working IB Secondary School Librarian, covering the exact Destiny workflows a modern school library runs on day to day &mdash; cataloging, circulation, inventory, and reporting. It's maintained independently, outside of any vendor relationship with Follett Software, and updated as Destiny's own releases change.</p>
  </div>
</section>

<section class="wrap-narrow" style="border-top:1px solid var(--stone-line);">
  <div class="section-head">
    <span class="eyebrow">About this resource</span>
    <h2>Independent, not official</h2>
    <p>This is an independently written training resource for Destiny users, sourced from and citing official Follett documentation, Follett Community resources, and publicly available tutorial videos. It is not published, sold, or endorsed by Follett Software. Trademarks (Follett Destiny&reg;, Destiny Discover&reg;, etc.) belong to their respective owners.</p>
  </div>
</section>''')

    page.append(footer(prefix=''))
    return ''.join(page)

# ---------------------------------------------------------------
# Glossary page
# ---------------------------------------------------------------
def build_glossary():
    items = []
    for term, definition in GLOSSARY:
        items.append(f'<div class="glossary-item"><dt>{esc(term)}</dt><dd>{esc(definition)}</dd></div>')
    page = []
    page.append(head("Glossary of Key Terms — Destiny Training Curriculum",
                      "Definitions of acronyms and terms used throughout the Follett Destiny training curriculum.",
                      prefix='', canonical_path='glossary.html', og_image='assets/img/og/home.png'))
    page.append(topbar(prefix=''))
    page.append('<div class="wrap breadcrumb"><a href="index.html">Home</a> / Glossary</div>')
    page.append('''<div class="wrap-narrow" style="padding:24px 0 60px;">
  <h1>Glossary of Key Terms</h1>
  <p style="color:var(--ink-soft);">Definitions of acronyms and terms used throughout Modules 1&ndash;9, in alphabetical order.</p>
  <div class="glossary-list">''')
    page.append(''.join(items))
    page.append('</div></div>')
    page.append(footer(prefix=''))
    return ''.join(page)

# ---------------------------------------------------------------
if __name__ == '__main__':
    with open('../index.html', 'w', encoding='utf-8') as f:
        f.write(build_index())
    with open('../glossary.html', 'w', encoding='utf-8') as f:
        f.write(build_glossary())
    for m in range(1, 10):
        with open(f'../modules/module-{m}.html', 'w', encoding='utf-8') as f:
            f.write(build_module_page(m))
    print("Site generated.")
