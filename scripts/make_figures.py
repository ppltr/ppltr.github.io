#!/usr/bin/env python3
"""Şekil gerektiren sorular için SVG çizimler üretir.

Çizimler bilerek sadedir: beyaz zemin, siyah çizgi, temel şekiller (doğru, daire,
elips, üçgen, yay). Renk yalnızca ayırt etmesi zorunlu yerlerde (zemin dolgusu,
vektör vurgusu) ve tek bir gri tonda kullanılır.

Çıktı:
    figures/<ad>.svg      benzersiz çizimler
    figures/index.json    {soru_id: çizim_adı}  — birden çok soru aynı şekli paylaşabilir

Şekil eklerken kaynak soruyu ve doğru şıkkı NOT olarak yaz; geriye doğru teyit
`scripts/check_figures.py` ile yapılır.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "figures"

INK = "#111111"
GREY = "#d8d8d8"
MID = "#8a8a8a"
FONT = 'font-family="ui-sans-serif, system-ui, Segoe UI, sans-serif"'

# ── küçük yardımcılar ────────────────────────────────────────────────


def svg(w: int, h: int, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="100%" role="img">'
        f'<rect width="{w}" height="{h}" fill="#ffffff"/>'
        f'<g fill="none" stroke="{INK}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>'
    )


def line(x1, y1, x2, y2, w=2, dash=None, color=INK):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{w}"{d}/>')


def txt(x, y, s, size=13, anchor="middle", weight="400", color=INK, style=""):
    st = f' font-style="{style}"' if style else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" {FONT} font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" fill="{color}" '
            f'stroke="none"{st}>{s}</text>')


def circle(cx, cy, r, w=2, fill="none", color=INK):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" '
            f'stroke="{color}" stroke-width="{w}"/>')


def ellipse(cx, cy, rx, ry, w=2, fill="none"):
    return (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
            f'fill="{fill}" stroke="{INK}" stroke-width="{w}"/>')


def path(d, w=2, fill="none", color=INK, dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="{fill}" stroke="{color}" '
            f'stroke-width="{w}"{ds}/>')


def poly(pts, w=2, fill="none", color=INK):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{p}" fill="{fill}" stroke="{color}" stroke-width="{w}"/>'


def arrow(x1, y1, x2, y2, w=2, head=9, color=INK, dash=None):
    """Ucu dolu üçgen olan ok."""
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
    left = (bx + head * 0.42 * math.cos(ang + math.pi / 2),
            by + head * 0.42 * math.sin(ang + math.pi / 2))
    right = (bx + head * 0.42 * math.cos(ang - math.pi / 2),
             by + head * 0.42 * math.sin(ang - math.pi / 2))
    return (line(x1, y1, bx, by, w, dash, color) +
            poly([(x2, y2), left, right], w=1, fill=color, color=color))


def dim(x1, y, x2, label, tick=7, size=13):
    """İki ok başlı ölçü çizgisi ve altında etiket."""
    return (arrow((x1 + x2) / 2, y, x1, y, w=1.4, head=7) +
            arrow((x1 + x2) / 2, y, x2, y, w=1.4, head=7) +
            line(x1, y - tick, x1, y + tick, 1.4) +
            line(x2, y - tick, x2, y + tick, 1.4) +
            txt((x1 + x2) / 2, y - 8, label, size=size, weight="600"))


FIGS: dict[str, str] = {}
MAP: dict[str, str] = {}


def add(name: str, ids: list[int], markup: str):
    FIGS[name] = markup
    for i in ids:
        MAP[str(i)] = name


# ── 020 · Gövde yapısı ───────────────────────────────────────────────
# 14447 Monocoque · 14448 Semi-monocoque · 14449 Truss
# Ayırt edici: monokokta yalnız kabuk + çerçeve; yarı monokokta boyuna
# stringerlar da var; kafes tipte üçgenlenmiş çubuk iskelet var.

_BODY = "M60,70 L300,70 L380,102 L380,118 L300,150 L60,150 Z"
_FRAMES = [100, 150, 200, 250, 300]


def fuselage(extra: str) -> str:
    return svg(430, 220,
               path(_BODY, 2.4) +
               "".join(ellipse(x, 110, 8, 40, 1.6) for x in _FRAMES) +
               extra)


add("govde-monocoque", [14447], fuselage(""))

add("govde-semi-monocoque", [14448], fuselage(
    "".join(line(60, y, 300, y, 1.4) for y in (80, 95, 125, 140)) +
    line(300, 80, 380, 104, 1.4) + line(300, 95, 380, 108, 1.4) +
    line(300, 125, 380, 116, 1.4) + line(300, 140, 380, 112, 1.4)))

add("govde-truss", [14449], svg(430, 220,
    path(_BODY, 2.4) +
    "".join(line(x, 70, x, 150, 1.8) for x in _FRAMES) +
    line(60, 150, 100, 70, 1.8) + line(100, 70, 150, 150, 1.8) +
    line(150, 150, 200, 70, 1.8) + line(200, 70, 250, 150, 1.8) +
    line(250, 150, 300, 70, 1.8) + line(300, 70, 380, 118, 1.8)))


# ── 020 · 14459 Kanat parçaları (A/B/C/D) ────────────────────────────
# Doğru: A-Front Spar  B-Ribs  C-Rear Spar  D-Stringer
def _le(x): return 72 + (x - 50) * (104 - 72) / 350
def _te(x): return 212 + (x - 50) * (170 - 212) / 350
def _at(x, frac): return _le(x) + (_te(x) - _le(x)) * frac


_ribs = [110, 165, 220, 275, 330]


def _leader(lx, ly, tx, ty, lab, anchor="middle", dx=0, dy=0):
    """Etiket + ince kılavuz çizgi + hedefin üstünde nokta."""
    return (line(lx, ly, tx, ty, 1.2) + circle(tx, ty, 3.6, 1.4, fill=INK) +
            txt(lx + dx, ly + dy, lab, 15, anchor, "700"))


add("kanat-parcalari", [14459], svg(470, 285,
    path("M50,72 L400,104 L400,170 L50,212 Z", 2.4) +
    # kaburgalar (ince, kirişe dik)
    "".join(line(x, _le(x), x, _te(x), 1.4) for x in _ribs) +
    # stringerlar (en ince, boyuna)
    line(56, _at(56, .40), 396, _at(396, .40), 1.0) +
    line(56, _at(56, .55), 396, _at(396, .55), 1.0) +
    # ön ve arka lonjeron (en kalın)
    line(56, _at(56, .25), 396, _at(396, .25), 3.6) +
    line(56, _at(56, .70), 396, _at(396, .70), 3.6) +
    # etiketler
    _leader(300, 34, 300, _at(300, .25), "A", dy=-8) +
    _leader(150, 262, 165, _at(165, .86), "B", dy=14) +
    _leader(352, 262, 340, _at(340, .70), "C", dy=14) +
    _leader(150, 34, 205, _at(205, .40), "D", dy=-8)))


# ── 020 · 14462 / 14463 Kanat bağlantısı ─────────────────────────────
# Önden görünüş. Konsol (cantilever): dıştan destek yok.
# Payandalı (braced): gövde altından kanada çapraz payanda.
def _plane(struts: bool) -> str:
    body = (
        ellipse(215, 118, 26, 34, 2.4) +                       # gövde
        path("M40,112 L189,106 L189,124 L40,124 Z", 2.2) +     # sol kanat
        path("M390,112 L241,106 L241,124 L390,124 Z", 2.2) +   # sağ kanat
        line(196, 152, 196, 176, 2) + line(234, 152, 234, 176, 2) +
        circle(196, 180, 5, 2) + circle(234, 180, 5, 2)        # iniş takımı
    )
    if struts:
        body += line(205, 150, 96, 124, 2) + line(225, 150, 334, 124, 2)
    return svg(430, 210, body)


add("kanat-cantilever", [14462], _plane(False))
add("kanat-payandali", [14463], _plane(True))


# ── 020 · 14684 / 14685 DC elektrik şeması ───────────────────────────
# 14684: orta-sıfır ampermetre ibresi ortada → akü tam dolu
# 14685: yük göstergesi (loadmeter) sıfırda → alternatör arızalı
SPAN = 70  # kadran yayının uç açısı (derece)


def _gauge(cx, cy, r, needle_deg, left_label, right_label, mark_centre=False):
    """Yarım daire kadranlı gösterge. needle_deg: -SPAN sol uç, 0 tepe, +SPAN sağ uç.
    Uç etiketleri kadranın DIŞINA yazılır; böylece ibre hiçbir yazının üstüne gelmez."""
    out = circle(cx, cy, r, 2)
    out += path(f"M{cx - r + 5},{cy} A{r - 5},{r - 5} 0 0 1 {cx + r - 5},{cy}", 1.4)
    for tk in (-SPAN, -SPAN / 2, 0, SPAN / 2, SPAN):
        a = math.radians(tk - 90)
        L = 12 if (tk == 0 and mark_centre) else 8
        out += line(cx + (r - 5) * math.cos(a), cy + (r - 5) * math.sin(a),
                    cx + (r - 5 - L) * math.cos(a), cy + (r - 5 - L) * math.sin(a),
                    2.2 if (tk == 0 and mark_centre) else 1.4)
    for tk, s, anc in ((-SPAN, left_label, "end"), (SPAN, right_label, "start")):
        a = math.radians(tk - 90)
        out += txt(cx + (r + 9) * math.cos(a), cy + (r + 9) * math.sin(a) + 5,
                   s, 12, anc, "600")
    a = math.radians(needle_deg - 90)
    out += line(cx, cy + 6, cx + (r - 12) * math.cos(a), cy + (r - 12) * math.sin(a), 3)
    out += circle(cx, cy + 6, 3.5, 1, fill=INK)
    return out


def _battery(x, y):
    """Akü sembolü: uzun/kısa plaka çiftleri + şasi."""
    out = ""
    for i, (half, wdt) in enumerate(((16, 2.6), (8, 2.6), (16, 2.6), (8, 2.6))):
        yy = y + i * 11
        out += line(x - half, yy, x + half, yy, wdt)
    out += line(x, y + 33, x, y + 46, 2)
    out += line(x - 16, y + 46, x + 16, y + 46, 2.6)
    out += line(x - 10, y + 52, x + 10, y + 52, 2)
    out += line(x - 5, y + 58, x + 5, y + 58, 2)
    return out


def _dc_system(bat_gauge: str | None, alt_gauge: str | None) -> str:
    """Gösterge hangi kola verilirse o kolun içine seri bağlanır."""
    bus_y, bx, ax = 196, 120, 348
    parts = [line(66, bus_y, 410, bus_y, 4.5),
             txt(70, bus_y - 11, "BUS", 12, "start", "600")]

    # akü kolu
    if bat_gauge:
        parts += [line(bx, bus_y, bx, 236, 2), bat_gauge, line(bx, 312, bx, 330, 2)]
        parts.append(_battery(bx, 330))
        parts.append(txt(bx, 412, "BATTERY", 12, weight="600"))
    else:
        parts += [line(bx, bus_y, bx, 296, 2), _battery(bx, 296),
                  txt(bx, 378, "BATTERY", 12, weight="600")]

    # alternatör kolu
    if alt_gauge:
        parts += [line(ax, bus_y, ax, 236, 2), alt_gauge, line(ax, 312, ax, 330, 2),
                  circle(ax, 356, 26, 2), txt(ax, 361, "ALT", 12, weight="600"),
                  line(ax, 382, ax, 398, 2), line(ax - 16, 398, ax + 16, 398, 2.6)]
    else:
        parts += [line(ax, bus_y, ax, 300, 2), circle(ax, 326, 26, 2),
                  txt(ax, 331, "ALT", 12, weight="600"),
                  line(ax, 352, ax, 368, 2), line(ax - 16, 368, ax + 16, 368, 2.6)]

    # yükler
    for x in (170, 234, 298):
        parts.append(line(x, bus_y, x, 138, 2))
        parts.append(path(f"M{x - 13},138 L{x + 13},138 L{x + 13},112 L{x - 13},112 Z", 2))
        parts.append(line(x, 112, x, 96, 2))
        parts.append(line(x - 12, 96, x + 12, 96, 2))
    parts.append(txt(234, 80, "LOADS", 12, weight="600"))
    return svg(470, 440, "".join(parts))


# orta-sıfır ampermetre: akü kolunda seri, ibre tam ortada (sıfır)
_amm = _gauge(120, 274, 38, 0, "−", "+", mark_centre=True)
add("dc-ampermetre-sifir", [14684], _dc_system(_amm, None))

# loadmeter: alternatör kolunda seri, ibre sol uçta (0 amper)
_load = _gauge(348, 274, 38, -SPAN, "0", "60")
add("dc-loadmeter-sifir", [14685], _dc_system(None, _load))


# ── 020 · 14709 Pitot tüpü, toplam basınç oku ────────────────────────
add("pitot-toplam-basinc", [14709], svg(450, 220,
    # tüp gövdesi
    path("M120,88 L360,88 L360,132 L120,132 Z", 2.4) +
    path("M120,88 L96,96 L96,124 L120,132", 2.4) +
    # direk
    path("M300,132 L316,132 L316,180 L300,180 Z", 2) +
    line(280, 180, 336, 180, 2.4) +
    # statik delikler
    circle(180, 88, 4, 1.6, fill=INK) + circle(215, 88, 4, 1.6, fill=INK) +
    circle(180, 132, 4, 1.6, fill=INK) + circle(215, 132, 4, 1.6, fill=INK) +
    txt(198, 66, "static ports", 12) +
    line(198, 72, 198, 82, 1.2) +
    # hava akımı
    line(20, 86, 74, 86, 1.2, dash="7 5") + line(20, 134, 74, 134, 1.2, dash="7 5") +
    # toplam basınç oku
    arrow(20, 110, 92, 110, w=3.4, head=14)))


# ── 020 · 14790 Dört suni ufuk ───────────────────────────────────────
# Doğru: 3 numara = 40° sağ yatış + burun aşağı
# Sağ yatışta ufuk çizgisi saat yönünün tersine döner (sağ ucu yukarı),
# yer sağda daha geniş görünür. Burun aşağıda ufuk çizgisi uçak
# sembolünün üstüne çıkar.
def _ai(cx, cy, r, bank, pitch, num):
    """bank: + sağ yatış (derece).  pitch: + burun aşağı (piksel)."""
    cid = f"ai{num}"
    g = (f'<clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
         f'<g clip-path="url(#{cid})">'
         f'<g transform="translate({cx},{cy}) rotate({-bank})">'
         f'<rect x="-{r * 2}" y="{-pitch}" width="{r * 4}" height="{r * 2}" '
         f'fill="{GREY}" stroke="none"/>'
         + line(-r * 2, -pitch, r * 2, -pitch, 2.4) +
         "".join(line(-16, -pitch + d, 16, -pitch + d, 1.2)
                 for d in (-24, -12, 12, 24)) +
         "</g></g>")
    g += circle(cx, cy, r, 2.4)
    # sabit yatış skalası
    for a in (-60, -30, -20, -10, 0, 10, 20, 30, 60):
        rad = math.radians(a - 90)
        L = 10 if a in (-60, -30, 0, 30, 60) else 6
        g += line(cx + r * math.cos(rad), cy + r * math.sin(rad),
                  cx + (r + L) * math.cos(rad), cy + (r + L) * math.sin(rad), 1.6)
    # sabit tepe göstergesi — yatış, ufuk çizgisinin eğiminden okunur
    g += poly([(cx, cy - r + 2), (cx - 8, cy - r - 12), (cx + 8, cy - r - 12)],
              w=1.5, fill=INK)
    # sabit uçak sembolü
    g += (line(cx - 34, cy, cx - 12, cy, 3.4) + line(cx + 12, cy, cx + 34, cy, 3.4) +
          line(cx - 12, cy, cx - 6, cy + 7, 3.4) + line(cx + 12, cy, cx + 6, cy + 7, 3.4) +
          circle(cx, cy, 3.5, 2, fill=INK))
    g += txt(cx, cy + r + 34, str(num), 16, weight="700")
    return g


add("suni-ufuk-dortlu", [14790], svg(560, 216,
    _ai(78, 92, 54, 0, -32, 1) +      # düz kanat, burun yukarı
    _ai(218, 92, 54, -40, 32, 2) +    # 40° sol yatış, burun aşağı
    _ai(358, 92, 54, 40, 32, 3) +     # 40° sağ yatış, burun aşağı  ← doğru
    _ai(498, 92, 54, 40, -32, 4)))    # 40° sağ yatış, burun yukarı


# ── 030 · Tahterevalli ───────────────────────────────────────────────
# 14876 Fb = A·Fa / B   ve   14877 A = B·Fb / Fa  → ikisi de Fa·A = Fb·B
# 14878 Fc = Fa / 3     → Fa mesafe A'da, Fc mesafe 3A'da
def _seesaw(pivot, items, dims, w=470, h=260):
    """pivot: mesnet x'i.  items: (x, etiket, ok_boyu).  dims: (x1, x2, etiket)."""
    beam_y = 118
    out = line(46, beam_y, w - 46, beam_y, 5)
    out += poly([(pivot, beam_y + 4), (pivot - 24, beam_y + 44),
                 (pivot + 24, beam_y + 44)], 2.4)
    out += line(pivot - 36, beam_y + 44, pivot + 36, beam_y + 44, 2.4)
    for x, lab, L in items:
        out += arrow(x, beam_y - L - 8, x, beam_y - 8, w=2.8, head=12)
        out += txt(x, beam_y - L - 16, lab, 16, weight="700")
    out += line(pivot, beam_y + 6, pivot, 214, 1.2, dash="5 4")
    for x1, x2, lab in dims:
        for xx in (x1, x2):
            out += line(xx, beam_y + 6, xx, 208, 1.2, dash="5 4")
        out += dim(x1, 214, x2, lab)
    return svg(w, h, out)


# Fa·A = Fb·B  →  A=150 px, B=120 px olduğundan Fb, Fa'nın 1,25 katı
add("tahterevalli-a-b", [14876, 14877], _seesaw(
    235, [(85, "Fa", 56), (355, "Fb", 70)],
    [(85, 235, "A"), (235, 355, "B")]))

# Fa·A = Fc·3A  →  Fc = Fa/3; A=70 px, 3A=210 px
add("tahterevalli-3a", [14878], _seesaw(
    160, [(90, "Fa", 78), (370, "Fc", 26)],
    [(90, 160, "A"), (160, 370, "3A")], w=440))


# ── 030 · 14975 Azami menzil hızı ────────────────────────────────────
# Gerekli güç eğrisi. C = orijinden çizilen teğetin değdiği nokta
# (asgari sürükleme / en iyi L/D) → pervaneli uçakta azami menzil hızı.
def _power_curve(v):
    """Gerekli güç: a/v + v^3.  a, asgari güç hızı 60 kt olacak şekilde seçildi;
    orijinden teğetin değdiği nokta (azami menzil) 3^(1/4)·60 ≈ 79 kt'ye düşer."""
    return 38_880_000.0 / v + v ** 3


def _graph(w, h, ox, oy, ax_w, ax_h, xlab, ylab):
    return (line(ox, oy, ox, oy - ax_h, 2.4) + line(ox, oy, ox + ax_w, oy, 2.4) +
            arrow(ox, oy, ox, oy - ax_h - 8, w=2.4, head=10) +
            arrow(ox, oy, ox + ax_w + 8, oy, w=2.4, head=10) +
            txt(ox + ax_w / 2, oy + 34, xlab, 13, weight="600") +
            f'<g transform="rotate(-90 {ox - 34} {oy - ax_h / 2})">' +
            txt(ox - 34, oy - ax_h / 2, ylab, 13, weight="600") + "</g>")


_vs = [v for v in range(30, 126)]
_ps = [_power_curve(v) for v in _vs]
_pmin, _pmax = min(_ps), max(_ps)
_OX, _OY, _AW, _AH = 78, 250, 350, 200


def _px(v): return _OX + (v - 25) / 108 * _AW
def _py(p): return _OY - (p - 0) / (_pmax * 1.05) * _AH


_curve = "M" + " L".join(f"{_px(v):.1f},{_py(p):.1f}" for v, p in zip(_vs, _ps))
# teğet noktası: p/v oranı en küçük olan hız
_tan_v = min(_vs, key=lambda v: _power_curve(v) / v)
_min_v = min(_vs, key=lambda v: _power_curve(v))
_pts = [(40, "A"), (_min_v, "B"), (_tan_v, "C"), (110, "D")]

add("azami-menzil-guc", [14975], svg(470, 300,
    _graph(470, 300, _OX, _OY, _AW, _AH, "Speed (IAS)", "Power required") +
    path(_curve, 2.6) +
    "".join(line(_px(v), _OY, _px(v), _py(_power_curve(v)), 1.2, dash="5 4") +
            circle(_px(v), _py(_power_curve(v)), 4, 1.6, fill=INK) +
            txt(_px(v), _OY + 20, lab, 15, weight="700")
            for v, lab in _pts)))


# ── 050 · Bulut biçimleri ────────────────────────────────────────────
# 1 kümülüs · 2 altokümülüs lentikülaris · 3 altokümülüs kastellanus
# 4 kümülonimbus kapillatus
def _cloud_cumulus(x, y):
    return (path(f"M{x - 46},{y} L{x + 46},{y}", 2.4) +
            path(f"M{x - 46},{y} C{x - 52},{y - 26} {x - 34},{y - 34} {x - 24},{y - 30} "
                 f"C{x - 22},{y - 52} {x + 4},{y - 56} {x + 10},{y - 36} "
                 f"C{x + 26},{y - 44} {x + 48},{y - 26} {x + 46},{y} Z", 2.4))


def _cloud_lenticularis(x, y):
    return (path(f"M{x - 54},{y} C{x - 30},{y - 26} {x + 30},{y - 26} {x + 54},{y} "
                 f"C{x + 28},{y + 12} {x - 28},{y + 12} {x - 54},{y} Z", 2.4) +
            path(f"M{x - 34},{y - 34} C{x - 18},{y - 48} {x + 18},{y - 48} {x + 34},{y - 34} "
                 f"C{x + 16},{y - 26} {x - 16},{y - 26} {x - 34},{y - 34} Z", 2.2))


def _cloud_castellanus(x, y):
    body = path(f"M{x - 56},{y} L{x + 56},{y}", 2.4)
    top = f"M{x - 56},{y} L{x - 56},{y - 8} "
    for i in range(4):
        bx = x - 56 + 28 * i
        hh = (26, 36, 30, 22)[i]
        top += (f"C{bx + 2},{y - 8 - hh} {bx + 26},{y - 8 - hh} {bx + 28},{y - 8} ")
    top += f"L{x + 56},{y} Z"
    return body + path(top, 2.4)


def _cloud_cb(x, y):
    return (path(f"M{x - 44},{y} L{x + 44},{y}", 2.4) +
            path(f"M{x - 44},{y} L{x - 30},{y - 60} L{x + 28},{y - 60} L{x + 44},{y} Z", 2.4) +
            path(f"M{x - 30},{y - 60} C{x - 62},{y - 66} {x - 66},{y - 84} {x - 40},{y - 88} "
                 f"L{x + 38},{y - 88} C{x + 66},{y - 84} {x + 60},{y - 66} {x + 28},{y - 60} Z",
                 2.4) +
            "".join(line(x - 34 + 12 * i, y - 88, x - 30 + 12 * i, y - 96, 1.2)
                    for i in range(7)))


add("bulut-dortlu", [15525, 15526, 15527, 15528], svg(560, 220, "".join([
    _cloud_cumulus(80, 170), txt(80, 202, "1", 16, weight="700"),
    _cloud_lenticularis(220, 158), txt(220, 202, "2", 16, weight="700"),
    _cloud_castellanus(360, 170), txt(360, 202, "3", 16, weight="700"),
    _cloud_cb(500, 170), txt(500, 202, "4", 16, weight="700"),
])))


# ── 050 · 15571 / 20939 Oklüzyon cephesi ─────────────────────────────
# Aynı taraftaki üçgen + yarım daire dizisi = oklüzyon.
def _front_line():
    y = 110
    out = line(50, y, 430, y, 3)
    x = 82
    flip = True
    while x < 410:
        if flip:
            out += poly([(x - 15, y), (x + 15, y), (x, y - 26)], 2, fill=INK)
        else:
            out += path(f"M{x - 15},{y} A15,15 0 0 1 {x + 15},{y} Z", 2, fill=INK)
        x += 62
        flip = not flip
    return out


add("cephe-okluzyon", [15571, 20939], svg(480, 190, _front_line()))


# ── 050 · 15611 Rüzgâr oku: 270 dereceden 65 kt ──────────────────────
# Sap, rüzgârın GELDİĞİ yöne uzanır → 270° = batı = sola.
# Kuzey yarım kürede tüyler kuzey (yukarı) tarafa çizilir.
# 65 kt = 1 flama (50) + 1 tam tüy (10) + 1 yarım tüy (5)
def _wind_barb():
    sx, sy = 340, 158
    out = circle(sx, sy, 7, 2.6)
    out += line(sx - 7, sy, 120, sy, 2.6)
    # flama (50 kt) — en dış uçta, dolu üçgen
    out += poly([(120, sy), (120, sy - 40), (146, sy)], 2, fill=INK)
    # tam tüy (10 kt)
    out += line(170, sy, 152, sy - 36, 2.8)
    # yarım tüy (5 kt)
    out += line(196, sy, 187, sy - 18, 2.8)
    # kuzey oku
    out += arrow(418, 126, 418, 62, w=2.2, head=12)
    out += txt(418, 50, "N", 15, weight="700")
    return out


add("ruzgar-oku-65kt-270", [15611], svg(470, 210, _wind_barb()))


# ── 080 · 16126 Kanat profilinde V1 ve V2 ────────────────────────────
# V1 = ön kenardaki durma noktası (0), V2 = üst yüzeyde hızlanan akım (> V)
_AIRFOIL = ("M92,150 C150,110 250,96 340,110 C382,118 400,128 404,134 "
            "C360,148 220,166 140,162 C112,160 96,156 92,150 Z")
add("kanat-v1-v2", [16126], svg(470, 230, "".join([
    path(_AIRFOIL, 2.6),
    # serbest akım
    "".join(arrow(18, y, 74, y, w=1.8, head=9, dash="6 4") for y in (86, 120, 176)),
    txt(46, 76, "V", 15, weight="700", style="italic"),
    # üst akım çizgisi
    path("M74,120 C150,84 250,72 350,92 C392,100 420,112 440,124", 1.4, dash="7 5"),
    # alt akım çizgisi
    path("M74,176 C150,182 260,186 350,170 C392,162 420,150 440,140", 1.4, dash="7 5"),
    circle(93, 150, 5, 2, fill=INK),
    line(93, 150, 66, 210, 1.4), txt(60, 224, "V1", 15, weight="700"),
    circle(214, 88, 5, 2, fill=INK),
    line(214, 88, 214, 46, 1.4), txt(214, 38, "V2", 15, weight="700"),
])))


# ── 080 · 16160 Sürükleme eğrileri ───────────────────────────────────
# 1 indüklenen (hızla azalır) · 2 parazit (hızla artar)
# 3 toplam · 4 daha ağır uçuş ağırlığında toplam
_DOX, _DOY, _DAW, _DAH = 78, 250, 350, 200


def _dx(v): return _DOX + (v - 20) / 115 * _DAW
def _dy(d): return _DOY - d / 1150 * _DAH


def _induced(v, k=520000.0): return k / (v * v)
def _parasite(v): return 0.075 * v * v


def _curve_path(f, lo=30, hi=132, clip=1150):
    pts = []
    for v in range(lo, hi + 1):
        d = f(v)
        if d > clip:
            continue
        pts.append(f"{_dx(v):.1f},{_dy(d):.1f}")
    return "M" + " L".join(pts)


def _tag(v, val, num, dx=0, dy=0):
    """Eğri üstünde nokta + kılavuz + numara."""
    px, py = _dx(v), _dy(val)
    lx, ly = px + dx, py + dy
    return (line(lx, ly, px, py, 1.2) + circle(px, py, 3.6, 1.4, fill=INK) +
            txt(lx, ly + (5 if dy < 0 else 13), str(num), 15, weight="700"))


_THRUST = 980.0
add("surukleme-egrileri", [16160], svg(470, 310, "".join([
    _graph(470, 310, _DOX, _DOY, _DAW, _DAH, "Speed (IAS)", "Drag / Thrust"),
    path(_curve_path(_induced), 2.6),
    path(_curve_path(_parasite), 2.6),
    path(_curve_path(lambda v: _induced(v) + _parasite(v)), 2.6),
    line(_dx(30), _dy(_THRUST), _dx(126), _dy(_THRUST), 2.6),
    _tag(110, _induced(110), 1, dy=-20),
    _tag(70, _parasite(70), 2, dy=14),
    _tag(52, _induced(52) + _parasite(52), 3, dy=-20),
    _tag(45, _THRUST, 4, dy=-16),
])))


# ── 080 · 16304 Dönüşteki kuvvet vektörleri ──────────────────────────
# B = toplam taşıma (kanada dik), A = düşey bileşen, C = yatay bileşen, W = ağırlık
def _turn_vectors():
    """Arkadan görünüş, sağa yatış: sağ kanat aşağıda (saat yönünde dönme).
    B = toplam taşıma (kanada dik), A = düşey bileşen, C = yatay bileşen, W = ağırlık."""
    ox, oy = 168, 250
    bank = 32
    L = 150
    hx = L * math.tan(math.radians(bank))
    # sağa yatışta kanat çizgisi saat yönünde döner
    out = (f'<g transform="rotate({bank} {ox} {oy})" opacity="0.55">' +
           line(ox - 78, oy, ox + 78, oy, 2.2) +
           ellipse(ox, oy, 13, 19, 1.8) +
           line(ox, oy - 19, ox, oy - 40, 1.8) +
           line(ox - 22, oy - 40, ox + 22, oy - 40, 1.8) + "</g>")
    # tamamlayıcı kesikli kenarlar (vektörlerin altında kalsın)
    out += line(ox, oy - L, ox + hx, oy - L, 1.4, dash="6 4")
    out += line(ox + hx, oy, ox + hx, oy - L, 1.4, dash="6 4")
    # vektörler
    out += arrow(ox, oy, ox, oy - L, w=2.8, head=12)
    out += txt(ox - 15, oy - L + 20, "A", 16, "end", "700")
    out += arrow(ox, oy, ox + hx, oy - L, w=3.6, head=15)
    out += txt(ox + hx + 16, oy - L + 4, "B", 16, "start", "700")
    out += arrow(ox, oy, ox + hx, oy, w=2.8, head=12)
    out += txt(ox + hx / 2, oy + 26, "C", 16, weight="700")
    out += arrow(ox, oy, ox, oy + L, w=2.8, head=12)
    out += txt(ox - 15, oy + L - 12, "W", 16, "end", "700")
    return out


add("donus-vektorleri", [16304], svg(400, 432, _turn_vectors()))


# ── yaz ──────────────────────────────────────────────────────────────
def main() -> None:
    OUT.mkdir(exist_ok=True)
    for name, markup in FIGS.items():
        (OUT / f"{name}.svg").write_text(markup, encoding="utf-8")
    (OUT / "index.json").write_text(
        json.dumps(MAP, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"{OUT}: {len(FIGS)} çizim, {len(MAP)} soru eşlendi")


if __name__ == "__main__":
    main()
