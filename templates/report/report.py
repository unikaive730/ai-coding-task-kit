"""한 장짜리 HTML 보고서 틀 (표준 라이브러리만). 숫자 타일 · 표 · 막대 · 선 그래프를 SVG 로 그린다.

    from report import Report
    r = Report("제목", "기준 시각 · 데이터 범위")
    r.text("요약 한 줄")
    r.stats([("고장 사전 알림", "4/5건", "목표 4건 이상")])       # 이름 먼저, 단위 붙여
    r.table(rows)                                                  # dict 목록 (또는 list 목록 + cols=)
    r.bar("설비별 알림 수", {"A-01": 3, "B-02": 1}, unit="건")
    r.line("A-01 온도", {"temp": [("2026-09-27T01:00", 61.2), ...]}, unit="°C",
           hlines={"상한": 68}, marks={"고장": "2026-09-27T03:00"})
    r.save("report.html")

- x 는 숫자 또는 ISO 날짜·시각 글자. 시간대는 미리 하나로 맞춰 넣는다(표시는 넣은 시각 그대로). y 가 None 이면 선을 끊는다
- 선은 4개까지 (그 이상은 그래프를 나눈다). 점마다 마우스를 올리면 값이 뜬다
- 보기: 그 폴더에서 python3 -m http.server 8000 --bind 0.0.0.0 → 미리보기 PORT 8000, URL /report.html
- 시험: python3 report.py --demo /tmp/report_demo.html (예시 값이라 결과물에 쓰지 않는다)
"""
import html
import math
import sys
from datetime import datetime, timezone

COLORS = ["var(--s1)", "var(--s2)", "var(--s3)", "var(--s4)"]
CSS = """
:root{color-scheme:light;--bg:#fcfcfb;--card:#ffffff;--ink:#0b0b0b;--ink2:#52514e;--muted:#8a8984;--grid:#e6e5e1;
--s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--s4:#eda100;--ref:#52514e}
@media (prefers-color-scheme:dark){:root{color-scheme:dark;--bg:#1a1a19;--card:#232322;--ink:#f0efec;--ink2:#c3c2b7;
--muted:#8f8e86;--grid:#3a3936;--s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--ref:#c3c2b7}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}
main{max-width:1080px;margin:0 auto;padding:24px 16px 48px}h1{font-size:24px;margin:0 0 4px}h2{font-size:17px;margin:0 0 8px}
.sub{color:var(--ink2);margin:0 0 20px}section{background:var(--card);border:1px solid var(--grid);border-radius:8px;padding:16px;margin:0 0 16px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}.tile .k{color:var(--ink2);font-size:13px}
.tile .v{font-size:26px;font-weight:650}.tile .n{color:var(--muted);font-size:12px}
table{border-collapse:collapse;width:100%;font-size:13px}th,td{border-bottom:1px solid var(--grid);padding:5px 8px;text-align:left;vertical-align:top}
th{color:var(--ink2);font-weight:600}td.num{text-align:right;font-variant-numeric:tabular-nums}.wrap{overflow-x:auto}
svg{width:100%;height:auto;display:block}svg text{fill:var(--ink2);font-size:12px}svg .grid{stroke:var(--grid)}
svg .hit{fill:transparent}svg .hit:hover{fill:currentColor;opacity:.25}details{margin-top:8px;color:var(--ink2)}
.legend{display:flex;gap:16px;flex-wrap:wrap;color:var(--ink2);font-size:13px;margin:0 0 6px}.legend i{display:inline-block;width:14px;height:3px;border-radius:2px;vertical-align:middle;margin-right:6px}
"""


def _esc(v):
    return html.escape("" if v is None else str(v))


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _fmt(v, unit=""):
    if not _num(v):
        return _esc(v)
    s = f"{v:,.0f}" if abs(v) >= 1000 or float(v).is_integer() else f"{v:,.3g}" if abs(v) < 1 else f"{v:,.2f}".rstrip("0").rstrip(".")
    return s + unit


def _x(v):
    """숫자는 그대로, 날짜·시각 글자는 UTC 초로."""
    if _num(v):
        return float(v), False
    d = datetime.fromisoformat(str(v).strip().replace("Z", "+00:00").replace(" ", "T"))
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.timestamp(), True


def _ticks(lo, hi, n=5):
    if hi <= lo:
        hi = lo + 1
    raw = (hi - lo) / n
    step = 10 ** math.floor(math.log10(raw))
    step *= next(m for m in (1, 2, 2.5, 5, 10) if raw <= step * m)
    t = math.floor(lo / step) * step
    out = [round(t, 10)]
    while out[-1] < hi - step * 1e-9:
        t += step
        out.append(round(t, 10))
    return out


def _time_ticks(x0, x1):
    span = (x1 - x0) or 1
    for step in (3600, 3 * 3600, 6 * 3600, 12 * 3600, 86400, 2 * 86400, 7 * 86400, 30 * 86400, 365 * 86400):
        if span / step <= 7:
            break
    t = math.ceil(x0 / step) * step
    out = []
    while t <= x1:
        out.append(t)
        t += step
    f = "%m-%d" if step >= 86400 else ("%m-%d %H:%M" if span > 86400 else "%H:%M")
    return [(v, datetime.fromtimestamp(v, timezone.utc).strftime(f)) for v in out]


class Report:
    def __init__(self, title, subtitle=""):
        self.title, self.subtitle, self.parts = title, subtitle, []

    def text(self, s, title=None):
        h = f"<h2>{_esc(title)}</h2>" if title else ""
        self.parts.append(f"<section>{h}<p>{_esc(s)}</p></section>")

    def stats(self, items):
        """items: (이름, 값, 설명) 목록. 이름에 무엇의 수인지, 값에 단위."""
        tiles = "".join(f'<div class="tile"><div class="k">{_esc(i[0])}</div><div class="v">{_esc(i[1])}</div>'
                        f'<div class="n">{_esc(i[2]) if len(i) > 2 else ""}</div></div>' for i in items)
        self.parts.append(f'<section><div class="tiles">{tiles}</div></section>')

    def table(self, rows, cols=None, title=None, max_rows=300):
        rows = list(rows)
        if rows and isinstance(rows[0], dict):
            cols = cols or list(rows[0].keys())
            rows = [[r.get(c) for c in cols] for r in rows]
        head = "".join(f"<th>{_esc(c)}</th>" for c in cols or [])
        body = "".join("<tr>" + "".join(f'<td class="num">{_fmt(v)}</td>' if _num(v) else f"<td>{_esc(v)}</td>" for v in r) + "</tr>"
                       for r in rows[:max_rows])
        more = f'<p class="sub">앞 {max_rows}행만 표시 · 전체 {len(rows)}행</p>' if len(rows) > max_rows else ""
        h = f"<h2>{_esc(title)}</h2>" if title else ""
        self.parts.append(f'<section>{h}<div class="wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>{more}</section>')

    def bar(self, title, data, unit="", color=1):
        """가로 막대. data: {이름: 값} (넣은 순서대로 그린다)."""
        items = list(data.items())
        W, lab, pad, bh, gap = 1000, 170, 70, 22, 10
        vals = [v for _, v in items if _num(v)] or [0]
        lo, hi = min(0, min(vals)), max(0, max(vals))
        span = (hi - lo) or 1
        sx = lambda v: lab + (v - lo) / span * (W - lab - pad)
        H = len(items) * (bh + gap) + 10
        out = [f'<line class="grid" x1="{sx(0):.1f}" x2="{sx(0):.1f}" y1="0" y2="{H - 6}"/>']
        for i, (k, v) in enumerate(items):
            y = 5 + i * (bh + gap)
            out.append(f'<text x="{lab - 8}" y="{y + bh / 2 + 4:.1f}" text-anchor="end">{_esc(str(k)[:22])}</text>')
            if not _num(v):
                continue
            a, b = sorted((sx(0), sx(v)))
            r = min(4, (b - a) / 2, bh / 2)
            if v >= 0:
                d = f"M{a:.1f},{y} H{b - r:.1f} Q{b:.1f},{y} {b:.1f},{y + r} V{y + bh - r} Q{b:.1f},{y + bh} {b - r:.1f},{y + bh} H{a:.1f} Z"
            else:
                d = f"M{b:.1f},{y} H{a + r:.1f} Q{a:.1f},{y} {a:.1f},{y + r} V{y + bh - r} Q{a:.1f},{y + bh} {a + r:.1f},{y + bh} H{b:.1f} Z"
            out.append(f'<path d="{d}" fill="{COLORS[(color - 1) % 4]}"><title>{_esc(k)}: {_fmt(v, unit)}</title></path>')
            tx = (b + 6) if v >= 0 else (a - 6)
            out.append(f'<text x="{tx:.1f}" y="{y + bh / 2 + 4:.1f}" text-anchor="{"start" if v >= 0 else "end"}" style="fill:var(--ink)">{_fmt(v, unit)}</text>')
        svg = f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{_esc(title)}">{"".join(out)}</svg>'
        rows = "".join(f'<tr><td>{_esc(k)}</td><td class="num">{_fmt(v, unit)}</td></tr>' for k, v in items)
        self.parts.append(f"<section><h2>{_esc(title)}</h2>{svg}<details><summary>표로 보기</summary><table>{rows}</table></details></section>")

    def line(self, title, series, unit="", hlines=None, marks=None, height=320):
        """series: {이름: [(x, y), ...]} 최대 4개. hlines: {이름: y} 기준선. marks: {이름: x} 사건 표시(세로선)."""
        names = list(series)[:4]
        if len(series) > 4:
            print(f"report.line: 선은 4개까지 · 빠진 것 {list(series)[4:]}", file=sys.stderr)
        pts, is_time = {}, False
        for n in names:
            pts[n] = []
            for x, y in series[n]:
                xv, t = _x(x)
                is_time |= t
                pts[n].append((xv, y if _num(y) else None, x))
        xs = [p[0] for n in names for p in pts[n]]
        ys = [p[1] for n in names for p in pts[n] if p[1] is not None] + list((hlines or {}).values())
        mk = [(k, _x(v)[0]) for k, v in (marks or {}).items()]
        xs += [v for _, v in mk]
        if not xs or not ys:
            return self.text("그릴 값 없음", title)
        x0, x1 = min(xs), max(xs)
        ylo, yhi = min(ys), max(ys)
        padv = (yhi - ylo) * 0.08 or 1
        yt = _ticks(ylo - padv, yhi + padv)
        ylo, yhi = yt[0], yt[-1]
        W, L, R, T, B = 1000, 64, 90, 12, 34
        H = height
        sx = lambda v: L + (v - x0) / ((x1 - x0) or 1) * (W - L - R)
        sy = lambda v: T + (yhi - v) / ((yhi - ylo) or 1) * (H - T - B)
        out = []
        for t in yt:
            out.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{sy(t):.1f}" y2="{sy(t):.1f}"/>'
                       f'<text x="{L - 8}" y="{sy(t) + 4:.1f}" text-anchor="end">{_fmt(t)}</text>')
        xt = _time_ticks(x0, x1) if is_time else [(v, _fmt(v)) for v in _ticks(x0, x1) if x0 <= v <= x1]
        for v, lab in xt:
            out.append(f'<text x="{sx(v):.1f}" y="{H - 12}" text-anchor="middle">{_esc(lab)}</text>')
        for k, v in (hlines or {}).items():
            out.append(f'<line x1="{L}" x2="{W - R}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" stroke="var(--ref)" stroke-width="1.5" stroke-dasharray="6 4"/>'
                       f'<text x="{W - R + 6}" y="{sy(v) + 4:.1f}">{_esc(k)} {_fmt(v, unit)}</text>')
        for k, v in mk:
            out.append(f'<line x1="{sx(v):.1f}" x2="{sx(v):.1f}" y1="{T}" y2="{H - B}" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="2 3"/>'
                       f'<text x="{sx(v) + 4:.1f}" y="{T + 12}" style="fill:var(--ink)">{_esc(k)}</text>')
        for i, n in enumerate(names):
            c = COLORS[i]
            seq = sorted(pts[n], key=lambda p: p[0])
            d, pen = [], False
            for xv, yv, _ in seq:
                if yv is None:
                    pen = False
                    continue
                d.append(f'{"L" if pen else "M"}{sx(xv):.1f},{sy(yv):.1f}')
                pen = True
            out.append(f'<path d="{" ".join(d)}" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>')
            step = max(1, len(seq) // 1500)
            for xv, yv, raw in seq[::step]:
                if yv is not None:
                    out.append(f'<circle class="hit" cx="{sx(xv):.1f}" cy="{sy(yv):.1f}" r="6" style="color:{c}">'
                               f'<title>{_esc(n)} · {_esc(raw)} · {_fmt(yv, unit)}</title></circle>')
            last = next((p for p in reversed(seq) if p[1] is not None), None)
            if last and len(names) > 1:
                out.append(f'<text x="{sx(last[0]) + 6:.1f}" y="{sy(last[1]) + 4:.1f}" style="fill:var(--ink)">{_esc(n)}</text>')
        legend = ""
        if len(names) > 1:
            legend = '<div class="legend">' + "".join(f'<span><i style="background:{COLORS[i]}"></i>{_esc(n)}</span>' for i, n in enumerate(names)) + "</div>"
        svg = f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{_esc(title)}">{"".join(out)}</svg>'
        summ = ""
        for n in names:
            v = [p[1] for p in pts[n] if p[1] is not None]
            if v:
                summ += f'<tr><td>{_esc(n)}</td><td class="num">{len(v)}</td><td class="num">{_fmt(min(v), unit)}</td><td class="num">{_fmt(sum(v) / len(v), unit)}</td><td class="num">{_fmt(max(v), unit)}</td></tr>'
        table = f"<details><summary>표로 보기</summary><table><tr><th>선</th><th>점 수</th><th>최소</th><th>평균</th><th>최대</th></tr>{summ}</table></details>"
        u = f" ({_esc(unit)})" if unit else ""
        self.parts.append(f"<section><h2>{_esc(title)}{u}</h2>{legend}{svg}{table}</section>")

    def html(self):
        return (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
                f"<title>{_esc(self.title)}</title><style>{CSS}</style></head><body><main><h1>{_esc(self.title)}</h1>"
                f'<p class="sub">{_esc(self.subtitle)}</p>{"".join(self.parts)}</main></body></html>')

    def save(self, path="report.html"):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.html())
        print(f"saved {path}")
        return path


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "--demo":
        print(__doc__)
        sys.exit(1)
    r = Report("보고서 틀 시험 (예시 값)", "예시 값 · 결과물에 쓰지 않는다")
    r.stats([("예시 지표 A", "4/5건", "목표 4건 이상"), ("예시 지표 B", "1.5건/주", "목표 2건 이하")])
    r.bar("예시 막대", {"A-01": 3, "A-02": 1, "B-01": 0, "B-02": 5}, unit="건")
    r.line("예시 선", {"a": [(f"2026-09-0{d}T{h:02d}:00Z", 60 + d + (h % 6) * 0.4 if (d, h) != (3, 6) else None)
                            for d in range(1, 6) for h in range(0, 24, 3)],
                      "b": [(f"2026-09-0{d}T{h:02d}:00Z", 58 + d * 0.5) for d in range(1, 6) for h in range(0, 24, 6)]},
           unit="°C", hlines={"상한": 68}, marks={"사건": "2026-09-04T06:00Z"})
    r.table([{"이름": "A-01", "값": 3.25, "메모": "<예시>"}, {"이름": "B-02", "값": 1200, "메모": ""}], title="예시 표")
    r.save(sys.argv[2])
