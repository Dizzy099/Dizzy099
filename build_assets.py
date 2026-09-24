# -*- coding: utf-8 -*-
"""Generate the profile README's SVGs in a dark and a light variant.

    python build_assets.py

Writes assets/hero-{dark,light}.svg and assets/pipeline-{dark,light}.svg.
Edit the text here, never in the SVGs -- the next run overwrites them.

GitHub loads these through <img>, so: no scripts, no external fonts, no
external images. CSS keyframes inside the SVG do run. Text is visible by
default (animations only use backwards fill), so a renderer that skips
animation still shows everything. Every animation ends in
its visible state and is switched off under prefers-reduced-motion.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent / "assets"

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", text="#e6edf3",
                 muted="#8b949e", accent="#58a6ff", ok="#3fb950", warn="#d29922",
                 dots=("#ff5f57", "#febc2e", "#28c840")),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", text="#1f2328",
                  muted="#59636e", accent="#0969da", ok="#1a7f37", warn="#9a6700",
                  dots=("#ff5f57", "#febc2e", "#28c840")),
}

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

# ------------------------------------------------------------------ hero terminal
# Each line: list of (text, colour-key) spans. Kept under ~60 characters so the
# SVG stays legible when GitHub scales it down on a phone.
def _step(label, detail, status, colour="ok"):
    """One trace row with the status column aligned (monospace padding)."""
    return [("  " + label.ljust(7), "muted"), (detail.ljust(29), "text"), (status, colour)]


HERO_LINES = [
    [("$ ", "muted"), ("whoami", "text")],
    [("Awanish Mishra", "accent"), (" · backend engineer, AI products", "text")],
    [],
    [("$ ", "muted"), ("trace ", "text"), ("POST /workflows/run", "warn")],
    _step("lock", "idempotency key held", "ok"),
    _step("plan", "DAG: llm → image → video", "ok"),
    _step("route", "claude 503 → openai", "fallback", "warn"),
    _step("queue", "celery, acks_late", "ok"),
    _step("meter", "tokens · cost · latency", "logged"),
    [("✓ 200 ", "ok"), ("correct on the bad day, not just the demo", "muted")],
]


def hero(t):
    w, line_h, top, left = 760, 27, 78, 36
    h = top + line_h * len(HERO_LINES) + 30
    rows = []
    for i, spans in enumerate(HERO_LINES):
        if not spans:
            continue
        y = top + i * line_h
        tspans = "".join(
            f'<tspan fill="{t[c]}">{escape(s)}</tspan>' for s, c in spans)
        rows.append(
            f'<text class="ln" style="animation-delay:{0.25 + i * 0.32:.2f}s" '
            f'x="{left}" y="{y}" xml:space="preserve">{tspans}</text>')
    last_y = top + (len(HERO_LINES) - 1) * line_h
    last_len = sum(len(s) for s, _ in HERO_LINES[-1])
    cursor_x = left + 17 * 0.6 * last_len  # just after the final line
    d1, d2, d3 = t["dots"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">
<title id="t">Awanish Mishra, backend engineer for AI products</title>
<desc id="d">A terminal tracing one AI workflow request: idempotency lock, DAG plan, provider fallback from Claude to OpenAI, Celery queue, and usage metering, ending in HTTP 200.</desc>
<style>
  text {{ font-family: {MONO}; font-size: 17px; }}
  .ln {{ animation: in .35s ease-out backwards; }}
  .cur {{ animation: blink 1.1s steps(1) infinite; }}
  @keyframes in {{ from {{ opacity: 0; transform: translateX(-6px); }} to {{ opacity: 1; transform: none; }} }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{ .ln {{ animation: none; }} .cur {{ animation: none; }} }}
</style>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="{t['bg']}" stroke="{t['border']}" stroke-width="1.5"/>
<path d="M1 13a12 12 0 0 1 12-12h{w - 26}a12 12 0 0 1 12 12v27H1z" fill="{t['panel']}"/>
<line x1="1" y1="40" x2="{w - 1}" y2="40" stroke="{t['border']}"/>
<circle cx="24" cy="21" r="6" fill="{d1}"/><circle cx="44" cy="21" r="6" fill="{d2}"/><circle cx="64" cy="21" r="6" fill="{d3}"/>
<text x="{w / 2}" y="26" text-anchor="middle" fill="{t['muted']}" style="font-size:14px">awanish@prod: ~</text>
{chr(10).join(rows)}
<rect class="cur" x="{min(cursor_x, w - 40):.0f}" y="{last_y - 15}" width="10" height="19" fill="{t['accent']}"/>
</svg>
'''


# ------------------------------------------------------------- request pipeline
# Vertical on purpose: a horizontal diagram shrinks to unreadable on a phone.
STAGES = [
    ("01", "API + tenant auth", "DRF · RBAC · workspace scoping · audit log"),
    ("02", "Idempotency guard", "row locks + keys · state-aware retry"),
    ("03", "Workflow planner", "DAG of LLM, image and video nodes"),
    ("04", "Provider router", "Claude → OpenAI → Gemini → DeepSeek"),
    ("05", "Async workers", "Celery · late acks · stuck-job reaper"),
    ("06", "Usage ledger", "tokens · cost · latency per call · credits"),
]


def pipeline(t):
    w, box_h, gap, top, x0 = 720, 72, 30, 74, 52
    bw = w - 2 * x0
    h = top + len(STAGES) * box_h + (len(STAGES) - 1) * gap + 34
    parts = []
    for i, (num, title, detail) in enumerate(STAGES):
        y = top + i * (box_h + gap)
        parts.append(
            f'<rect x="{x0}" y="{y}" width="{bw}" height="{box_h}" rx="10" '
            f'fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="1.5"/>'
            f'<text x="{x0 + 22}" y="{y + 44}" fill="{t["accent"]}" class="n">{num}</text>'
            f'<text x="{x0 + 76}" y="{y + 31}" fill="{t["text"]}" class="h">{escape(title)}</text>'
            f'<text x="{x0 + 76}" y="{y + 56}" fill="{t["muted"]}" class="s">{escape(detail)}</text>')
        if i < len(STAGES) - 1:
            ya = y + box_h
            parts.append(
                f'<path d="M{w / 2} {ya + 4}v{gap - 10}" stroke="{t["border"]}" stroke-width="2"/>'
                f'<path d="M{w / 2 - 6} {ya + gap - 10}l6 7 6-7" fill="none" stroke="{t["border"]}" stroke-width="2"/>')
    spine_top, spine_bot = top + box_h / 2, top + (len(STAGES) - 1) * (box_h + gap) + box_h / 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">
<title id="t">The shape of the AI backends I build</title>
<desc id="d">Six stages a request passes through: API with tenant auth, idempotency guard, workflow planner, provider router with fallback, async Celery workers, and a usage ledger.</desc>
<style>
  text {{ font-family: {MONO}; }}
  .h {{ font-size: 19px; font-weight: 700; }}
  .s {{ font-size: 15px; }}
  .n {{ font-size: 22px; font-weight: 700; }}
  .cap {{ font-size: 14px; letter-spacing: .08em; }}
  @media (prefers-reduced-motion: reduce) {{ .pulse {{ display: none; }} }}
</style>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="{t['bg']}" stroke="{t['border']}" stroke-width="1.5"/>
<text x="{x0}" y="44" fill="{t['muted']}" class="cap">ONE REQUEST, SIX PLACES IT CAN FAIL</text>
{''.join(parts)}
<line x1="26" y1="{spine_top}" x2="26" y2="{spine_bot}" stroke="{t['border']}" stroke-width="2" stroke-dasharray="3 5"/>
{''.join(f'<circle cx="26" cy="{top + i * (box_h + gap) + box_h / 2}" r="4" fill="{t["border"]}"/>' for i in range(len(STAGES)))}
<circle class="pulse" r="6" fill="{t['ok']}" cx="26" cy="{spine_top}">
  <animate attributeName="cy" values="{spine_top};{spine_bot};{spine_bot}" keyTimes="0;0.85;1" dur="5s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.85;1" dur="5s" repeatCount="indefinite"/>
</circle>
</svg>
'''


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        (OUT / f"hero-{name}.svg").write_text(hero(t), encoding="utf-8")
        (OUT / f"pipeline-{name}.svg").write_text(pipeline(t), encoding="utf-8")
    print("wrote", sorted(p.name for p in OUT.glob("*.svg")))
