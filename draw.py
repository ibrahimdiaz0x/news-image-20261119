#!/usr/bin/env python3
"""Draw entry.png: a one-page front page summing up Thursday 19 November 2026.

Original flat artwork rendered with PIL + DejaVu fonts. Generated locally;
the sandbox entrypoint (main.py) only copies the finished entry.png.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (244, 238, 226)
INK = (24, 24, 24)
NAVY = (20, 32, 58)
GOLD = (228, 196, 112)
RED = (186, 32, 40)
CARD = (255, 255, 255)
BORDER = (214, 208, 194)
SUBINK = (62, 62, 62)
FOOTINK = (105, 105, 105)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


F_KICK = font("DejaVuSans-Bold.ttf", 19)
F_DATE = font("DejaVuSerif-Bold.ttf", 52)
F_SUBKICK = font("DejaVuSans.ttf", 18)
F_TAG = font("DejaVuSans-Bold.ttf", 14)
F_HEAD = font("DejaVuSerif-Bold.ttf", 27)
F_SUB = font("DejaVuSans.ttf", 18)
F_FOOT = font("DejaVuSans.ttf", 16)


def centered(d, cx, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def spiral(d, cx, cy, turns, r0, r1, fill, width=4):
    """An Archimedean spiral, for the cyclone."""
    steps = int(turns * 72)
    pts = []
    for i in range(steps + 1):
        t = i / steps
        a = t * turns * 2 * math.pi
        r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.line(pts, fill=fill, width=width, joint="curve")


def sun_rays(d, cx, cy, r, fill, width=3):
    for k in range(12):
        a = math.radians(k * 30)
        x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        x2, y2 = cx + (r + 10) * math.cos(a), cy + (r + 10) * math.sin(a)
        d.line([(x1, y1), (x2, y2)], fill=fill, width=width)


# ---------------- icon scenes (each in a 280x140 box) ----------------

def icon_summit(d, x, y):
    # Shenzhen skyline at dusk, three flags in front
    d.rectangle([x, y, x + 280, y + 140], fill=(223, 231, 244))
    d.rectangle([x, y + 112, x + 280, y + 140], fill=(120, 140, 165))
    # towers
    for bx, bw, bh in ((18, 34, 74), (60, 26, 96), (94, 40, 60),
                       (142, 30, 108), (180, 36, 70), (224, 28, 88)):
        d.rectangle([x + bx, y + 112 - bh, x + bx + bw, y + 112],
                    fill=(58, 74, 102))
        for wy in range(y + 112 - bh + 8, y + 108, 14):
            for wx in range(x + bx + 5, x + bx + bw - 4, 9):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(232, 201, 122))
    # three flags: US, China, Russia
    for fx, flag in ((34, "us"), (118, "cn"), (202, "ru")):
        d.line([(x + fx, y + 118), (x + fx, y + 52)], fill=(70, 70, 70), width=3)
        if flag == "us":
            for s in range(4):
                d.rectangle([x + fx, y + 52 + s * 7, x + fx + 44, y + 59 + s * 7],
                            fill=(178, 34, 52) if s % 2 == 0 else (255, 255, 255))
            d.rectangle([x + fx, y + 52, x + fx + 20, y + 66], fill=(40, 60, 120))
        elif flag == "cn":
            d.rectangle([x + fx, y + 52, x + fx + 44, y + 80], fill=(222, 41, 16))
            d.ellipse([x + fx + 5, y + 57, x + fx + 13, y + 65], fill=(255, 222, 0))
        else:
            d.rectangle([x + fx, y + 52, x + fx + 44, y + 61], fill=(255, 255, 255))
            d.rectangle([x + fx, y + 61, x + fx + 44, y + 70], fill=(0, 57, 166))
            d.rectangle([x + fx, y + 70, x + fx + 44, y + 79], fill=(213, 0, 50))
    # table with three chairs, seen from above the skyline base
    d.ellipse([x + 96, y + 122, x + 184, y + 136], fill=(150, 110, 70))


def icon_scales(d, x, y):
    # Courthouse + scales of justice
    d.rectangle([x, y, x + 280, y + 140], fill=(228, 232, 240))
    # pediment + columns
    d.polygon([(x + 70, y + 30), (x + 140, y + 8), (x + 210, y + 30)],
              fill=(70, 88, 112))
    d.rectangle([x + 66, y + 30, x + 214, y + 36], fill=(70, 88, 112))
    for cx in (88, 118, 148, 178):
        d.rectangle([x + cx - 6, y + 36, x + cx + 6, y + 84], fill=(245, 245, 245),
                    outline=(140, 148, 158), width=2)
    d.rectangle([x + 60, y + 84, x + 220, y + 90], fill=(120, 130, 142))
    # scales
    cx, cy = x + 140, y + 112
    d.line([(cx, cy - 4), (cx, cy + 16)], fill=(60, 60, 60), width=4)
    d.line([(cx - 26, cy - 4), (cx + 26, cy - 4)], fill=(60, 60, 60), width=4)
    for px in (cx - 26, cx + 26):
        d.line([(px, cy - 4), (px, cy + 6)], fill=(60, 60, 60), width=3)
        d.polygon([(px - 12, cy + 6), (px + 12, cy + 6), (px, cy + 18)],
                  fill=(186, 32, 40))
    d.ellipse([cx - 4, cy - 12, cx + 4, cy - 4], fill=(60, 60, 60))
    d.rectangle([x + 96, y + 128, x + 184, y + 134], fill=(60, 60, 60))


def icon_tower(d, x, y):
    # Riyadh tower struck: tall skyscraper, flash at the top, missile trail
    d.rectangle([x, y, x + 280, y + 140], fill=(250, 226, 214))
    # tower (tapering, with the PIF Tower's slanted top)
    d.polygon([(x + 118, y + 132), (x + 118, y + 26), (x + 162, y + 26),
               (x + 162, y + 132)], fill=(88, 96, 110))
    d.polygon([(x + 118, y + 26), (x + 162, y + 26), (x + 150, y + 12),
               (x + 130, y + 12)], fill=(70, 78, 92))
    for wy in range(y + 34, y + 128, 12):
        d.rectangle([x + 124, wy, x + 156, wy + 5], fill=(210, 220, 235))
    # city base
    d.rectangle([x, y + 132, x + 280, y + 140], fill=(120, 110, 100))
    for bx, bw, bh in ((24, 30, 34), (60, 26, 48), (196, 30, 40), (232, 28, 30)):
        d.rectangle([x + bx, y + 132 - bh, x + bx + bw, y + 132],
                    fill=(140, 132, 120))
    # explosion flash at the tower top
    fx, fy = x + 140, y + 18
    sun_rays(d, fx, fy, 12, (255, 140, 0), 4)
    d.ellipse([fx - 12, fy - 12, fx + 12, fy + 12], fill=(255, 196, 0))
    d.ellipse([fx - 6, fy - 6, fx + 6, fy + 6], fill=(255, 90, 0))
    # missile streak from the upper right
    d.line([(x + 268, y + 8), (x + 196, y + 22)], fill=(150, 150, 150), width=3)
    d.line([(x + 268, y + 8), (x + 252, y + 12)], fill=(60, 60, 60), width=5)


def icon_knesset(d, x, y):
    # Parliament dome + ballot box with a check
    d.rectangle([x, y, x + 280, y + 140], fill=(226, 234, 240))
    # dome building
    d.rectangle([x + 58, y + 74, x + 222, y + 118], fill=(110, 122, 140))
    d.arc([x + 104, y + 34, x + 176, y + 96], 180, 360, fill=(110, 122, 140),
          width=10)
    d.rectangle([x + 138, y + 30, x + 142, y + 44], fill=(110, 122, 140))
    for cx in (76, 108, 140, 172, 204):
        d.rectangle([x + cx - 5, y + 78, x + cx + 5, y + 118],
                    fill=(240, 240, 240))
    d.rectangle([x + 52, y + 118, x + 228, y + 124], fill=(90, 100, 116))
    # ballot box with a green check
    d.rectangle([x + 196, y + 96, x + 258, y + 126], fill=(255, 255, 255),
                outline=(60, 60, 60), width=3)
    d.line([(x + 206, y + 112), (x + 218, y + 122), (x + 244, y + 100)],
           fill=(34, 139, 34), width=5)
    # small flag
    d.line([(x + 30, y + 118), (x + 30, y + 78)], fill=(70, 70, 70), width=3)
    d.rectangle([x + 30, y + 78, x + 62, y + 96], fill=(255, 255, 255),
                outline=(40, 90, 180), width=2)
    d.polygon([(x + 36, y + 82), (x + 46, y + 92), (x + 56, y + 82)],
              fill=(40, 90, 180))


def icon_cyclone(d, x, y):
    # Cyclone spiral over the sea, rain bands, coastline arrow
    d.rectangle([x, y, x + 280, y + 140], fill=(222, 236, 242))
    d.rectangle([x, y + 100, x + 280, y + 140], fill=(46, 94, 140))
    for wx in range(x + 8, x + 272, 34):
        d.arc([wx, y + 108, wx + 26, y + 122], 200, 340,
              fill=(255, 255, 255), width=3)
    # coastline
    d.polygon([(x + 8, y + 140), (x + 40, y + 104), (x + 72, y + 118),
               (x + 96, y + 140)], fill=(70, 130, 80))
    # storm spiral
    spiral(d, x + 170, y + 56, 2.4, 4, 46, (30, 60, 110), 5)
    d.ellipse([x + 164, y + 50, x + 176, y + 62], fill=(186, 32, 40))
    # rain streaks
    for rx in (x + 96, x + 118, x + 232, x + 252):
        d.line([(rx, y + 78), (rx - 6, y + 96)], fill=(120, 160, 200), width=3)
    # arrow toward the coast
    d.line([(x + 232, y + 30), (x + 200, y + 52)], fill=RED, width=5)
    d.polygon([(x + 192, y + 44), (x + 214, y + 40), (x + 204, y + 60)],
              fill=RED)


def icon_game(d, x, y):
    # Neon dusk skyline + game controller
    d.rectangle([x, y, x + 280, y + 140], fill=(38, 22, 64))
    # sun disc
    d.ellipse([x + 196, y + 12, x + 252, y + 68], fill=(255, 120, 60))
    # skyline
    for bx, bw, bh in ((12, 30, 58), (48, 24, 82), (78, 34, 48),
                       (118, 28, 96), (152, 32, 66), (190, 26, 78),
                       (222, 30, 54)):
        d.rectangle([x + bx, y + 140 - bh, x + bx + bw, y + 140],
                    fill=(16, 10, 28))
        for wy in range(y + 140 - bh + 8, y + 136, 13):
            for wx in range(x + bx + 5, x + bx + bw - 4, 9):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
    # controller, floating over the skyline
    cx, cy = x + 96, y + 52
    d.rounded_rectangle([cx - 52, cy - 22, cx + 52, cy + 22], radius=18,
                        fill=(240, 240, 245), outline=(30, 30, 40), width=3)
    d.ellipse([cx - 34, cy - 4, cx - 20, cy + 10], fill=(30, 30, 40))
    d.ellipse([cx + 20, cy - 10, cx + 34, cy + 4], fill=(30, 30, 40))
    for dx, dy, c in ((-8, -12, (186, 32, 40)), (2, -12, (40, 120, 60)),
                      (-8, -2, (40, 90, 180)), (2, -2, (220, 180, 0))):
        d.ellipse([cx + dx - 4, cy + dy - 4, cx + dx + 4, cy + dy + 4], fill=c)
    d.line([(cx - 44, cy + 6), (cx - 44, cy + 16)], fill=(30, 30, 40), width=3)
    d.line([(cx - 49, cy + 11), (cx - 39, cy + 11)], fill=(30, 30, 40), width=3)


PANELS = [
    ("ASIA-PACIFIC  •  DIPLOMACY", (40, 90, 170), "THREE LEADERS, ONE TABLE",
     "Trump, Xi and Putin hold the first three-way summit in Shenzhen; a joint declaration on nuclear risks and energy.",
     icon_summit),
    ("INTERNATIONAL LAW  •  JUSTICE", (110, 60, 140), "WORLD COURT: MYANMAR GUILTY",
     "The ICJ rules 9\u20136 that Myanmar committed genocide against the Rohingya.",
     icon_scales),
    ("MIDDLE EAST  •  WAR", (186, 32, 40), "MISSILE HITS RIYADH TOWER",
     "An apparent Houthi missile damages the PIF Tower in the Saudi capital as the Iran war widens.",
     icon_tower),
    ("ISRAEL  •  POLITICS", (30, 90, 120), "EISENKOT TAPPED TO LEAD ISRAEL",
     "Herzog asks the ex-army chief to form the next government, bypassing Netanyahu.",
     icon_knesset),
    ("SOUTH ASIA  •  WEATHER", (20, 100, 150), "CYCLONE AKVAN BEARS DOWN",
     "The storm is set to hit the Andhra\u2013Odisha coast on Friday with winds near 100 km/h.",
     icon_cyclone),
    ("CULTURE  •  GAMES", (120, 40, 160), "GTA VI LAUNCHES TODAY",
     "The decade's most awaited game arrives; doctors urge players to move every 30 minutes.",
     icon_game),
]

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# masthead
d.rectangle([0, 0, W, 166], fill=NAVY)
centered(d, W // 2, 22, "THE WORLD IN ONE PAGE", F_KICK, GOLD)
centered(d, W // 2, 52, "THURSDAY 19 NOVEMBER 2026", F_DATE, (255, 255, 255))
d.rectangle([W // 2 - 110, 126, W // 2 + 110, 130], fill=RED)
centered(d, W // 2, 138, "SIX STORIES THAT DEFINED THE DAY", F_SUBKICK,
         (201, 210, 224))

# grid
MARGIN, GAP = 26, 18
PW = (W - 2 * MARGIN - 2 * GAP) // 3
PH = 378
TOPS = (186, 584)
for i, (tag, color, head, sub, icon) in enumerate(PANELS):
    col, row = i % 3, i // 3
    px = MARGIN + col * (PW + GAP)
    py = TOPS[row]
    d.rectangle([px, py, px + PW, py + PH], fill=CARD, outline=BORDER, width=2)
    d.rectangle([px, py, px + PW, py + 8], fill=color)
    icon(d, px + 16, py + 20)
    ty = py + 172
    d.text((px + 16, ty), tag, font=F_TAG, fill=color)
    hy = ty + 26
    for line in wrap(d, head, F_HEAD, PW - 32):
        d.text((px + 16, hy), line, font=F_HEAD, fill=INK)
        hy += 33
    sy = hy + 6
    for line in wrap(d, sub, F_SUB, PW - 32):
        d.text((px + 16, sy), line, font=F_SUB, fill=SUBINK)
        sy += 23

# footer
d.line([(MARGIN, 980), (W - MARGIN, 980)], fill=BORDER, width=2)
centered(d, W // 2, 988,
         "Every story above happened, or was first reported, on Thursday 19 November 2026.",
         F_FOOT, FOOTINK)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
