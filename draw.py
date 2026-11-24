#!/usr/bin/env python3
"""news-23 b92 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"

def f_serif_b(sz): return ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", sz)
def f_sans_b(sz): return ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", sz)
def f_sans(sz): return ImageFont.truetype(FD + "DejaVuSans.ttf", sz)
def f_sans_o(sz): return ImageFont.truetype(FD + "DejaVuSans-Oblique.ttf", sz)

BLACK = (12, 12, 12)
WHITE = (255, 255, 255)
PAPER = (250, 248, 240)
INK = (20, 20, 20)
GRAY = (110, 110, 110)
RED = (178, 24, 24)
NAVY = (16, 42, 90)
TEAL = (0, 120, 120)
GOLD = (176, 132, 16)
GOLD_L = (212, 168, 60)
GREEN = (22, 110, 44)
PURPLE = (96, 48, 128)
BLUE_CHIP = (24, 72, 160)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def wrap(s, font, maxw):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def chip(x, y, label, fill):
    f = f_sans_b(9)
    w = int(d.textlength(label, font=f)) + 10
    d.rounded_rectangle([x, y, x + w, y + 12], radius=2, fill=fill)
    d.text((x + 5, y + 1), label, font=f, fill=WHITE)
    return w

# ---------- masthead ----------
d.rectangle([0, 0, W, 58], fill=BLACK)
text(10, 8, "THE WORLD TODAY", f_serif_b(34), WHITE)
text(W - 10, 18, "MONDAY 23 NOVEMBER 2026", f_sans_b(16), GOLD_L, anchor="ra")

# ---------- kicker ----------
d.rectangle([0, 58, W, 78], fill=RED)
text(10, 63, "AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at record low  ·  Anthropic IPO $107.3B",
     f_sans_b(13), WHITE)

# ---------- number strip (5 cols x 2 rows) ----------
nums = [
    ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", NAVY),
    ("11,762", "EBOLA CASES, DRC", TEAL), ("10T won", "SEOUL STABILISATION FUND", GOLD),
    ("2%", "BILLIONAIRE TAX IN PARIS", GREEN),
    ("$450M", "SKUBAL DEAL", NAVY), ("165", "RUSSIAN MISSILES/WEEK", RED),
    ("12,000", "CLEARED IN MANCHESTER", TEAL), ("264 kg", "EXPLOSIVES SEIZED", GOLD),
    ("$107.3B", "ANTHROPIC IPO", GREEN),
]
for i, (v, lab, col) in enumerate(nums):
    col_i, row_i = i % 5, i // 5
    x = 10 + col_i * 202
    y = 82 + row_i * 31
    text(x, y, v, f_sans_b(17), col)
    text(x, y + 19, lab, f_sans(8), GRAY)
d.line([0, 144, W, 144], fill=(200, 195, 180), width=1)

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", NAVY, 190), ("AMERICAS 8", RED, 185),
           ("MIDDLE EAST 6", GOLD, 175), ("EUROPE 5", TEAL, 160),
           ("AFRICA 3", PURPLE, 150), ("WORLD 2", (90, 90, 90), 138)]
x = 8
for name, col, w in regions:
    d.rectangle([x, 148, x + w, 162], fill=col)
    text(x + 6, 151, name, f_sans_b(10), WHITE)
    x += w + 2

# ---------- UTC strip ----------
d.line([0, 166, W, 166], fill=(200, 195, 180), width=1)
text(10, 168, "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
     f_sans(10), (70, 70, 70))
text(W - 10, 168, "~ APPROX", f_sans(10), GRAY, anchor="ra")

# ---------- heroes ----------
HX = [8, 348, 688]
HW = 328
HY = 184          # hero block top
SCENE_H = 108     # scene 184..292
HEAD_Y = 296
BODY_Y = 336
SRC_Y = 366

def hero_scene_kospi(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(10, 24, 64))
    # buildings with lit windows
    import random
    rnd = random.Random(7)
    bx = x0 + 4
    while bx < x0 + w - 30:
        bw = rnd.randint(22, 38)
        bh = rnd.randint(34, 66)
        by = y0 + h - 18 - bh
        d.rectangle([bx, by, bx + bw, y0 + h - 18], fill=(24, 44, 96))
        for wy in range(by + 5, y0 + h - 22, 9):
            for wx in range(bx + 4, bx + bw - 3, 8):
                if rnd.random() < 0.45:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 110))
        bx += bw + 4
    # orange chart line (below the big number, above the bottom strip)
    pts = [(x0 + 8, y0 + 62), (x0 + 55, y0 + 48), (x0 + 105, y0 + 58),
           (x0 + 160, y0 + 40), (x0 + 215, y0 + 52), (x0 + 270, y0 + 34),
           (x0 + 318, y0 + 42)]
    d.line(pts, fill=(255, 140, 40), width=3)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=WHITE, outline=(255, 140, 40))
    text(x0 + 8, y0 + 6, "-3.3%", f_sans_b(26), (255, 90, 60))
    d.rectangle([x0, y0 + h - 18, x0 + w, y0 + h], fill=BLACK)
    text(x0 + 8, y0 + h - 16, "KOSPI 4,708.54  ·  -161 PTS", f_sans_b(10), WHITE)

def hero_scene_guterres(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(18, 96, 44))
    # globe on the right
    cx, cy, r = x0 + w - 48, y0 + h // 2, 36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 220, 180), outline=(220, 240, 220), width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(90, 160, 110), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(90, 160, 110), width=1)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 180, fill=(90, 160, 110), width=1)
    # gold text, 3 lines, kept clear of the globe (text width <= 200)
    text(x0 + 10, y0 + 8, "150 DELEGATES", f_sans_b(24), (255, 210, 90))
    text(x0 + 10, y0 + 36, "BACK A RISK", f_sans_b(24), (255, 210, 90))
    text(x0 + 10, y0 + 64, "FRAMEWORK", f_sans_b(24), (255, 210, 90))
    d.rectangle([x0, y0 + h - 18, x0 + w, y0 + h], fill=BLACK)
    text(x0 + 8, y0 + h - 16, "UN  ·  BRIDGETOWN", f_sans_b(10), WHITE)

def hero_scene_power(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(246, 240, 222))
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=(200, 190, 160), width=1)
    text(x0 + 8, y0 + 6, "NARROWEST SINCE 2018", f_sans_b(10), INK)
    text(x0 + w - 8, y0 + 6, "GAP 5.3", f_sans_b(10), RED, anchor="ra")
    # bars: values INSIDE bars, labels INSIDE bars near bottom
    bars = [("78.9", "US", NAVY, 62), ("73.6", "CHINA", RED, 58), ("40.5", "INDIA", GOLD, 34)]
    bx = x0 + 18
    base = y0 + h - 20
    for val, lab, col, bh in bars:
        d.rectangle([bx, base - bh, bx + 82, base], fill=col)
        text(bx + 41, base - bh + 5, val, f_sans_b(15), WHITE, anchor="ma")
        text(bx + 41, base - 16, lab, f_sans_b(10), WHITE, anchor="ma")
        bx += 100
    d.rectangle([x0, y0 + h - 18, x0 + w, y0 + h], fill=BLACK)
    text(x0 + 8, y0 + h - 16, "ASIA POWER INDEX 2026", f_sans_b(10), WHITE)

heroes = [
    (hero_scene_kospi, "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE"),
    (hero_scene_guterres, "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS"),
    (hero_scene_power, "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 - gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE"),
]
for (scene_fn, headline, body, source), x0 in zip(heroes, HX):
    scene_fn(x0, HY, HW, SCENE_H)
    lines = wrap(headline, f_sans_b(19), HW)
    y = HEAD_Y
    for ln in lines[:2]:
        text(x0, y, ln, f_sans_b(19), INK)
        y += 20
    blines = wrap(body, f_sans(11), HW)
    y = BODY_Y
    for ln in blines[:2]:
        text(x0, y, ln, f_sans(11), INK)
        y += 13
    text(x0, SRC_Y, source, f_sans(9), GRAY)
    cw = chip(x0 + HW - 62, SRC_Y - 1, "REPORTED", BLUE_CHIP)

# ---------- MORE OF THE DAY strip ----------
d.rectangle([0, 404, W, 422], fill=BLACK)
text(10, 408, "MORE OF THE DAY  —  10 STORIES", f_sans_b(12), WHITE)

# ---------- cards ----------
cards = [
    ("AMERICAS", NAVY, "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED"),
    ("FBI", (60, 60, 60), "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("WHITE HOUSE", GOLD, "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", TEAL, "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", RED, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED"),
    ("SPORT", RED, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("LEGAL", PURPLE, "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("TECH", TEAL, "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", NAVY, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", PURPLE, "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
CW, CH, CG = 196, 86, 6
for i, (cat, col, head, body, src, kind) in enumerate(cards):
    r, c = divmod(i, 5)
    x0 = 8 + c * (CW + CG)
    y0 = 422 + 6 + r * (CH + 4)
    d.rectangle([x0, y0, x0 + CW, y0 + CH], fill=WHITE, outline=(200, 195, 180), width=1)
    d.rectangle([x0, y0, x0 + CW, y0 + 15], fill=col)
    text(x0 + 5, y0 + 2, cat, f_sans_b(9), WHITE)
    text(x0 + CW - 5, y0 + 2, str(i + 1), f_sans_b(9), WHITE, anchor="ra")
    hlines = wrap(head, f_sans_b(12), CW - 10)
    y = y0 + 19
    for ln in hlines[:2]:
        text(x0 + 5, y, ln, f_sans_b(12), INK)
        y += 14
    text(x0 + 5, y0 + 52, body, f_sans(10), (60, 60, 60))
    text(x0 + 5, y0 + 70, src, f_sans(9), GRAY)
    chip(x0 + CW - 67, y0 + 69, kind, BLUE_CHIP if kind == "REPORTED" else RED)

# ---------- WHERE IT HAPPENED / ALSO strip ----------
d.rectangle([0, 606, W, 624], fill=BLACK)
text(10, 610, "WHERE IT HAPPENED", f_sans_b(12), WHITE)
text(348, 610, "ALSO ON MONDAY", f_sans_b(12), WHITE)

# ---------- map ----------
MAP = (8, 630, 332, 832)
d.rectangle(MAP, fill=WHITE, outline=(160, 155, 140), width=1)
LAND = (196, 222, 178)
# Americas blob
d.polygon([(22, 648), (120, 636), (150, 658), (138, 708), (118, 738), (108, 778),
           (92, 808), (78, 770), (58, 728), (34, 698), (20, 668)], fill=LAND)
# Europe blob
d.polygon([(178, 644), (232, 636), (246, 658), (238, 690), (210, 704), (182, 690),
           (170, 664)], fill=LAND)
# Asia blob
d.polygon([(250, 640), (312, 632), (326, 656), (318, 698), (300, 724), (272, 714),
           (252, 688), (244, 660)], fill=LAND)
# Africa blob
d.polygon([(186, 708), (238, 704), (252, 732), (240, 774), (214, 790), (192, 764),
           (180, 732)], fill=LAND)
# Australia
d.polygon([(282, 780), (322, 776), (328, 796), (300, 806), (282, 794)], fill=LAND)

pins = [
    (1, "Seoul", 302, 676), (2, "Bridgetown", 92, 764), (3, "Beijing", 288, 658),
    (4, "Washington", 132, 672), (5, "New York", 142, 648), (6, "Kyiv", 214, 674),
    (7, "Chicago", 118, 698), (8, "SF", 58, 698), (9, "Denver", 84, 728),
    (10, "Austin", 108, 738), (11, "Warsaw", 238, 682), (12, "London", 192, 658),
    (13, "Moscow", 262, 664),
]
for n, name, px, py in pins:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
    d.text((px, py - 5), str(n), font=f_sans_b(8), fill=WHITE, anchor="ma")
text(14, 796, "Pins 1-13:  1 Seoul · 2 Bridgetown · 3 Beijing", f_sans(8), GRAY)
text(14, 806, "4 Washington · 5 New York · 6 Kyiv · 7 Chicago · 8 SF", f_sans(8), GRAY)
text(14, 816, "9 Denver · 10 Austin · 11 Warsaw · 12 London · 13 Moscow", f_sans(8), GRAY)

# ---------- ALSO list ----------
also = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week",
    "17. COP31: the day after Antalya pact rejected",
    "18. Benghazi: UN demands probe [CLAIM]",
    "19. Israel unity talks resume",
    "20. Gaza: two killed in Israeli strike",
    "21. West Bank settler attacks",
    "22. Iran war: no deal in sight",
    "23. Lebanon seizes 264 kg explosives",
    "24. Bahrain: strike hits plant, 2 hurt",
    "25. Sudan: defences down drones [CLAIM]",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row",
    "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
for i, item in enumerate(also):
    col_i, row_i = i // 9, i % 9
    x = 348 + col_i * 336
    y = 636 + row_i * 21
    if "[CLAIM]" in item:
        base, _ = item.split(" [CLAIM]")
        text(x, y, base, f_sans(11), INK)
        w = d.textlength(base, font=f_sans(11))
        text(x + w + 4, y, "[CLAIM]", f_sans_b(10), RED)
    else:
        text(x, y, item, f_sans(11), INK)

# ---------- DATE CHECK ----------
d.rectangle([8, 832, 1016, 904], outline=RED, width=2)
text(14, 838, "DATE CHECK", f_sans_b(13), RED)
text(1010, 838, "READ 23 NOV 2026, 23:59 UTC — STORIES DATED 23 NOV ONLY", f_sans_b(9), RED, anchor="ra")
text(14, 858, "LEFT OUT — NOT 23 NOV:  Dems 258 seats (22 Nov)  ·  Sparta II fire (22 Nov)  ·  El Chapo (22 Nov)  ·  EU-Indonesia (21 Nov)  ·  Nigeria boat (21 Nov)  ·  ICJ Myanmar (19 Nov)",
     f_sans(11), INK)
text(14, 878, "NOT YET — Dymer search continues (14 missing)  ·  4 House races uncalled  ·  COP32 venue not set  ·  WHO evacuating trapped Ebola staff",
     f_sans(11), INK)

# ---------- footer ----------
text(10, 912, "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · NYT · ESPN · Lowy Institute (Asia Power Index 2026).",
     f_sans(10), GRAY)
text(10, 928, "CHIPS: REPORTED = confirmed by wires.  CLAIM = one side's claim, not independently confirmed.  ONGOING = still developing.",
     f_sans(10), GRAY)
text(10, 944, "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
     f_sans(10), GRAY)
d.line([8, 964, 1016, 964], fill=GOLD, width=2)
text(W // 2, 972, "THE WORLD TODAY  —  Monday 23 November 2026  ·  31 stories  ·  6 regions",
     f_sans_b(13), GOLD, anchor="ma")

img.save(OUT, optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
