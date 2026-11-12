"""Render a project's data_flow.mmd with mermaid-cli and place it on its page.

The diagram is drawn in the site's palette (flow_config.json), the colours are swapped for the site's CSS
variables so it follows the light and dark themes, and the section is written between data-flow markers
just above the page's last section. Re-running replaces the section.

Usage: python build_flow.py <page.html> <project dir> "<intro sentence>" "<long description for screen readers>"
The arguments used for each page are kept in flows.json.
Needs mermaid-cli:  MMDC=path/to/mmdc  (and optionally PUPPETEER_CFG=puppeteer.json)
"""
import os, re, subprocess, sys, tempfile
page, proj, intro, desc = sys.argv[1:5]
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
slug = os.path.basename(proj.rstrip("/")); sid = "flow-" + re.sub(r"[^a-z0-9]", "", slug)
out = os.path.join(tempfile.mkdtemp(), "flow.svg")
cmd = [os.environ.get("MMDC", "mmdc"), "-i", f"{proj}/data_flow.mmd", "-o", out, "-c", f"{here}/flow_config.json", "-b", "transparent", "-I", sid]
if os.environ.get("PUPPETEER_CFG"): cmd += ["-p", os.environ["PUPPETEER_CFG"]]
subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
svg = open(out, encoding="utf-8").read()
for h, v in {"#f1f2ec": "var(--paper)", "#e6e9dd": "var(--paper-2)", "#1b241d": "var(--ink)", "#4c5a4f": "var(--ink-2)",
             "#6d7a3a": "var(--olive)", "#2e4a34": "var(--forest)", "#c7ccbb": "var(--rule)"}.items():
    svg = re.sub(h, v, svg, flags=re.I)
svg = svg.replace('role="graphics-document document"', 'role="img" aria-hidden="true"', 1)
A, B = "<!-- data-flow:start -->", "<!-- data-flow:end -->"
sec = f'''{A}
  <section id="data-flow">
    <style>
      .flow-fig {{ margin: 0; border: 1px solid var(--rule); background: var(--paper); padding: clamp(.75rem, 2vw, 1.5rem); overflow-x: auto; }}
      .flow-fig svg {{ display: block; min-width: 760px; height: auto; margin-inline: auto; }}
      .flow-fig svg .label, .flow-fig svg .label span, .flow-fig svg .label p {{ font: 400 14px/1.5 var(--body); letter-spacing: 0; text-transform: none; }}
      .flow-fig svg .label b {{ font-weight: 600; }}
      .flow-note {{ font-size: 0.875rem; color: var(--ink-2); margin: 1rem 0 0; max-width: 60ch; }}
    </style>
    <div class="wrap">
      <div class="section-head">
        <span class="label">Data flow</span>
        <div>
          <h2>Where the data came from</h2>
          <p>{intro}</p>
        </div>
      </div>
      <figure class="flow-fig" role="img" aria-label="Flowchart. {desc}">
{svg}
      </figure>
      <p class="flow-note">Drawn with Mermaid. The diagram's source is <a href="https://github.com/krauskajames/krauskajames.github.io/blob/main/projects/{slug}/data_flow.mmd">data_flow.mmd</a> in the site's repository.</p>
    </div>
  </section>
  {B}
'''
def place(path):
    s = open(path, encoding="utf-8").read()
    if A in s: s = s[: s.index(A)] + sec.rstrip("\n") + s[s.index(B) + len(B):]
    else:
        end = s.rindex("</main>") if "</main>" in s else len(s)
        i = s.rindex("<section", 0, end); i = s.rindex("\n", 0, i) + 1
        s = s[:i] + sec + "\n" + s[i:]
    open(path, "w", encoding="utf-8").write(s)
place(page)
body = f"{proj}/page_body.html"
if os.path.exists(body): place(body)
print("ok", page, f"{len(svg) / 1024:.0f} KB", re.search(r'viewBox="[\d. -]+ ([\d.]+) ([\d.]+)"', svg).groups())
