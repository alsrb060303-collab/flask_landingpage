# -*- coding: utf-8 -*-
"""
서비스 소개 이미지 생성기 (static/images/service-*.jpg)

SVG 로 그린 뒤 Chromium 으로 래스터화한다. 벡터 기반이라 크기를 키워도 깨지지 않고,
아래 PALETTE 의 색상 값만 바꾸면 전체 톤을 한 번에 갈아엎을 수 있다.

실행:
    pip install playwright && playwright install chromium
    python tools/gen_service_images.py

출력:
    static/images/service-api.jpg
    static/images/service-network.jpg
    static/images/service-redteam.jpg
    static/images/service-ai.jpg

크기: 1600×1200 (4:3)
  · 서비스 목록에서는 4:3 그대로 쓰인다.
  · 서비스 상세 히어로에서는 21:9 로 잘린다 → 세로 y=257~942 구간만 남는다.
  그래서 중요한 요소는 전부 y 280~920 안쪽(SAFE_TOP~SAFE_BOTTOM)에 배치한다.
"""

import math
import os
import random
import subprocess
import sys

W, H = 1600, 1200
SAFE_TOP, SAFE_BOTTOM = 280, 920
CX, CY = W / 2, H / 2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE_DIR, "static", "images")
TMP_DIR = os.path.join(BASE_DIR, "tools", ".render")


# ---------------------------------------------------------------------------
# 팔레트 — 어두운 페이지 위에서 색으로 숨통을 틔우는 역할.
# bg1(밝은 쪽) → bg2(어두운 쪽) 그라디언트에 accent 로 포인트를 준다.
# ---------------------------------------------------------------------------
PALETTE = {
    "api": {          # API 모의해킹 — 시안
        "bg1": "#2C63BC", "bg2": "#0D2049",
        "glow": "#3CBAF2", "accent": "#5AEAF7", "accent2": "#BCF5FB",
    },
    "network": {      # 네트워크 모의해킹 — 바이올렛
        "bg1": "#3E44AE", "bg2": "#121744",
        "glow": "#8271FF", "accent": "#AB9EFF", "accent2": "#E0DAFF",
    },
    "redteam": {      # 레드팀 — 코랄 + 앰버
        "bg1": "#A23256", "bg2": "#20112E",
        "glow": "#F65C7E", "accent": "#FF9AA6", "accent2": "#FFD2A2",
    },
    "ai": {           # AI 취약점 점검 — 민트
        "bg1": "#1C7B90", "bg2": "#092B3E",
        "glow": "#2AD4A8", "accent": "#68F2BC", "accent2": "#C0FAE6",
    },
}

# 배경 어둡게 눌리는 정도. 0 이면 비네트 없음. 더 환하게 하려면 값을 낮춘다.
VIGNETTE = 0.32


# ---------------------------------------------------------------------------
# 공통 조각
# ---------------------------------------------------------------------------

def defs(p, extra=""):
    """배경 그라디언트 · 글로우 · 그레인 · 페이드 마스크."""
    return f"""
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%"   stop-color="{p['bg1']}"/>
    <stop offset="55%"  stop-color="{mix(p['bg1'], p['bg2'], .55)}"/>
    <stop offset="100%" stop-color="{p['bg2']}"/>
  </linearGradient>

  <radialGradient id="glowA">
    <stop offset="0%"   stop-color="{p['glow']}" stop-opacity=".95"/>
    <stop offset="42%"  stop-color="{p['glow']}" stop-opacity=".34"/>
    <stop offset="100%" stop-color="{p['glow']}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowB">
    <stop offset="0%"   stop-color="{p['accent']}" stop-opacity=".62"/>
    <stop offset="100%" stop-color="{p['accent']}" stop-opacity="0"/>
  </radialGradient>

  <radialGradient id="vignette">
    <stop offset="62%"  stop-color="#000" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000" stop-opacity="{VIGNETTE}"/>
  </radialGradient>

  <linearGradient id="fadeX" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%"   stop-color="#fff" stop-opacity="0"/>
    <stop offset="7%"   stop-color="#fff" stop-opacity="1"/>
    <stop offset="93%"  stop-color="#fff" stop-opacity="1"/>
    <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="maskX"><rect width="{W}" height="{H}" fill="url(#fadeX)"/></mask>

  <linearGradient id="fadeY" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%"   stop-color="#fff" stop-opacity="0"/>
    <stop offset="14%"  stop-color="#fff" stop-opacity="1"/>
    <stop offset="86%"  stop-color="#fff" stop-opacity="1"/>
    <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="maskY"><rect width="{W}" height="{H}" fill="url(#fadeY)"/></mask>

  <radialGradient id="fadeR">
    <stop offset="0%"  stop-color="#fff" stop-opacity="1"/>
    <stop offset="62%" stop-color="#fff" stop-opacity=".7"/>
    <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <mask id="maskR"><rect width="{W}" height="{H}" fill="url(#fadeR)"/></mask>

  <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="9"/>
  </filter>
  <filter id="soft2" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="3"/>
  </filter>
  <filter id="grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
  {extra}
</defs>"""


def backdrop(p, gx=0.30, gy=0.30):
    return f"""
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<ellipse cx="{W*gx:.0f}" cy="{H*gy:.0f}" rx="760" ry="620" fill="url(#glowA)"/>
<ellipse cx="{W*0.86:.0f}" cy="{H*0.82:.0f}" rx="520" ry="440" fill="url(#glowB)"/>"""


def grid(step=64, opacity=.10):
    lines = []
    x = 0
    while x <= W:
        lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>')
        x += step
    y = 0
    while y <= H:
        lines.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>')
        y += step
    return (f'<g mask="url(#maskR)" stroke="#fff" stroke-opacity="{opacity}" '
            f'stroke-width="1">{"".join(lines)}</g>')


def overlay():
    return f"""
<rect width="{W}" height="{H}" fill="url(#vignette)"/>
<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".055" style="mix-blend-mode:overlay"/>"""


def mix(c1, c2, t):
    """두 hex 색을 t 비율로 섞는다."""
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(a[i] + (b[i] - a[i]) * t):02x}" for i in range(3))


def dot(x, y, r, color, glow=True):
    g = (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*3.4:.1f}" fill="{color}" '
         f'opacity=".30" filter="url(#soft)"/>') if glow else ""
    return g + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{color}"/>'


# ---------------------------------------------------------------------------
# 1. API 모의해킹 — 엔드포인트 레인과 요청 흐름, 그리고 흐릿한 섀도우 API
# ---------------------------------------------------------------------------
def scene_api(p):
    rnd = random.Random(11)
    s = [defs(p), backdrop(p, .26, .24), grid(64, .085)]

    lanes = [
        (360, "/v2/orders",          True,  1.0),
        (470, "/v2/users/{id}",      True,  0.85),
        (580, "/v1/payments",        True,  1.0),
        (690, "/v1/users/{id}/roles", True, 0.8),
        (800, "/internal/debug",     False, 1.0),   # 섀도우 API
    ]

    body = []
    for y, label, known, op in lanes:
        color = p["accent"] if known else p["accent2"]
        dash = "" if known else ' stroke-dasharray="14 12"'
        alpha = 0.55 * op if known else 0.42
        body.append(
            f'<line x1="150" y1="{y}" x2="1450" y2="{y}" stroke="{color}" '
            f'stroke-opacity="{alpha:.2f}" stroke-width="{2.2 if known else 1.8}"{dash}/>'
        )
        # 엔드포인트 칩
        for x in (330, 640, 950, 1260):
            wch = 58
            body.append(
                f'<rect x="{x - wch/2}" y="{y - 13}" width="{wch}" height="26" rx="13" '
                f'fill="{color}" fill-opacity="{0.13 if known else 0.08}" '
                f'stroke="{color}" stroke-opacity="{0.45 if known else 0.28}" stroke-width="1.2"/>'
            )
        # 흐르는 패킷
        n = 3 if known else 1
        for i in range(n):
            x = 200 + rnd.random() * 1200
            body.append(dot(x, y, 5.2 if known else 4.0, p["accent2"] if known else color))
        # 경로 라벨
        body.append(
            f'<text x="150" y="{y - 22}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
            f'font-size="19" fill="{color}" fill-opacity="{0.62 if known else 0.45}" '
            f'letter-spacing="1.5">{label}</text>'
        )

    # 좌우 기둥 (클라이언트 / 서버)
    for x, lab, anchor in ((126, "CLIENT", "start"), (1474, "SERVICE", "end")):
        body.append(
            f'<line x1="{x}" y1="{SAFE_TOP + 20}" x2="{x}" y2="{SAFE_BOTTOM - 20}" '
            f'stroke="{p["accent"]}" stroke-opacity=".42" stroke-width="2.4"/>'
        )
        body.append(
            f'<text x="{x + (12 if anchor == "start" else -12)}" y="{SAFE_TOP + 6}" '
            f'text-anchor="{anchor}" font-family="ui-monospace, Menlo, monospace" font-size="17" '
            f'fill="{p["accent2"]}" fill-opacity=".55" letter-spacing="3">{lab}</text>'
        )

    # 섀도우 API 강조 링
    body.append(
        f'<rect x="120" y="768" width="1360" height="64" rx="32" fill="none" '
        f'stroke="{p["accent2"]}" stroke-opacity=".34" stroke-width="1.6" stroke-dasharray="4 9"/>'
    )

    s.append(f'<g mask="url(#maskX)">{"".join(body)}</g>')
    s.append(overlay())
    return "".join(s)


# ---------------------------------------------------------------------------
# 2. 네트워크 모의해킹 — 경계에서 중심까지 이어지는 침투 경로
# ---------------------------------------------------------------------------
def scene_network(p):
    rnd = random.Random(23)
    s = [defs(p), backdrop(p, .70, .28), grid(80, .07)]
    body = []

    # 동심원 = 경계 / DMZ / 내부망
    for r, op in ((520, .22), (360, .28), (200, .34)):
        body.append(
            f'<ellipse cx="{CX}" cy="{CY}" rx="{r * 1.55:.0f}" ry="{r:.0f}" fill="none" '
            f'stroke="{p["accent"]}" stroke-opacity="{op}" stroke-width="1.6" stroke-dasharray="3 10"/>'
        )

    # 노드 뿌리기
    nodes = []
    for ring, count in ((520, 16), (360, 11), (200, 7)):
        for i in range(count):
            a = (i / count) * math.tau + rnd.uniform(-.14, .14)
            rr = ring * rnd.uniform(.9, 1.06)
            x = CX + math.cos(a) * rr * 1.55
            y = CY + math.sin(a) * rr
            if SAFE_TOP - 30 < y < SAFE_BOTTOM + 30 and 60 < x < W - 60:
                nodes.append((x, y, ring))

    # 노드 간 옅은 연결선
    for i, (x1, y1, r1) in enumerate(nodes):
        for x2, y2, r2 in nodes[i + 1:]:
            d = math.hypot(x2 - x1, y2 - y1)
            if d < 210:
                body.append(
                    f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
                    f'stroke="{p["accent"]}" stroke-opacity=".16" stroke-width="1"/>'
                )
    for x, y, r in nodes:
        body.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{6.0 if r == 200 else 4.6:.1f}" '
            f'fill="{p["accent"]}" fill-opacity=".78"/>'
        )

    # 침투 경로 — 왼쪽 경계에서 중심까지, x 가 단조 증가해야 되돌아오지 않는다
    path = [(140, 436), (352, 520), (556, 468), (700, 552), (CX, CY)]
    d = "M " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in path)
    body.append(f'<path d="{d}" fill="none" stroke="{p["accent"]}" stroke-opacity=".38" '
                f'stroke-width="13" filter="url(#soft)"/>')
    body.append(f'<path d="{d}" fill="none" stroke="{p["accent"]}" stroke-width="3.0" '
                f'stroke-linecap="round" stroke-linejoin="round"/>')
    for i, (x, y) in enumerate(path[:-1]):
        body.append(dot(x, y, 7.5, p["accent2"], glow=False))
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="14" fill="none" '
                    f'stroke="{p["accent"]}" stroke-opacity=".5" stroke-width="1.6"/>')
        body.append(
            f'<text x="{x}" y="{y - 28}" text-anchor="middle" font-family="ui-monospace, Menlo, monospace" '
            f'font-size="18" fill="{p["accent2"]}" fill-opacity=".62" letter-spacing="2">'
            f'{"0%d" % (i + 1)}</text>'
        )

    # 중심 목표
    body.append(f'<circle cx="{CX}" cy="{CY}" r="86" fill="{p["accent2"]}" opacity=".20" filter="url(#soft)"/>')
    body.append(f'<circle cx="{CX}" cy="{CY}" r="52" fill="none" stroke="{p["accent2"]}" '
                f'stroke-opacity=".40" stroke-width="1.6" stroke-dasharray="5 8"/>')
    body.append(f'<circle cx="{CX}" cy="{CY}" r="30" fill="none" stroke="{p["accent2"]}" stroke-width="2.6"/>')
    body.append(f'<circle cx="{CX}" cy="{CY}" r="11" fill="{p["accent2"]}"/>')
    body.append(
        f'<text x="{CX}" y="{CY + 92}" text-anchor="middle" font-family="ui-monospace, Menlo, monospace" '
        f'font-size="17" fill="{p["accent2"]}" fill-opacity=".6" letter-spacing="3">DOMAIN ADMIN</text>'
    )

    s.append("".join(body))
    s.append(overlay())
    return "".join(s)


# ---------------------------------------------------------------------------
# 3. 레드팀 — 표적 링, 레이더 스윕, 킬체인 단계
# ---------------------------------------------------------------------------
def scene_redteam(p):
    s = [defs(p), backdrop(p, .66, .28), grid(80, .06)]
    body = []
    tx, ty = W * 0.72, CY

    # 레이더 스윕 (부채꼴)
    sweep_defs = (
        f'<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0%" stop-color="{p["accent"]}" stop-opacity=".34"/>'
        f'<stop offset="100%" stop-color="{p["accent"]}" stop-opacity="0"/></linearGradient>'
    )
    s[0] = defs(p, sweep_defs)
    a0, a1 = math.radians(-148), math.radians(-92)
    R = 400
    body.append(
        f'<path d="M {tx:.0f} {ty:.0f} L {tx + math.cos(a0)*R:.0f} {ty + math.sin(a0)*R:.0f} '
        f'A {R} {R} 0 0 1 {tx + math.cos(a1)*R:.0f} {ty + math.sin(a1)*R:.0f} Z" '
        f'fill="url(#sweep)"/>'
    )

    # 표적 링
    for r, op in ((400, .18), (300, .24), (200, .30), (100, .40)):
        body.append(f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="{r}" fill="none" '
                    f'stroke="{p["accent"]}" stroke-opacity="{op}" stroke-width="1.5"/>')
    # 십자선
    body.append(f'<line x1="{tx-450:.0f}" y1="{ty}" x2="{tx+450:.0f}" y2="{ty}" '
                f'stroke="{p["accent"]}" stroke-opacity=".26" stroke-width="1.2"/>')
    body.append(f'<line x1="{tx:.0f}" y1="{ty-420:.0f}" x2="{tx:.0f}" y2="{ty+420:.0f}" '
                f'stroke="{p["accent"]}" stroke-opacity=".26" stroke-width="1.2"/>')
    body.append(f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="78" fill="{p["accent"]}" opacity=".24" filter="url(#soft)"/>')
    body.append(f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="14" fill="{p["accent2"]}"/>')
    body.append(
        f'<text x="{tx:.0f}" y="{ty - 128:.0f}" text-anchor="middle" '
        f'font-family="ui-monospace, Menlo, monospace" font-size="18" fill="{p["accent2"]}" '
        f'fill-opacity=".68" letter-spacing="3.4">OBJECTIVE</text>'
    )

    # 킬체인 — 좌하단에서 표적까지 계단식.
    # 노드 x 좌표가 서로 충분히 떨어져 있어야 라벨이 겹치지 않는다.
    nodes = [(150, 878), (342, 802), (534, 730), (704, 670), (862, 626)]
    labels = ["RECON", "ACCESS", "FOOTHOLD", "ESCALATE", "PIVOT"]

    steps = [nodes[0]]
    for (x0, y0), (x1, y1) in zip(nodes, nodes[1:]):
        steps += [(x1, y0), (x1, y1)]
    steps += [(tx - 100, nodes[-1][1]), (tx - 100, ty)]

    d = "M " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in steps)
    body.append(f'<path d="{d}" fill="none" stroke="{p["accent2"]}" stroke-opacity=".28" '
                f'stroke-width="12" filter="url(#soft)"/>')
    body.append(f'<path d="{d}" fill="none" stroke="{p["accent2"]}" stroke-width="2.6" '
                f'stroke-linejoin="round" stroke-linecap="round"/>')

    for (x, y), lab in zip(nodes, labels):
        body.append(f'<rect x="{x-10}" y="{y-10}" width="20" height="20" rx="5" '
                    f'fill="{p["bg2"]}" stroke="{p["accent2"]}" stroke-width="2.4"/>')
        body.append(
            f'<text x="{x}" y="{y - 26}" text-anchor="middle" font-family="ui-monospace, Menlo, monospace" '
            f'font-size="16" fill="{p["accent2"]}" fill-opacity=".66" letter-spacing="2.4">{lab}</text>'
        )

    s.append("".join(body))
    s.append(overlay())
    return "".join(s)


# ---------------------------------------------------------------------------
# 4. AI 취약점 점검 — 전수 스캔 격자, 스캔 밴드, 검증 대상 셀
# ---------------------------------------------------------------------------
def scene_ai(p):
    rnd = random.Random(7)
    scan_defs = (
        f'<linearGradient id="scan" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0%" stop-color="{p["accent"]}" stop-opacity="0"/>'
        f'<stop offset="55%" stop-color="{p["accent"]}" stop-opacity=".30"/>'
        f'<stop offset="88%" stop-color="{p["accent2"]}" stop-opacity=".55"/>'
        f'<stop offset="100%" stop-color="{p["accent2"]}" stop-opacity="0"/></linearGradient>'
    )
    s = [defs(p, scan_defs), backdrop(p, .28, .70), ""]
    body = []

    cell, gap = 26, 8
    cols, rows = 42, 20
    gw = cols * (cell + gap) - gap
    gh = rows * (cell + gap) - gap
    ox, oy = (W - gw) / 2, (H - gh) / 2
    scan_x = ox + gw * 0.63

    flagged = set()
    while len(flagged) < 9:
        flagged.add((rnd.randrange(6, cols - 4), rnd.randrange(3, rows - 3)))

    for r in range(rows):
        for c in range(cols):
            x, y = ox + c * (cell + gap), oy + r * (cell + gap)
            cxp = x + cell / 2
            near = max(0.0, 1 - abs(cxp - scan_x) / 320)     # 스캔 밴드 근처는 밝게
            base = 0.055 + rnd.random() * 0.075 + near * 0.16
            body.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{cell}" height="{cell}" rx="5" '
                        f'fill="{p["accent"]}" fill-opacity="{base:.3f}"/>')

    # 스캔 밴드 — 위아래로도 페이드해서 패널처럼 보이지 않게 한다
    band = [
        f'<rect x="{scan_x - 300:.0f}" y="0" width="320" height="{H}" fill="url(#scan)"/>',
        f'<line x1="{scan_x:.0f}" y1="0" x2="{scan_x:.0f}" y2="{H}" '
        f'stroke="{p["accent2"]}" stroke-opacity=".9" stroke-width="2.6"/>',
        f'<line x1="{scan_x:.0f}" y1="0" x2="{scan_x:.0f}" y2="{H}" '
        f'stroke="{p["accent2"]}" stroke-opacity=".5" stroke-width="13" filter="url(#soft)"/>',
    ]
    body.append(f'<g mask="url(#maskY)">{"".join(band)}</g>')

    # 검증 대상 셀 + 수렴선
    hub = (W * 0.5, SAFE_BOTTOM + 22)
    for c, r in sorted(flagged):
        x, y = ox + c * (cell + gap), oy + r * (cell + gap)
        body.append(f'<rect x="{x-4:.0f}" y="{y-4:.0f}" width="{cell+8}" height="{cell+8}" rx="8" '
                    f'fill="{p["accent2"]}" fill-opacity=".22" stroke="{p["accent2"]}" stroke-width="2"/>')
        body.append(f'<rect x="{x-4:.0f}" y="{y-4:.0f}" width="{cell+8}" height="{cell+8}" rx="8" '
                    f'fill="{p["accent2"]}" fill-opacity=".18" filter="url(#soft2)"/>')
        body.append(f'<path d="M {x + cell/2:.0f} {y + cell/2:.0f} Q {hub[0]:.0f} {(y+hub[1])/2:.0f} '
                    f'{hub[0]:.0f} {hub[1]:.0f}" fill="none" stroke="{p["accent2"]}" '
                    f'stroke-opacity=".22" stroke-width="1.3"/>')
    body.append(dot(hub[0], hub[1], 9, p["accent2"]))
    body.append(
        f'<text x="{hub[0]:.0f}" y="{hub[1] + 40:.0f}" text-anchor="middle" '
        f'font-family="ui-monospace, Menlo, monospace" font-size="17" fill="{p["accent2"]}" '
        f'fill-opacity=".6" letter-spacing="3">EXPERT VALIDATION</text>'
    )

    s[2] = f'<g mask="url(#maskX)">{"".join(body)}</g>'
    s.append(overlay())
    return "".join(s)


# ---------------------------------------------------------------------------
SCENES = {
    "service-api":     ("api",     scene_api),
    "service-network": ("network", scene_network),
    "service-redteam": ("redteam", scene_redteam),
    "service-ai":      ("ai",      scene_ai),
}


def build():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(TMP_DIR, exist_ok=True)
    made = []
    for name, (key, fn) in SCENES.items():
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
               f'viewBox="0 0 {W} {H}">{fn(PALETTE[key])}</svg>')
        path = os.path.join(TMP_DIR, name + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f'<!doctype html><meta charset="utf-8">'
                    f'<style>html,body{{margin:0;padding:0;background:#000}}</style>{svg}')
        made.append((name, path))
    return made


def rasterize(made):
    from playwright.sync_api import sync_playwright
    exe = os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium")
    with sync_playwright() as pw:
        launch = {"executable_path": exe} if os.path.exists(exe) else {}
        b = pw.chromium.launch(**launch)
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for name, path in made:
            pg.goto("file://" + path)
            pg.wait_for_timeout(320)
            out = os.path.join(OUT_DIR, name + ".jpg")
            pg.screenshot(path=out, type="jpeg", quality=88)
            print(f"  {name}.jpg  {os.path.getsize(out)//1024} KB")
        b.close()


if __name__ == "__main__":
    print("서비스 이미지 생성 중...")
    rasterize(build())
    print(f"완료 → {OUT_DIR}")
