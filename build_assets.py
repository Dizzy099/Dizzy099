# -*- coding: utf-8 -*-
"""Generate every SVG on the profile README, in a dark and a light variant.

    python build_assets.py

Writes assets/<name>-dark.svg and assets/<name>-light.svg. Edit the words here,
never in the SVGs -- the next run overwrites them.

GitHub loads these through <img>, so: no scripts, no external fonts or images.
CSS keyframes and SMIL do run. Text is visible by default -- animations only use
`backwards` fill or loop over already-visible marks -- so a renderer that skips
animation still shows everything. Motion is removed under prefers-reduced-motion.

Numbers shown here come from evidence/METRICS_LEDGER.md (GREEN or qualified AMBER)
and portfolio/chunk-router/README.md. Schematic marks (grey bars in the ledger
card) are deliberately unlabelled so they cannot be read as real figures.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent / "assets"
W = 760  # every card shares one width so the page reads as one system

THEMES = {
    "dark": dict(bg="#0d1117", card="#161b22", border="#30363d", text="#e6edf3",
                 soft="#c9d1d9", muted="#8b949e", faint="#21262d", film="#010409",
                 blue="#58a6ff", purple="#bc8cff", green="#3fb950", orange="#f0883e",
                 pink="#f778ba", teal="#39c5cf", red="#f85149"),
    "light": dict(bg="#ffffff", card="#f6f8fa", border="#d0d7de", text="#1f2328",
                  soft="#31373d", muted="#59636e", faint="#eaeef2", film="#24292f",
                  blue="#0969da", purple="#8250df", green="#1a7f37", orange="#bc4c00",
                  pink="#bf3989", teal="#1b7c83", red="#cf222e"),
}

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

BASE_CSS = (
    ".s{font-family:%s}.m{font-family:%s}" % (SANS, MONO)
    + ".in{animation:in .5s ease-out backwards}"
    + "@keyframes in{from{opacity:0;transform:translateY(6px)}}"
    + "@media (prefers-reduced-motion:reduce){.in{animation:none}.mv{display:none}}"
)


def e(s):
    return escape(str(s))


def txt(x, y, s, size, fill, cls="s", weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{e(s)}</text>')


def box(x, y, w, h, fill, stroke="none", rx=8, sw=1.5, extra=""):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def arrow(x1, y1, x2, y2, color, dash=False, sw=2):
    d = ' stroke-dasharray="5 5"' if dash else ""
    # arrowhead drawn by hand: markers are fine too, but this keeps colours per-theme simple
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx1, hy1 = x2 - 9 * math.cos(a - .45), y2 - 9 * math.sin(a - .45)
    hx2, hy2 = x2 - 9 * math.cos(a + .45), y2 - 9 * math.sin(a + .45)
    return (f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="{sw}" fill="none"{d}/>'
            f'<path d="M{hx1:.1f} {hy1:.1f}L{x2} {y2}L{hx2:.1f} {hy2:.1f}" stroke="{color}" '
            f'stroke-width="{sw}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def svg(w, h, title, desc, body, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="t d"><title id="t">{e(title)}</title><desc id="d">{e(desc)}</desc>'
            f'<style>{BASE_CSS}</style>'
            f'{box(1, 1, w - 2, h - 2, t["card"], t["border"], rx=14)}{body}</svg>\n')


# ============================================================================ hero
def hero(t):
    h = 350
    a = t["blue"]
    stats = [("~200", "REST endpoints"), ("4", "LLM providers"),
             ("2,600+", "tests in suite"), ("70 → 94", "Lighthouse score")]
    parts = [
        # dotted engineering-paper texture on the right
        f'<defs><pattern id="g" width="18" height="18" patternUnits="userSpaceOnUse">'
        f'<circle cx="2" cy="2" r="1.2" fill="{t["border"]}"/></pattern></defs>',
        box(470, 2, W - 472, 214, "url(#g)", rx=0),
        txt(40, 58, "AWANISH MISHRA  ·  BACKEND ENGINEER  ·  NOIDA, INDIA", 14, a, "m in", 600,
            extra='letter-spacing="1.5"'),
        txt(40, 118, "I build the machinery", 46, t["text"], "s in", 800,
            extra='style="animation-delay:.15s"'),
        f'<text x="40" y="170" class="s in" font-size="46" font-weight="800" fill="{t["text"]}" '
        f'style="animation-delay:.3s">behind <tspan fill="{a}">AI products.</tspan></text>',
        txt(40, 206, "LLM routing · async pipelines · billing that adds up", 19, t["muted"], "s in",
            extra='style="animation-delay:.45s"'),
    ]
    # little live graph: a request hopping across four nodes, one of which fails over
    nodes = [(540, 70), (620, 110), (700, 70), (620, 180), (700, 170)]
    edges = [(0, 1), (1, 2), (1, 3), (3, 4)]
    for i, j in edges:
        (x1, y1), (x2, y2) = nodes[i], nodes[j]
        parts.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{t["border"]}" stroke-width="2"/>')
    cols = [a, a, t["red"], t["green"], t["green"]]
    for (x, y), c in zip(nodes, cols):
        parts.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{t["card"]}" stroke="{c}" stroke-width="3"/>')
    parts.append(txt(700, 46, "503", 12, t["red"], "m", 700, "middle"))
    parts.append(txt(620, 214, "fallback", 12, t["green"], "m", 700, "middle"))
    parts.append(
        f'<circle class="mv" r="5" fill="{a}"><animateMotion dur="4s" repeatCount="indefinite" '
        f'keyPoints="0;0.25;0.5;0.75;1" keyTimes="0;0.25;0.5;0.75;1" calcMode="linear" '
        f'path="M540 70L620 110L700 70L620 110L620 180L700 170"/></circle>')
    # stat strip
    x, tw, gap, y = 40, 157, 11, 244
    for i, (big, label) in enumerate(stats):
        xi = x + i * (tw + gap)
        parts.append(box(xi, y, tw, 74, t["bg"], t["border"], rx=10,
                         extra=f'class="in" style="animation-delay:{.6 + i * .12:.2f}s"'))
        parts.append(txt(xi + 16, y + 36, big, 26, a, "s", 800))
        parts.append(txt(xi + 16, y + 58, label, 13, t["muted"], "m"))
    return svg(W, h, "Awanish Mishra: I build the machinery behind AI products",
               "Backend engineer in Noida, India. LLM routing, async pipelines and billing that adds up. "
               "About 200 REST endpoints, 4 LLM providers in one fallback chain, a suite of 2,600+ tests, "
               "and Lighthouse 70 to 94 on a live store.", "".join(parts), t)


# ======================================================================= card frame
def card(t, accent, kicker, title, body, pills, visual, h=380, title_str="", desc=""):
    parts = [box(1, 1, 6, h - 2, accent, rx=3)]
    parts.append(txt(36, 50, kicker, 13, accent, "m", 700, extra='letter-spacing="1.4"'))
    for i, line in enumerate(title):
        parts.append(txt(36, 92 + i * 36, line, 30, t["text"], "s", 800))
    y0 = 92 + len(title) * 36 + 14
    for i, line in enumerate(body):
        parts.append(txt(36, y0 + i * 26, line, 17, t["soft"], "s"))
    px = 36
    for p in pills:
        w = 16 + len(p) * 7.9
        parts.append(box(px, h - 56, w, 28, t["faint"], rx=14, sw=0))
        parts.append(txt(px + w / 2, h - 37, p, 13, t["muted"], "m", 600, "middle"))
        px += w + 8
    parts.append(f'<g transform="translate(404 34)">{visual}</g>')
    return svg(W, h, title_str or " ".join(title), desc, "".join(parts), t)


# ------------------------------------------------------------------ 1. AI engine
def card_engine(t):
    a, v = t["blue"], []
    def node(x, y, label, c):
        return box(x, y, 88, 42, t["bg"], c, rx=10, sw=2) + txt(x + 44, y + 27, label, 15, t["text"], "m", 700, "middle")
    v += [node(0, 24, "brief", t["border"]), node(122, 24, "LLM", a), node(244, 24, "image", a),
          node(244, 150, "video", a)]
    v += [arrow(88, 45, 120, 45, t["muted"]), arrow(210, 45, 242, 45, t["muted"]),
          arrow(288, 66, 288, 148, t["muted"]), arrow(166, 66, 166, 96, t["muted"])]
    chain = [("claude", "503", t["red"], True), ("openai", "ok", t["green"], False),
             ("gemini", "", t["border"], False), ("deepseek", "", t["border"], False)]
    for i, (name, st, c, dead) in enumerate(chain):
        y = 100 + i * 40
        v.append(box(112, y, 110, 32, t["bg"], c, rx=16, sw=2))
        fill = t["muted"] if not st else t["text"]
        v.append(txt(128, y + 21, name, 14, fill, "m", 600))
        if st:
            v.append(txt(212, y + 21, st, 12, c, "m", 700, "end"))
        if dead:
            v.append(f'<path d="M126 {y + 16}H188" stroke="{c}" stroke-width="2"/>')
    v.append(txt(0, 128, "fallback", 13, t["muted"], "m"))
    v.append(txt(0, 146, "chain", 13, t["muted"], "m"))
    v.append(arrow(62, 140, 106, 140, t["muted"], dash=True))
    v.append(f'<path d="M224 116 C 244 118, 244 150, 224 156" stroke="{t["green"]}" stroke-width="2" '
             f'fill="none" stroke-dasharray="4 4"/>')
    v.append(f'<circle class="mv" r="5" fill="{a}"><animateMotion dur="3.6s" repeatCount="indefinite" '
             f'path="M44 45H166V110H166V156H166V66H288V171"/></circle>')
    v.append(txt(0, 292, "a new model = an admin row, not a deploy", 13, t["muted"], "m"))
    return card(t, a, "01 · TINGG.AI · IN PRODUCTION",
                ["Multi-provider", "AI workflow engine"],
                ["Workflows are graphs of LLM, image", "and video steps. When a provider",
                 "fails, the call falls through to the", "next one instead of failing the run."],
                ["Django", "Celery", "4 LLM APIs"], "".join(v),
                desc="Workflow graph brief to LLM to image to video. The LLM step uses a fallback chain: "
                     "Claude returns 503, OpenAI answers, Gemini and DeepSeek stand by. "
                     "A new model is enabled from an admin row, with no deploy.")


# ------------------------------------------------------------------ 2. video
def card_video(t):
    a, v = t["purple"], []
    stages = ["idea", "script", "board", "frames", "clips"]
    for i, s in enumerate(stages):
        x = i * 68
        v.append(box(x, 0, 60, 30, t["bg"], a if i else t["border"], rx=15, sw=2,
                     extra=f'class="in" style="animation-delay:{i * .15:.2f}s"'))
        v.append(txt(x + 30, 20, s, 12, t["text"], "m", 700, "middle"))
    # film strip
    v.append(box(0, 58, 340, 150, t["film"], rx=6, sw=0))
    for i in range(17):
        v.append(box(8 + i * 20, 64, 10, 8, t["bg"], rx=2, sw=0, extra='opacity=".5"'))
        v.append(box(8 + i * 20, 194, 10, 8, t["bg"], rx=2, sw=0, extra='opacity=".5"'))
    tints = [t["purple"], t["pink"], t["blue"]]
    for i, c in enumerate(tints):
        x = 12 + i * 110
        v.append(box(x, 82, 96, 104, c, rx=4, sw=0, extra='opacity=".28"'))
        v.append(f'<circle cx="{x + 70}" cy="104" r="10" fill="{c}" opacity=".9"/>')
        v.append(f'<path d="M{x} 186L{x + 34} 140L{x + 58} 166L{x + 76} 150L{x + 96} 172V186Z" fill="{c}" opacity=".75"/>')
        v.append(txt(x + 6, 100, f"scene {i + 1}", 12, "#ffffff", "m", 700))
        if i < 2:
            # last frame of scene i becomes first frame of scene i+1
            v.append(box(x + 82, 82, 14, 104, "#ffffff", rx=2, sw=0, extra='opacity=".55"'))
            v.append(box(x + 110, 82, 14, 104, "#ffffff", rx=2, sw=0, extra='opacity=".55"'))
            v.append(f'<path d="M{x + 89} 232 C {x + 89} 252, {x + 117} 252, {x + 117} 232" '
                     f'stroke="{t["muted"]}" stroke-width="2" fill="none"/>')
            v.append(arrow(x + 117, 240, x + 117, 214, t["muted"]))
    v.append(txt(0, 276, "each scene opens on the last frame of", 13, t["muted"], "m"))
    v.append(txt(0, 294, "the one before, so the story stays whole", 13, t["muted"], "m"))
    return card(t, a, "02 · TINGG.AI · GENERATIVE VIDEO",
                ["Idea to video,", "one scene at a time"],
                ["Script, storyboard, frames and clips,", "run as async jobs: submit, poll,",
                 "store to S3. Scenes can be re-rolled,", "versioned, restored or cancelled."],
                ["Celery", "S3", "Claude", "image + video APIs"], "".join(v),
                desc="Five stages: idea, script, storyboard, frames, clips. A film strip of three scenes, "
                     "where each scene starts on the last frame of the scene before it.")


# ------------------------------------------------------------------ 3. metering
def card_meter(t):
    a, v = t["green"], []
    cols = [("provider", 0), ("tokens", 96), ("cost", 170), ("latency", 232), ("run", 304)]
    for name, x in cols:
        v.append(txt(x, 14, name, 12, t["muted"], "m", 700))
    v.append(f'<path d="M0 24H340" stroke="{t["border"]}"/>')
    rows = [("claude", 44, 30, 40, 18), ("openai", 36, 22, 28, 18),
            ("gemini", 58, 34, 50, 18), ("image", 24, 40, 56, 18)]
    for i, (p, a1, a2, a3, a4) in enumerate(rows):
        y = 34 + i * 30
        g = [txt(0, y + 14, p, 13, t["text"], "m", 600),
             box(96, y + 4, a1, 12, t["border"], rx=3, sw=0),
             box(170, y + 4, a2, 12, a, rx=3, sw=0, extra='opacity=".75"'),
             box(232, y + 4, a3, 12, t["border"], rx=3, sw=0),
             box(304, y + 4, a4, 12, t["border"], rx=3, sw=0)]
        v.append(f'<g class="in" style="animation-delay:{i * .25:.2f}s">{"".join(g)}</g>')
    v.append(f'<path d="M0 158H340" stroke="{t["border"]}"/>')
    v.append(txt(0, 186, "CREDITS · APPEND-ONLY LEDGER", 12, t["muted"], "m", 700, extra='letter-spacing="1"'))
    v.append(txt(0, 212, "monthly allowance  → spent first, resets", 13, t["text"], "m"))
    v.append(box(0, 220, 340, 16, t["faint"], rx=8, sw=0))
    v.append(f'<rect x="0" y="220" height="16" rx="8" fill="{a}" width="120">'
             f'<animate attributeName="width" values="340;120" dur="2.2s" fill="freeze"/></rect>')
    v.append(txt(0, 262, "purchased credit   → kept until used", 13, t["text"], "m"))
    v.append(box(0, 270, 340, 16, t["faint"], rx=8, sw=0))
    v.append(box(0, 270, 230, 16, t["teal"], rx=8, sw=0))
    return card(t, a, "03 · TINGG.AI · USAGE & BILLING",
                ["Every token has", "a price and an owner"],
                ["Each model call records tokens, cost,", "latency and the run that spent it.",
                 "I found cache tokens billed at zero,", "fixed it, and re-priced history safely."],
                ["append-only ledger", "reconciliation"], "".join(v),
                desc="A schematic usage log with columns provider, tokens, cost, latency and run. "
                     "Below, two credit buckets: a monthly allowance that is spent first and resets, "
                     "and purchased credit kept until used.")


# ------------------------------------------------------------------ 4. AutoDM
def card_autodm(t):
    a, v = t["pink"], []
    def bubble(x, y, w, label, c, faded=False):
        op = ' opacity=".55"' if faded else ""
        return (f'<g{op}>{box(x, y, w, 44, t["bg"], c, rx=12, sw=2)}'
                f'<path d="M{x + 16} {y + 44}l6 10 8-10" fill="{t["bg"]}" stroke="{c}" stroke-width="2"/>'
                f'{txt(x + w / 2, y + 27, label, 14, t["text"], "m", 700, "middle")}</g>')
    v.append(bubble(0, 20, 96, "comment", a))
    v.append(box(128, 14, 96, 58, t["bg"], t["orange"], rx=10, sw=2))
    v.append(txt(176, 40, "claim", 15, t["text"], "m", 700, "middle"))
    v.append(txt(176, 58, "UNIQUE", 11, t["orange"], "m", 700, "middle"))
    v.append(box(256, 20, 84, 44, t["bg"], t["green"], rx=10, sw=2))
    v.append(txt(298, 47, "DM sent", 14, t["text"], "m", 700, "middle"))
    v.append(arrow(98, 42, 124, 42, t["muted"]))
    v.append(arrow(226, 42, 252, 42, t["muted"]))
    v.append(bubble(0, 128, 96, "same one", t["border"], faded=True))
    v.append(f'<path d="M98 150 C 150 150, 176 120, 176 76" stroke="{t["red"]}" stroke-width="2" '
             f'fill="none" stroke-dasharray="5 5"/>')
    v.append(f'<g stroke="{t["red"]}" stroke-width="3" stroke-linecap="round">'
             f'<path d="M168 92l16 16M184 92l-16 16"/></g>')
    v.append(txt(196, 106, "duplicate refused", 13, t["red"], "m", 700))
    v.append(txt(196, 124, "by the database", 13, t["red"], "m"))
    v.append(box(0, 196, 340, 64, t["faint"], rx=10, sw=0))
    v.append(txt(16, 222, "hourly reconciler", 13, t["text"], "m", 700))
    v.append(txt(16, 244, "frees claims stuck > 30 min with no send", 12, t["muted"], "m"))
    v.append(f'<circle class="mv" r="5" fill="{a}"><animateMotion dur="3s" repeatCount="indefinite" '
             f'path="M48 42H298"/></circle>')
    v.append(txt(0, 292, "Meta allows one reply per comment", 13, t["muted"], "m"))
    return card(t, a, "04 · CREATOR PLATFORM · AUTOMATION",
                ["Comment in,", "DM out: exactly once"],
                ["Instagram webhooks trigger replies", "and DMs in real time, plus leads,",
                 "funnels and link analytics. Built", "with several hundred unit tests."],
                ["Meta Graph API", "webhooks", "MySQL"], "".join(v),
                desc="A comment is claimed through a UNIQUE database column before the DM is sent. "
                     "A duplicate delivery of the same comment is refused by the database. "
                     "An hourly reconciler frees claims stuck for more than 30 minutes with no send.")


# ------------------------------------------------------------------ 5. live store
def ring(cx, cy, r, value, color, t, label, delay):
    import math
    c = 2 * math.pi * r
    on = c * value / 100
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["faint"]}" stroke-width="10"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="10" '
            f'stroke-linecap="round" stroke-dasharray="{on:.1f} {c:.1f}" transform="rotate(-90 {cx} {cy})">'
            f'<animate attributeName="stroke-dasharray" from="0 {c:.1f}" to="{on:.1f} {c:.1f}" '
            f'dur="1.4s" begin="{delay}s" fill="freeze"/></circle>'
            + txt(cx, cy + 12, value, 34, t["text"], "s", 800, "middle")
            + txt(cx, cy + r + 30, label, 13, t["muted"], "m", 700, "middle"))


def card_store(t):
    a, v = t["orange"], []
    v.append(txt(0, 10, "LIGHTHOUSE PERFORMANCE · CATALOGUE", 12, t["muted"], "m", 700, extra='letter-spacing="1"'))
    v.append(ring(62, 86, 52, 70, t["orange"], t, "before", 0))
    v.append(ring(262, 86, 52, 94, t["green"], t, "after", .4))
    v.append(arrow(134, 86, 190, 86, t["muted"], sw=3))
    v.append(txt(0, 214, "LAYOUT SHIFT (CLS) · LOWER IS BETTER", 12, t["muted"], "m", 700, extra='letter-spacing="1"'))
    v.append(box(0, 228, 300, 18, t["orange"], rx=9, sw=0))
    v.append(txt(308, 242, "0.75", 13, t["text"], "m", 700))
    v.append(box(0, 258, 9, 18, t["green"], rx=4, sw=0))
    v.append(txt(18, 272, "0.024", 13, t["text"], "m", 700))
    v.append(txt(0, 300, "reserved grid space before products load", 12, t["muted"], "m"))
    return card(t, a, "05 · FREELANCE · LIVE E-COMMERCE",
                ["A live store,", "made fast and safe"],
                ["PhonePe payments, Shiprocket tracking,", "server-side pricing rules. Closed a",
                 "NoSQL-injection path to admin.", "134 commits across 3 repos."],
                ["Node.js", "Express", "MongoDB", "Angular"], "".join(v),
                desc="Lighthouse performance on catalogue pages rose from 70 to 94. "
                     "Layout shift fell from 0.75 to 0.024 by reserving grid space before products load.")


# ------------------------------------------------------------------ 6. chunk-router
def card_router(t):
    a, v = t["teal"], []
    xs = [44, 142, 240, 338]
    labels = ["24", "240", "2.4k", "24k"]
    brute = [0.17, 0.16, 1.74, 6.43]
    chroma = [3.96, 4.18, 4.42, 4.40]
    Y = lambda ms: 230 - ms / 7 * 196
    v.append(box(240, 26, 98, 204, a, rx=0, sw=0, extra='opacity=".10"'))
    v.append(txt(289, 222, "crossover", 12, a, "m", 700, "middle"))
    for ms in (0, 2, 4, 6):
        v.append(f'<path d="M36 {Y(ms):.0f}H340" stroke="{t["faint"]}"/>')
        v.append(txt(28, Y(ms) + 4, ms, 12, t["muted"], "m", 400, "end"))
    for x, l in zip(xs, labels):
        v.append(txt(x, 252, l, 12, t["muted"], "m", 600, "middle"))
    v.append(txt(190, 274, "vectors in the index (log scale)", 12, t["muted"], "m", 400, "middle"))
    v.append(txt(0, 18, "query ms", 12, t["muted"], "m", 700))

    def line(vals, c, name, ly, lx):
        pts = " ".join(f"{x},{Y(ms):.1f}" for x, ms in zip(xs, vals))
        dots = "".join(f'<circle cx="{x}" cy="{Y(ms):.1f}" r="4.5" fill="{c}"/>' for x, ms in zip(xs, vals))
        return (f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="3" '
                f'stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0">'
                f'<animate attributeName="stroke-dashoffset" from="1" to="0" dur="1.6s" fill="freeze"/></polyline>'
                f'{dots}' + txt(lx, ly, name, 13, c, "m", 700, "end" if lx > 300 else "start"))
    v.append(line(chroma, t["orange"], "chromadb", Y(4.18) - 12, 150))
    v.append(line(brute, a, "brute force", Y(6.43) + 5, xs[-1] - 12))
    v.append(txt(0, 304, "top-1 routing: 69% semantic vs 31% lexical", 13, t["text"], "m", 600))
    return card(t, a, "06 · SIDE PROJECT · MEASURED, NOT ASSUMED",
                ["Do you even need", "a vector database?"],
                ["Routes document chunks to a taxonomy", "with embeddings, then benchmarks brute",
                 "force against ChromaDB. Below a few", "thousand vectors, brute force wins."],
                ["Python", "ChromaDB", "MiniLM"], "".join(v),
                desc="Query time in milliseconds against index size. Brute force: 0.17, 0.16, 1.74, 6.43 ms "
                     "at 24, 240, 2,400 and 24,000 vectors. ChromaDB: 3.96, 4.18, 4.42, 4.40 ms. "
                     "The lines cross between 2,400 and 24,000 vectors. Top-1 routing accuracy 69% semantic "
                     "versus 31% lexical, on a small synthetic corpus.")


# ============================================================================ bug board
BUGS = [
    ("14 images instead of 7", "Double-click race. Row locks and", "idempotency keys; retries made safe."),
    ("Every video request: 500", "A 480 s poll ran in a 120 s web", "worker. Moved it back onto Celery."),
    ("Uploads stuck “processing”", "Queue nobody consumed + early acks.", "Late acks and a stuck-job reaper."),
    ("Costs drifting from prices", "Cache tokens priced at zero. Fixed,", "then re-priced history, dry run first."),
    ("Only the newest rule fires", "Wrong sort order. Tests proven to", "fail if the bug ever comes back."),
    ("5 auth flaws, my own feature", "Found in my own pre-release review;", "reported with fixes before merge."),
]


def board(t):
    tw, th, gx, gy, top = 334, 124, 20, 16, 78
    h = top + 3 * th + 2 * gy + 34
    parts = [txt(36, 50, "BUG HUNTS · SYMPTOM → ROOT CAUSE → FIX", 13, t["red"], "m", 700,
                 extra='letter-spacing="1.4"')]
    for i, (sym, f1, f2) in enumerate(BUGS):
        x = 36 + (i % 2) * (tw + gx)
        y = top + (i // 2) * (th + gy)
        g = [box(x, y, tw, th, t["bg"], t["border"], rx=12),
             box(x, y + 14, 4, 30, t["red"], rx=2, sw=0),
             txt(x + 20, y + 36, sym, 20, t["text"], "s", 800),
             txt(x + 20, y + 70, "FIX", 11, t["green"], "m", 800, extra='letter-spacing="1.2"'),
             txt(x + 52, y + 70, f1, 15, t["soft"], "s"),
             txt(x + 52, y + 94, f2, 15, t["soft"], "s")]
        parts.append(f'<g class="in" style="animation-delay:{i * .12:.2f}s">{"".join(g)}</g>')
    desc = " ".join(f"{s}: {a} {b}" for s, a, b in BUGS)
    return svg(W, h, "Bug hunts: six production bugs and their fixes", desc, "".join(parts), t)


ASSETS = {"hero": hero, "card-engine": card_engine, "card-video": card_video,
          "card-meter": card_meter, "card-autodm": card_autodm, "card-store": card_store,
          "card-router": card_router, "bugs": board}

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for stale in ("pipeline-dark.svg", "pipeline-light.svg"):
        (OUT / stale).unlink(missing_ok=True)
    for name, fn in ASSETS.items():
        for theme, t in THEMES.items():
            (OUT / f"{name}-{theme}.svg").write_text(fn(t), encoding="utf-8")
    print("wrote", len(ASSETS) * 2, "files:", ", ".join(ASSETS))
