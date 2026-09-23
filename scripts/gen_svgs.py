import math, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)
BG = "#0B1020"; GRID = "#1A2340"; CYAN = "#22D3EE"; BLUE = "#3B82F6"; VIOLET = "#A78BFA"
INK = "#E6EDF3"; MUTED = "#8B95A7"; PINK = "#F472B6"
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"


def write(name, body):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(body)


def frame(w, h, inner, defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
<defs>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
    <path d="M32 0H0V32" stroke="{GRID}" stroke-width="1"/>
    <animateTransform attributeName="patternTransform" type="translate" from="0 0" to="32 32" dur="8s" repeatCount="indefinite"/>
  </pattern>
  <radialGradient id="vignette" cx="50%" cy="50%" r="75%">
    <stop offset="60%" stop-color="{BG}" stop-opacity="0"/>
    <stop offset="100%" stop-color="{BG}" stop-opacity="1"/>
  </radialGradient>
  <clipPath id="panel"><rect width="{w}" height="{h}" rx="16"/></clipPath>
  {defs}
</defs>
<g clip-path="url(#panel)">
<rect width="{w}" height="{h}" fill="{BG}"/>
<rect width="{w}" height="{h}" fill="url(#grid)"/>
<rect width="{w}" height="{h}" fill="url(#vignette)"/>
{inner}
</g>
<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="15.5" stroke="{GRID}"/>
</svg>
'''


def glow(fid, sd):
    return (f'<filter id="{fid}" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="{sd}" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


# ---------------------------------------------------------------- header
def header():
    W, H = 1000, 320
    cx, cy = 805, 160
    sats = [(655, 70, "xlsx"), (640, 190, "legacy"), (700, 280, "email"),
            (930, 62, "notes"), (955, 180, "paper"), (905, 282, "xlsx"), (805, 32, "csv")]
    lines, nodes, dots = [], [], []
    for i, (x, y, lab) in enumerate(sats):
        d = f"M{x},{y} L{cx},{cy}"
        L = math.hypot(cx - x, cy - y)
        delay = 0.6 + i * 0.15
        lines.append(f'<path d="{d}" stroke="{BLUE}" stroke-opacity=".45" stroke-width="1.5" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}">'
                     f'<animate attributeName="stroke-dashoffset" to="0" dur="0.8s" begin="{delay:.2f}s" fill="freeze"/></path>')
        nodes.append(f'''<g opacity="0">
  <animate attributeName="opacity" to="1" dur="0.4s" begin="{delay-0.3:.2f}s" fill="freeze"/>
  <rect x="{x-15}" y="{y-11}" width="30" height="22" rx="4" fill="#111a33" stroke="{VIOLET}" stroke-width="1.2"/>
  <path d="M{x-15} {y-3}H{x+15}M{x-15} {y+4}H{x+15}M{x-5} {y-11}V{y+11}M{x+5} {y-11}V{y+11}" stroke="{VIOLET}" stroke-opacity=".5"/>
  <text x="{x}" y="{y+26}" fill="{MUTED}" font-family="{MONO}" font-size="10" text-anchor="middle">{lab}</text>
</g>''')
        for k in range(2):
            b = 1.6 + i * 0.37 + k * 1.4
            dots.append(f'''<circle r="3" fill="{CYAN}" opacity="0">
  <animateMotion path="{d}" dur="1.4s" begin="{b:.2f}s" repeatCount="indefinite" keyPoints="0;1" keyTimes="0;1" calcMode="spline" keySplines=".5 0 .5 1"/>
  <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.8;1" dur="1.4s" begin="{b:.2f}s" repeatCount="indefinite"/>
</circle>''')
    cloud = f"M{cx-48},{cy+22} a22,22 0 0 1 2,-44 a30,30 0 0 1 56,-14 a24,24 0 0 1 38,24 a20,20 0 0 1 -4,34 z"
    rings = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="40" stroke="{CYAN}" stroke-width="1.5" opacity="0">'
        f'<animate attributeName="r" values="40;95" dur="3s" begin="{2+k:.1f}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".6;0" dur="3s" begin="{2+k:.1f}s" repeatCount="indefinite"/></circle>'
        for k in range(3))
    hub = f'''{rings}
<g filter="url(#glow)">
  <path d="{cloud}" fill="#0f2447" stroke="{CYAN}" stroke-width="2.2" stroke-linejoin="round" stroke-dasharray="330" stroke-dashoffset="330">
    <animate attributeName="stroke-dashoffset" to="0" dur="1.2s" begin="0.2s" fill="freeze"/>
  </path>
</g>
<text x="{cx+2}" y="{cy+10}" fill="{INK}" font-family="{MONO}" font-size="15" font-weight="700" text-anchor="middle" opacity="0">1 org<animate attributeName="opacity" to="1" dur=".5s" begin="1.2s" fill="freeze"/></text>'''

    phrases = ["Solutions Architect", "Spreadsheets → one platform", "Board-room to backlog", "Apex · LWC · Flow"]
    n = len(phrases); per = 3.0; cyc = n * per; e = 0.35 / cyc
    rot = []
    for i, p in enumerate(phrases):
        a = i / n; b = (i + 1) / n
        kt = f"0;{a:.4f};{a+e:.4f};{b-e:.4f};{b:.4f};1"
        rot.append(f'''<text x="60" y="206" fill="{CYAN}" font-family="{MONO}" font-size="22" opacity="0">&gt; {p}
  <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{cyc}s" begin="1.8s" repeatCount="indefinite"/>
  <animateTransform attributeName="transform" type="translate" values="0 10;0 10;0 0;0 0;0 -10;0 -10" keyTimes="{kt}" dur="{cyc}s" begin="1.8s" repeatCount="indefinite"/>
</text>''')
    defs = f'''
  <linearGradient id="shine" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="{INK}"/><stop offset=".42" stop-color="{INK}"/>
    <stop offset=".5" stop-color="{CYAN}"/><stop offset=".58" stop-color="{INK}"/><stop offset="1" stop-color="{INK}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;1 0" keyTimes="0;.4;1" dur="5s" begin="1.5s" repeatCount="indefinite"/>
  </linearGradient>
  <clipPath id="wipe"><rect x="50" y="80" width="0" height="100">
    <animate attributeName="width" to="560" dur="1.1s" begin="0.3s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".7 0 .3 1"/></rect></clipPath>
  <linearGradient id="bar"><stop stop-color="{CYAN}"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></linearGradient>
  {glow("glow", 3)}'''
    inner = f'''
<text x="60" y="72" fill="{MUTED}" font-family="{MONO}" font-size="13" letter-spacing="3" opacity="0">HELLO, I’M<animate attributeName="opacity" to="1" dur=".6s" begin="0.1s" fill="freeze"/></text>
<g clip-path="url(#wipe)">
  <text x="58" y="150" fill="url(#shine)" font-family="{SANS}" font-size="62" font-weight="800" letter-spacing="-1">Nathan Marchant</text>
</g>
<rect x="60" y="100" width="4" height="60" fill="{CYAN}" opacity="0">
  <animate attributeName="x" from="60" to="590" dur="1.1s" begin="0.3s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".7 0 .3 1"/>
  <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.05;.9;1" dur="1.3s" begin="0.3s" fill="freeze"/>
</rect>
{''.join(rot)}
<rect x="60" y="236" width="0" height="2" fill="url(#bar)"><animate attributeName="width" to="420" dur="1s" begin="1.4s" fill="freeze"/></rect>
<text x="60" y="266" fill="{MUTED}" font-family="{MONO}" font-size="13" opacity="0">9 years · Sales · Service · Experience · Marketing Cloud<animate attributeName="opacity" to="1" dur=".8s" begin="1.8s" fill="freeze"/></text>
{''.join(lines)}
{''.join(nodes)}
{''.join(dots)}
{hub}
'''
    write("header.svg", frame(W, H, inner, defs))


# ---------------------------------------------------------------- stats
def stats():
    W, H = 1000, 170
    cards = [("9", "years on Salesforce", CYAN, 0.9, [0, 3, 6]),
             ("10+", "orgs worked on", BLUE, 0.7, [0, 4, 8]),
             ("100+", "projects shipped", VIOLET, 0.85, [0, 40, 80]),
             ("1,400+", "properties, one org", PINK, 0.95, [0, 500, 1000])]
    cw, gap = 226, 24; x0 = (W - (4 * cw + 3 * gap)) / 2
    C = 2 * math.pi * 30
    out = []
    for i, (val, lab, col, pct, steps) in enumerate(cards):
        x = x0 + i * (cw + gap); y = 25; d = 0.2 + i * 0.2
        rx, ry = x + 50, y + 60
        out.append(f'''<g opacity="0">
  <animate attributeName="opacity" to="1" dur=".5s" begin="{d:.1f}s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 14" to="0 0" dur=".6s" begin="{d:.1f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/>
  <rect x="{x}" y="{y}" width="{cw}" height="120" rx="12" fill="#10182e" stroke="{GRID}"/>
  <circle cx="{rx}" cy="{ry}" r="30" stroke="{GRID}" stroke-width="6"/>
  <circle cx="{rx}" cy="{ry}" r="30" stroke="{col}" stroke-width="6" stroke-linecap="round" stroke-dasharray="{C:.1f}" stroke-dashoffset="{C:.1f}" transform="rotate(-90 {rx} {ry})">
    <animate attributeName="stroke-dashoffset" to="{C*(1-pct):.1f}" dur="1.4s" begin="{d+0.3:.1f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".3 0 .2 1"/>
  </circle>
  <circle cx="{rx}" cy="{ry}" r="6" fill="{col}"><animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/></circle>''')
        seq = [f"{s:,}" for s in steps] + [val]
        t = d + 0.3
        for j, s in enumerate(seq):
            b = t + j * 0.3
            vis = (f'<set attributeName="opacity" to="1" begin="{b:.2f}s"/>' if j == len(seq) - 1 else
                   f'<set attributeName="opacity" to="1" begin="{b:.2f}s" end="{b+0.3:.2f}s"/>')
            out.append(f'  <text x="{x+100}" y="{y+68}" fill="{INK}" font-family="{SANS}" font-size="30" font-weight="800" opacity="0">{s}{vis}</text>')
        out.append(f'  <text x="{x+100}" y="{y+90}" fill="{MUTED}" font-family="{SANS}" font-size="12.5">{lab}</text>\n</g>')
    write("stats.svg", frame(W, H, "\n".join(out)))


# ---------------------------------------------------------------- timeline
def timeline():
    W, H = 1000, 270
    y0, xa, xb = 145, 60, 940
    ya, yb = 2012, 2026.4
    X = lambda yr: xa + (yr - ya) / (yb - ya) * (xb - xa)
    ms = [(2012, "Junior IT Admin", "Magna International"),
          (2015, "IT Enquiries", "Uni of Greenwich"),
          (2017, "Systems Support", "Harbour Rock Capital"),
          (2019, "Software Architect", "Harbour Rock Capital"),
          (2023, "Systems Dev Manager", "+ Apex Infinity founding team"),
          (2026, "Salesforce Admin", "The Royal Institution")]
    out = [f'''<text x="{xa}" y="36" fill="{MUTED}" font-family="{MONO}" font-size="13" letter-spacing="3">THE ROUTE SO FAR</text>
<path d="M{xa},{y0} H{xb}" stroke="{GRID}" stroke-width="4" stroke-linecap="round"/>
<path d="M{xa},{y0} H{xb}" stroke="url(#tl)" stroke-width="4" stroke-linecap="round" stroke-dasharray="{xb-xa}" stroke-dashoffset="{xb-xa}">
  <animate attributeName="stroke-dashoffset" to="0" dur="2.6s" begin=".2s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".4 0 .2 1"/></path>
<circle r="5" fill="{INK}" filter="url(#g2)" opacity="0">
  <animateMotion path="M{xa},{y0} H{xb}" dur="4s" begin="3s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.9;1" dur="4s" begin="3s" repeatCount="indefinite"/></circle>''']
    for yr in range(2012, 2027):
        out.append(f'<text x="{X(yr):.1f}" y="{y0+28}" fill="#4a5678" font-family="{MONO}" font-size="10" text-anchor="middle">’{str(yr)[2:]}</text>')
    cols = [MUTED, MUTED, VIOLET, BLUE, CYAN, PINK]
    for i, (yr, role, org) in enumerate(ms):
        x = X(yr)
        # keySplines .4 0 .2 1 is ease-out-ish; approximate reveal time as linear-ish but a bit early
        frac = (x - xa) / (xb - xa)
        d = 0.2 + 2.6 * (frac ** 1.6)
        up = i % 2 == 0
        ty = y0 - 62 if up else y0 + 66
        ly1, ly2 = (y0 - 14, y0 - 40) if up else (y0 + 36, y0 + 46)
        anchor = "start" if i == 0 else ("end" if i == len(ms) - 1 else "middle")
        tx = x - 8 if i == 0 else (x + 8 if i == len(ms) - 1 else x)
        c = cols[i]
        out.append(f'''<g opacity="0">
  <animate attributeName="opacity" to="1" dur=".4s" begin="{d:.2f}s" fill="freeze"/>
  <circle cx="{x:.1f}" cy="{y0}" r="8" fill="{BG}" stroke="{c}" stroke-width="3"/>
  <path d="M{x:.1f},{ly1} V{ly2}" stroke="{c}" stroke-opacity=".6" stroke-dasharray="2 3"/>
  <text x="{tx:.1f}" y="{ty}" fill="{INK}" font-family="{SANS}" font-size="14" font-weight="700" text-anchor="{anchor}">{role}</text>
  <text x="{tx:.1f}" y="{ty+17}" fill="{MUTED}" font-family="{SANS}" font-size="11.5" text-anchor="{anchor}">{org}</text>
</g>''')
    x = X(2026)
    out.append(f'''<circle cx="{x:.1f}" cy="{y0}" r="8" stroke="{PINK}" stroke-width="2" opacity="0">
  <animate attributeName="r" values="8;22" dur="1.8s" begin="3s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values=".8;0" dur="1.8s" begin="3s" repeatCount="indefinite"/></circle>''')
    defs = f'''<linearGradient id="tl" x1="{xa}" x2="{xb}" gradientUnits="userSpaceOnUse">
  <stop stop-color="{MUTED}"/><stop offset=".4" stop-color="{VIOLET}"/><stop offset=".72" stop-color="{BLUE}"/><stop offset=".88" stop-color="{CYAN}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
{glow("g2", 3)}'''
    write("timeline.svg", frame(W, H, "\n".join(out), defs))


# ---------------------------------------------------------------- footer
def footer():
    W, H = 1000, 150
    period = 2 * math.pi * 80  # wave wavelength in px
    waves = []
    for k, (col, op, dur, amp, yb) in enumerate([(VIOLET, .35, 18, 12, 112), (BLUE, .45, 13, 10, 120), (CYAN, .55, 9, 8, 128)]):
        pts = [f"M0,{yb}"]
        s = 0.0
        while s <= W + period + 20:
            pts.append(f"L{s:.0f},{yb + amp * math.sin(s / 80 + k):.1f}")
            s += 20
        pts.append(f"L{W+period+20:.0f},{H} L0,{H} Z")
        waves.append(f'''<path d="{' '.join(pts)}" fill="{col}" fill-opacity="{op}">
  <animateTransform attributeName="transform" type="translate" from="0 0" to="-{period:.1f} 0" dur="{dur}s" repeatCount="indefinite"/></path>''')
    inner = f'''<text x="{W/2}" y="58" fill="{INK}" font-family="{SANS}" font-size="30" font-weight="800" text-anchor="middle">Let’s build something that sticks.</text>
<text x="{W/2}" y="84" fill="{MUTED}" font-family="{MONO}" font-size="13" text-anchor="middle">architecture · delivery · or just Salesforce in general</text>
{''.join(waves)}'''
    write("footer.svg", frame(W, H, inner))


# ---------------------------------------------------------------- pebble showcase
PEB = os.path.expanduser("~/Projects/pebble")


def b64(path):
    import base64
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def cycler(shots, x, y, w, h, per=2.6, clip=None, begin=0.6):
    n = len(shots); cyc = n * per; e = 0.3 / cyc
    out = []
    for i, p in enumerate(shots):
        a = i / n; b = (i + 1) / n
        if i == 0:  # first frame visible at rest so a static render still shows something
            vals, kt = "1;1;0;0;1", f"0;{b-e:.4f};{b:.4f};{1-e:.4f};1"
        else:
            vals, kt = "0;0;1;1;0;0", f"0;{a:.4f};{a+e:.4f};{b-e:.4f};{b:.4f};1"
        op = "1" if i == 0 else "0"
        cp = f' clip-path="url(#{clip})"' if clip else ""
        out.append(f'<image href="{b64(p)}" x="{x}" y="{y}" width="{w}" height="{h}" style="image-rendering:pixelated" opacity="{op}"{cp}>'
                   f'<animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="{cyc}s" begin="{begin}s" repeatCount="indefinite"/></image>')
    return "\n".join(out)


def pebble():
    W, H = 1000, 400
    dd = f"{PEB}/dicey-depths/docs/screenshots"
    rect_shots = [f"{dd}/{s}.png" for s in ("splash", "combat", "floor", "enemy-wasp", "class-select", "robot-cpu")]
    round_shots = [f"{dd}/round-combat.png", f"{PEB}/orbi-face/screenshots/orbi-face.png",
                   f"{PEB}/roulette/screenshots/gabbro.png", f"{PEB}/orbital-face/screenshots/chalk.png"]
    # Pebble Time 2 body
    tx, ty, sw, sh = 110, 86, 200, 228
    time2 = f'''<g>
  <animateTransform attributeName="transform" type="translate" values="0 0;0 -6;0 0" dur="5s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/>
  <rect x="{tx-50}" y="{ty-38}" width="{sw+100}" height="{sh+76}" rx="34" fill="#1c2233" stroke="#2c3550" stroke-width="2"/>
  <rect x="{tx-46}" y="{ty-34}" width="{sw+92}" height="{sh+68}" rx="30" fill="none" stroke="#3a4566" stroke-opacity=".5"/>
  <rect x="{tx-56}" y="{ty+30}" width="8" height="46" rx="3" fill="#2c3550"/>
  <rect x="{tx+sw+48}" y="{ty+10}" width="8" height="40" rx="3" fill="#2c3550"/>
  <rect x="{tx+sw+48}" y="{ty+94}" width="8" height="40" rx="3" fill="#2c3550"/>
  <rect x="{tx+sw+48}" y="{ty+178}" width="8" height="40" rx="3" fill="#2c3550"/>
  <rect x="{tx-6}" y="{ty-6}" width="{sw+12}" height="{sh+12}" rx="6" fill="#000"/>
  {cycler(rect_shots, tx, ty, sw, sh)}
  <rect x="{tx}" y="{ty}" width="{sw}" height="{sh}" fill="url(#glare)"/>
</g>'''
    rcx, rcy, rr = 850, 200, 92
    round2 = f'''<g>
  <animateTransform attributeName="transform" type="translate" values="0 -5;0 3;0 -5" dur="6s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/>
  <circle cx="{rcx}" cy="{rcy}" r="{rr+34}" fill="#1c2233" stroke="#2c3550" stroke-width="2"/>
  <circle cx="{rcx}" cy="{rcy}" r="{rr+26}" fill="none" stroke="{PINK}" stroke-opacity=".35" stroke-width="2" stroke-dasharray="4 10">
    <animateTransform attributeName="transform" type="rotate" from="0 {rcx} {rcy}" to="360 {rcx} {rcy}" dur="30s" repeatCount="indefinite"/></circle>
  <rect x="{rcx+rr+30}" y="{rcy-60}" width="8" height="30" rx="3" fill="#2c3550"/>
  <rect x="{rcx+rr+30}" y="{rcy-15}" width="8" height="30" rx="3" fill="#2c3550"/>
  <rect x="{rcx+rr+30}" y="{rcy+30}" width="8" height="30" rx="3" fill="#2c3550"/>
  <rect x="{rcx-rr-38}" y="{rcy-15}" width="8" height="30" rx="3" fill="#2c3550"/>
  <circle cx="{rcx}" cy="{rcy}" r="{rr+4}" fill="#000"/>
  {cycler(round_shots, rcx-rr, rcy-rr, 2*rr, 2*rr, per=3.2, clip="roundclip", begin=1.4)}
</g>'''
    # a die tumbling across the middle
    pips = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)],
            4: [(-1, -1), (1, -1), (-1, 1), (1, 1)], 5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)],
            6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}
    faces = []
    order = [6, 3, 5, 1, 4, 2]
    for i, f in enumerate(order):
        a, b = i / 6, (i + 1) / 6
        vals, kt = ("1;1;0;0" , f"0;{b:.4f};{b+0.0001:.4f};1") if i == 0 else ("0;0;1;1;0;0", f"0;{a:.4f};{a+0.0001:.4f};{b:.4f};{b+0.0001:.4f};1")
        if i == 5:
            vals, kt = "0;0;1;1", f"0;{a:.4f};{a+0.0001:.4f};1"
        dots = "".join(f'<circle cx="{dx*11}" cy="{dy*11}" r="4" fill="{BG}"/>' for dx, dy in pips[f])
        faces.append(f'<g opacity="{1 if i == 0 else 0}">{dots}<animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="3s" calcMode="discrete" repeatCount="indefinite"/></g>')
    die = f'''<g transform="translate(520 305)">
  <g><animateTransform attributeName="transform" type="rotate" values="0;90;180;270;360" dur="3s" repeatCount="indefinite"/>
    <rect x="-24" y="-24" width="48" height="48" rx="10" fill="{INK}" stroke="{CYAN}" stroke-width="2"/>
    {''.join(faces)}
  </g>
</g>'''
    txt = f'''<text x="392" y="92" fill="{MUTED}" font-family="{MONO}" font-size="13" letter-spacing="3">AFTER HOURS · 2014 → 2026</text>
<text x="392" y="136" fill="{INK}" font-family="{SANS}" font-size="34" font-weight="800">Dicey Depths</text>
<text x="392" y="166" fill="{CYAN}" font-family="{MONO}" font-size="15">&gt; a dice roguelike for your wrist</text>
<text x="392" y="204" fill="{MUTED}" font-family="{SANS}" font-size="13.5">Roll first, then decide. 4 cards, 4 dice,</text>
<text x="392" y="224" fill="{MUTED}" font-family="{SANS}" font-size="13.5">3 floors, permadeath. Written in C</text>
<text x="392" y="244" fill="{MUTED}" font-family="{SANS}" font-size="13.5">for the Pebble Time 2 and Round 2.</text>'''
    defs = f'''<clipPath id="roundclip"><circle cx="{rcx}" cy="{rcy}" r="{rr}"/></clipPath>
<linearGradient id="glare" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff" stop-opacity=".10"/><stop offset=".35" stop-color="#fff" stop-opacity="0"/></linearGradient>'''
    write("pebble.svg", frame(W, H, time2 + round2 + txt + die, defs))


header(); stats(); timeline(); footer(); pebble()
print("done")
