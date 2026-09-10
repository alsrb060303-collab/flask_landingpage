"""
UNIV (유니브) — 모의해킹 · 레드팀 · AI 보안 전문기업 웹사이트

실행:
    pip install -r requirements.txt
    python app.py            # http://127.0.0.1:5000

구조:
    /            한국어  ·  /en          English
    /services    서비스 목록
    /services/<slug>
    /about /insights /careers /contact /security
"""

from __future__ import annotations

import os
from datetime import datetime

from flask import (
    Blueprint,
    Flask,
    Response,
    abort,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from markupsafe import Markup

from content import (
    CERTIFICATIONS,
    CLIENT_LOGOS,
    COMPANY,
    CONTENT,
    INSIGHTS,
    OPENINGS,
    SERVICES,
    SERVICE_ORDER,
    TEAM,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "static", "images")

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

site = Blueprint("site", __name__)


# ---------------------------------------------------------------------------
# 언어 처리
# ---------------------------------------------------------------------------

LANGS = ("ko", "en")


@site.url_value_preprocessor
def _pull_lang(endpoint, values):
    """URL 규칙의 defaults 로 들어온 lang 을 g 에 옮기고 뷰 인자에서는 제거한다."""
    g.lang = (values or {}).pop("lang", "ko")


@app.context_processor
def _inject_globals():
    lang = getattr(g, "lang", "ko")
    other = "en" if lang == "ko" else "ko"

    def u(name, **kwargs):
        """현재 언어 기준 내부 링크. u('services') -> /services 또는 /en/services"""
        return url_for(f"{lang}.{name}", **kwargs)

    def switch_url():
        """같은 페이지의 반대 언어 URL."""
        endpoint = (request.endpoint or "ko.index").split(".")[-1]
        view_args = dict(request.view_args or {})
        view_args.pop("lang", None)
        try:
            return url_for(f"{other}.{endpoint}", **view_args)
        except Exception:
            return url_for(f"{other}.index")

    def image(filename, alt="", ratio="16 / 9", note=None, classes=""):
        """
        static/images/<filename> 이 있으면 <img>, 없으면 채워 넣을 자리를 보여준다.
        파일만 넣으면 자동으로 사진이 반영된다.
        """
        exists = os.path.isfile(os.path.join(IMAGE_DIR, filename))
        return Markup(render_template(
            "_image_slot.html",
            filename=filename,
            alt=alt,
            ratio=ratio,
            note=note,
            classes=classes,
            exists=exists,
            src=url_for("static", filename=f"images/{filename}") if exists else None,
        ))

    return {
        "lang": lang,
        "other_lang": other,
        "t": CONTENT[lang],
        "company": COMPANY,
        "services": [SERVICES[s] for s in SERVICE_ORDER],
        "team": TEAM,
        "certifications": CERTIFICATIONS,
        "insights_list": INSIGHTS,
        "openings": OPENINGS,
        "client_logos": CLIENT_LOGOS,
        "u": u,
        "switch_url": switch_url,
        "image": image,
        "now": datetime.now(),
        "current_endpoint": (request.endpoint or "").split(".")[-1],
    }


# ---------------------------------------------------------------------------
# 페이지
# ---------------------------------------------------------------------------


@site.route("/")
def index():
    return render_template("index.html")


@site.route("/services")
def services():
    return render_template("services.html")


@site.route("/services/<slug>")
def service_detail(slug):
    if slug not in SERVICES:
        abort(404)
    return render_template("service_detail.html", service=SERVICES[slug], slug=slug)


@site.route("/about")
def about():
    return render_template("about.html")


# 인사이트 목록 페이징 — 처음 몇 편을 서버가 그리고, 이후 몇 편씩 이어 붙일지
INSIGHTS_INITIAL = 2
INSIGHTS_STEP = 1


def _clamp_int(raw, default, lo, hi):
    try:
        v = int(raw)
    except (TypeError, ValueError):
        v = default
    return max(lo, min(v, hi))


@site.route("/insights")
def insights():
    total = len(INSIGHTS)
    # JS 가 없을 때도 ?show=N 으로 더 볼 수 있게 한다.
    show = _clamp_int(request.args.get("show"), INSIGHTS_INITIAL, 1, max(total, 1))
    return render_template(
        "insights.html",
        shown=INSIGHTS[:show],
        step=INSIGHTS_STEP,
    )


@site.route("/api/insights")
def api_insights():
    """
    동적 로딩용. 카드 HTML 을 그대로 돌려주므로 마크업이 템플릿 한 곳에만 존재한다.
    GET /api/insights?offset=2&limit=1  ·  영문은 /en/api/insights
    """
    total = len(INSIGHTS)
    offset = _clamp_int(request.args.get("offset"), 0, 0, total)
    limit = _clamp_int(request.args.get("limit"), INSIGHTS_STEP, 1, 12)

    items = INSIGHTS[offset:offset + limit]
    html = "".join(
        render_template("_post_card.html", post=post, delay=0) for post in items
    )
    next_offset = offset + len(items)

    return jsonify({
        "html": html,
        "count": len(items),
        "offset": offset,
        "next_offset": next_offset,
        "remaining": total - next_offset,
        "total": total,
    })


@site.route("/insights/<slug>")
def insight_detail(slug):
    idx = next((i for i, p in enumerate(INSIGHTS) if p["slug"] == slug), None)
    if idx is None:
        abort(404)
    nxt = INSIGHTS[(idx + 1) % len(INSIGHTS)] if len(INSIGHTS) > 1 else None
    return render_template("insight_detail.html", post=INSIGHTS[idx], nxt=nxt)


@site.route("/careers")
def careers():
    return render_template("careers.html")


@site.route("/contact")
def contact():
    return render_template("contact.html")


@site.route("/security")
def security():
    return render_template("security.html")


# 두 언어로 동일한 블루프린트를 등록한다.
app.register_blueprint(site, name="ko", url_defaults={"lang": "ko"})
app.register_blueprint(site, name="en", url_prefix="/en", url_defaults={"lang": "en"})


# ---------------------------------------------------------------------------
# 부가 라우트
# ---------------------------------------------------------------------------


@app.route("/.well-known/security.txt")
@app.route("/security.txt")
def security_txt():
    """RFC 9116 — 취약점 제보 창구 공시. 보안 기업이라면 반드시 있어야 한다."""
    expires = datetime(datetime.now().year + 1, 1, 1).strftime("%Y-%m-%dT00:00:00.000Z")
    body = (
        f"Contact: mailto:{COMPANY['email']}\n"
        f"Expires: {expires}\n"
        "Preferred-Languages: ko, en\n"
        f"Canonical: {COMPANY['site_url']}/.well-known/security.txt\n"
        f"Policy: {COMPANY['site_url']}/security\n"
    )
    return Response(body, mimetype="text/plain; charset=utf-8")


@app.route("/robots.txt")
def robots_txt():
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {COMPANY['site_url']}/sitemap.xml\n"
    )
    return Response(body, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    names = ["index", "services", "about", "insights", "careers", "contact", "security"]
    urls = []
    for lang in LANGS:
        for name in names:
            urls.append(url_for(f"{lang}.{name}"))
        for slug in SERVICE_ORDER:
            urls.append(url_for(f"{lang}.service_detail", slug=slug))
        for post in INSIGHTS:
            urls.append(url_for(f"{lang}.insight_detail", slug=post["slug"]))

    today = datetime.now().strftime("%Y-%m-%d")
    body = ['<?xml version="1.0" encoding="UTF-8"?>']
    body.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for path in urls:
        body.append(
            f"  <url><loc>{COMPANY['site_url']}{path}</loc>"
            f"<lastmod>{today}</lastmod></url>"
        )
    body.append("</urlset>")
    return Response("\n".join(body), mimetype="application/xml")


@app.errorhandler(404)
def not_found(e):
    g.lang = "en" if request.path.startswith("/en") else "ko"
    return render_template("404.html"), 404


@app.route("/index.html")
def _legacy_index():
    return redirect(url_for("ko.index"), code=301)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
