"""Generate the profile terminal assets using only Python's standard library.

Run: python scripts/build-terminal.py
The SVGs animate without JavaScript, external fonts, or an image service.
"""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERIOD = 16


def render(mobile=False, static=False):
    width, height = (560, 508) if mobile else (900, 420)
    step, font_size = (10.5, 18) if mobile else (10, 17)
    prompt = "zures@tunisia:~$ "
    lines = [
        ("whoami", 100, 0.5, True),
        ("Iheb Mahfoudh", 132, 1.6, False),
        ("Cybersecurity Engineer", 160, 1.9, False),
        ("cat profile.txt", 214, 2.8, True),
        ("role   Penetration Tester / Red Teamer", 250, 4.6, False),
    ]
    if mobile:
        lines += [
            ("focus  Web / Networks / Active Directory", 282, 5.0, False),
            ("       Privilege escalation / Reversing", 314, 5.4, False),
            ("labs   CTFs / Hack The Box", 346, 5.8, False),
            ("email  zures001@gmail.com", 378, 6.2, False),
        ]
        cursor_y = 434
    else:
        lines += [
            ("focus  Web / Networks / Active Directory / Privilege escalation", 282, 5.0, False),
            ("labs   CTFs / Hack The Box / Reverse engineering", 314, 5.5, False),
            ("email  zures001@gmail.com", 346, 6.0, False),
        ]
        cursor_y = 390

    styles = [
        "text { font-family: 'Cascadia Code', Consolas, 'Liberation Mono', monospace; white-space: pre; }",
        "@keyframes blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }",
        ".cursor { animation: blink 1s step-end infinite; }",
    ]
    definitions, body = [], []
    for index, (value, y, start, command) in enumerate(lines):
        text = prompt + value if command else value
        extent = len(text) * step
        duration = len(value) * 0.075 if command else 0.16
        begin, end = start / PERIOD * 100, (start + duration) / PERIOD * 100
        styles += [
            f"@keyframes show{index} {{ 0%, {begin:.3f}% {{ opacity: 0; }} {begin + 0.01:.3f}%, 100% {{ opacity: 1; }} }}",
            f".line{index} {{ animation: show{index} {PERIOD}s linear infinite; }}",
        ]
        if command:
            initial = len(prompt) * step
            styles += [
                f"@keyframes type{index} {{ 0%, {begin:.3f}% {{ width: {initial}px; }} {end:.3f}%, 100% {{ width: {extent}px; }} }}",
                f".clip{index} {{ animation: type{index} {PERIOD}s steps({len(value)}, end) infinite; }}",
                f"@keyframes move{index} {{ 0%, {begin:.3f}% {{ transform: translateX({initial}px); }} {end:.3f}%, 100% {{ transform: translateX({extent}px); }} }}",
                f"@keyframes caret{index} {{ 0%, {begin:.3f}% {{ opacity: 0; }} {begin + 0.01:.3f}%, {end:.3f}% {{ opacity: 1; }} {end + 0.01:.3f}%, 100% {{ opacity: 0; }} }}",
                f".typing{index} {{ animation: move{index} {PERIOD}s steps({len(value)}, end) infinite, caret{index} {PERIOD}s linear infinite; }}",
            ]
            definitions.append(f'<clipPath id="clip{index}"><rect class="clip{index}" x="28" y="{y-23}" width="{extent}" height="30" /></clipPath>')
            content = f'<tspan fill="#9fef00">{escape(prompt)}</tspan><tspan fill="#f0f6fc">{escape(value)}</tspan>'
            clip = f' clip-path="url(#clip{index})"'
        else:
            content = escape(text)
            clip = ""
        body.append(f'<text class="line{index}" x="28" y="{y}" font-size="{font_size}" fill="#c9d1d9" textLength="{extent}" lengthAdjust="spacingAndGlyphs"{clip}>{content}</text>')
        if command:
            body.append(f'<rect class="typing{index} typing" x="30" y="{y-17}" width="9" height="21" fill="#9fef00" opacity="0" />')

    styles += [
        f"@keyframes ready {{ 0%, 42% {{ opacity: 0; }} 42.01%, 100% {{ opacity: 1; }} }}",
        f".ready {{ animation: ready {PERIOD}s linear infinite; }}",
        "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } .typing, .cursor { display: none; } }",
    ]
    body.append(f'<g class="ready"><text x="28" y="{cursor_y}" font-size="{font_size}" fill="#9fef00" textLength="{len(prompt)*step}" lengthAdjust="spacingAndGlyphs">{escape(prompt)}</text><rect class="cursor" x="{28+len(prompt)*step}" y="{cursor_y-17}" width="9" height="21" fill="#9fef00" /></g>')
    if static:
        styles = [styles[0], ".typing, .cursor { display: none; }"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">
  <title id="title">ZuresTN's animated profile terminal</title>
  <desc id="description">Commands reveal Iheb Mahfoudh, Cybersecurity Engineer and Penetration Tester / Red Teamer. Focus: web, networks, Active Directory, privilege escalation, and reverse engineering. Labs: CTFs and Hack The Box. Email: zures001@gmail.com. Animation repeats every 16 seconds; reduced motion shows the complete profile.</desc>
  <defs>{''.join(definitions)}</defs>
  <style>{''.join(styles)}</style>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" rx="14" fill="#0d1117" stroke="#30363d" />
  <path d="M15 1H{width-15}Q{width-1} 1 {width-1} 15V52H1V15Q1 1 15 1Z" fill="#161b22" />
  <path d="M1 52H{width-1}" stroke="#30363d" />
  <circle cx="28" cy="27" r="6" fill="#ff5f57" />
  <circle cx="50" cy="27" r="6" fill="#febc2e" />
  <circle cx="72" cy="27" r="6" fill="#28c840" />
  <text x="{width/2}" y="32" fill="#8b949e" font-size="13" text-anchor="middle">zures@tunisia — profile</text>
  {''.join(body)}
</svg>
'''


if __name__ == "__main__":
    (ROOT / "assets").mkdir(exist_ok=True)
    for mobile in (False, True):
        for static in (False, True):
            name = "terminal" + ("-mobile" if mobile else "") + ("-static" if static else "") + ".svg"
            (ROOT / "assets" / name).write_text(render(mobile, static), encoding="utf-8")
            print(f"Generated assets/{name}")
