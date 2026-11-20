#!/usr/bin/env python3
"""Render the morning-edition broadsheet for 20 Nov 2026.
Build-time only: uses PIL + local fonts. The submitted program (main.py)
only copies the pre-rendered entry.png, so no fonts are needed at run time.
Layout is computed with a running y cursor; nothing may pass y=996.
"""
from PIL import Image, ImageDraw, ImageFont
import random

W = H = 1024
CREAM = (245, 238, 221)
NAVY = (27, 42, 74)
NAVY_SOFT = (52, 68, 104)
RED = (166, 58, 46)
GOLD = (176, 141, 74)
INK = (32, 32, 30)
GREY = (110, 104, 90)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.32)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y

def headline(draw, x, y, text, fnt, width, fill=NAVY, leading=None, align="left"):
    if leading is None:
        leading = int(fnt.size * 1.12)
    for line in wrap(draw, text, fnt, width):
        if align == "center":
            draw.text((x + (width - draw.textlength(line, font=fnt)) / 2, y),
                      line, font=fnt, fill=fill)
        else:
            draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y

def rule(draw, x0, x1, y, fill=NAVY, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)

def draw_capitol(d, x, y, w, h):
    cx = x + w // 2
    base = y + h - 6
    # dome
    d.pieslice([cx - 46, y + 8, cx + 46, y + 84], 180, 360, outline=NAVY, width=3)
    d.line([(cx - 46, y + 46), (cx + 46, y + 46)], fill=NAVY, width=2)
    d.rectangle([cx - 5, y + 2, cx + 5, y + 12], fill=NAVY)
    d.line([(cx, y + 2), (cx, y - 8)], fill=NAVY, width=2)
    # columns
    for i in range(5):
        colx = x + 26 + i * ((w - 52) // 4)
        d.line([(colx, base - 34), (colx, base - 4)], fill=NAVY, width=3)
    d.rectangle([x + 10, base - 38, x + w - 10, base - 34], outline=NAVY, width=2)
    d.rectangle([x + 6, base - 4, x + w - 6, base], fill=NAVY)
    # small flag
    d.line([(x + w - 18, base - 62), (x + w - 18, base - 38)], fill=NAVY, width=2)
    d.polygon([(x + w - 18, base - 62), (x + w - 2, base - 57),
               (x + w - 18, base - 52)], fill=RED)

def draw_scales(d, x, y, w, h):
    cx = x + w // 2
    top = y + 4
    d.line([(cx, top), (cx, y + h - 10)], fill=NAVY, width=3)
    d.line([(x + 70, top + 12), (x + w - 70, top + 12)], fill=NAVY, width=3)
    d.ellipse([cx - 4, top - 5, cx + 4, top + 3], fill=NAVY)
    for side in (-1, 1):
        px = cx + side * (w // 2 - 82)
        d.line([(px, top + 12), (px - 24, y + h - 30)], fill=NAVY, width=2)
        d.line([(px, top + 12), (px + 24, y + h - 30)], fill=NAVY, width=2)
        d.arc([px - 26, y + h - 34, px + 26, y + h - 2], 0, 180, fill=NAVY, width=3)
    d.rectangle([x + 10, y + h - 10, x + w - 10, y + h - 6], fill=NAVY)

def draw_globe(d, x, y, w, h):
    cx, cy, r = x + w // 2, y + h // 2 + 4, min(w, h) // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=NAVY, width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=NAVY, width=2)
    for i, col in enumerate((RED, NAVY, GOLD)):
        fx = cx - 40 + i * 40
        d.line([(fx, cy - r - 16), (fx, cy - r - 2)], fill=NAVY, width=2)
        d.polygon([(fx, cy - r - 16), (fx + 22, cy - r - 11), (fx, cy - r - 6)],
                  fill=col, outline=NAVY)

def draw_voyager(d, x, y, w, h):
    rng = random.Random(20261120)
    for _ in range(40):
        sx, sy = x + rng.randint(4, w - 4), y + rng.randint(4, h - 4)
        r = rng.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=NAVY)
    cx, cy = x + w // 2, y + h // 2 + 4
    d.line([(cx - 52, cy + 28), (cx + 52, cy - 22)], fill=NAVY, width=3)
    d.polygon([(cx - 4, cy - 28), (cx + 22, cy - 4), (cx - 2, cy + 2)],
              outline=NAVY, fill=GOLD)
    d.ellipse([cx - 30, cy - 34, cx + 2, cy - 2], outline=NAVY, width=3)
    d.line([(cx + 36, cy - 12), (cx + 58, cy - 26)], fill=NAVY, width=2)
    d.ellipse([cx + 54, cy - 30, cx + 64, cy - 20], fill=RED)

def draw_cyclone(d, x, y, w, h):
    cx, cy = x + w // 2, y + h // 2
    for k, r in enumerate(range(10, min(w, h) // 2, 11)):
        start = k * 60
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 230,
              fill=NAVY if k % 2 == 0 else NAVY_SOFT, width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)

def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=NAVY, width=3)
    d.rectangle([20, 20, W - 21, H - 21], outline=NAVY, width=1)

    # ---- Masthead ----
    y = 30
    d.text((W // 2, y), "THE WORLD TODAY", font=font(SERIF_B, 58),
           fill=NAVY, anchor="ma")
    y = 100
    rule(d, 40, W - 40, y, width=2)
    y = 108
    d.text((W // 2, y), "FRIDAY, 20 NOVEMBER 2026  •  MORNING EDITION  •  ONE PAGE, THE WHOLE PLANET",
           font=font(SANS_B, 15), fill=NAVY_SOFT, anchor="ma")
    y = 130
    rule(d, 40, W - 40, y, width=2)

    # ---- Breaking banner ----
    y = 140
    d.rectangle([40, y, W - 40, y + 28], fill=RED)
    d.text((W // 2, y + 14), "BREAKING NEWS  —  WASHINGTON",
           font=font(SANS_B, 16), fill=CREAM, anchor="mm")
    y += 28

    # ---- Lead story ----
    y += 10
    y = headline(d, 40, y, "TRUMP PUSHES IRAN WAR DECISION TO 2027",
                 font(SERIF_B, 36), W - 80, align="center")
    y += 2
    d.text((W // 2, y), "Senate rejects war-powers curb, 51–48, as president says: “see what happens after Jan 1”",
           font=font(SERIF, 17), fill=NAVY_SOFT, anchor="ma")
    y += 26
    draw_capitol(d, 44, y, 210, 96)
    lead = ("President Donald Trump has pushed any decision on war with Iran into 2027, "
            "saying he will “see what happens after Jan 1”, as the US Senate rejected a "
            "war-powers resolution that would have barred strikes without Congress. "
            "The measure failed 51–48 on Thursday, with three Republicans voting in "
            "favour and one Democrat against. The vote leaves the White House free to "
            "act — but, for now, the president says he is waiting.")
    y = para(d, 274, y, lead, font(SERIF, 16), W - 40 - 274)
    y += 8
    rule(d, 40, W - 40, y, width=2)

    col_w = (W - 80 - 24) // 2

    def story(x, y, head, kicker, body, draw_fn):
        yy = headline(d, x, y, head, font(SERIF_B, 22), col_w)
        yy += 3
        d.text((x, yy), kicker, font=font(SANS_B, 12), fill=RED)
        yy += 18
        yy = para(d, x, yy, body, font(SERIF, 15), col_w, leading=18)
        yy += 4
        draw_fn(d, x, yy, col_w, 44)
        return yy + 44

    # ---- Row 2 ----
    y += 12
    y0 = y
    end_l = story(40, y0, "ICJ: MYANMAR COMMITTED GENOCIDE",
                  "THE HAGUE — 9–6 RULING, THURSDAY",
                  "The International Court of Justice ruled that Myanmar committed "
                  "genocide against the Rohingya in northern Rakhine state, holding the "
                  "state itself responsible. The court ordered restitution for victims "
                  "and further investigations into the campaign.", draw_scales)
    end_r = story(40 + col_w + 24, y0, "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
                  "APEC SUMMIT — FIRST TRILATERAL, THURSDAY",
                  "The three leaders held their first trilateral meeting, discussing "
                  "nuclear arms, Iran and the war in Ukraine. APEC adopted the Shenzhen "
                  "Outlook on trade, data and AI — and Mr Trump warned that strict AI "
                  "regulation would stifle development.", draw_globe)
    y = max(end_l, end_r) + 8
    rule(d, 40, W - 40, y, width=2)

    # ---- Row 3 ----
    y += 12
    y0 = y
    end_l = story(40, y0, "VOYAGER 1 CROSSES ONE LIGHT-DAY",
                  "NASA CONFIRMS — FRIDAY",
                  "NASA confirmed that Voyager 1, launched in 1977, has now travelled "
                  "one light-day from Earth — about 26 billion kilometres — and is still "
                  "sending data home, the most distant human-made object ever.",
                  draw_voyager)
    end_r = story(40 + col_w + 24, y0, "CYCLONE AKVAN BEARS DOWN ON ODISHA",
                  "INDIA — EVACUATIONS UNDER WAY, FRIDAY",
                  "Cyclone Akvan neared India's Odisha coast on Friday, with mass "
                  "evacuations under way and schools closed across the state. Officials "
                  "said about 300,000 people had been moved to shelters as the storm "
                  "approached land.", draw_cyclone)
    y = max(end_l, end_r) + 8
    rule(d, 40, W - 40, y, width=2)

    # ---- Also today strip ----
    y += 10
    d.text((40, y), "ALSO TODAY", font=font(SANS_B, 17), fill=NAVY)
    d.text((W - 40, y), "FRIDAY 20 NOVEMBER 2026", font=font(SANS_B, 12),
           fill=GREY, anchor="ra")
    y += 26
    items = [
        "Anthropic IPO: $81.3bn raised at $83 a share; shares up 17%+ on debut.",
        "GTA VI sales have already passed The Odyssey’s $1.80bn global run.",
        "Kyiv hit by four ballistic missiles, officials said.",
        "Houthis claim drone and missile strikes on four Saudi targets.",
        "Tanker catches fire after hitting a mine east of the Strait of Hormuz.",
        "Europe ready for talks with Russia on ending the Ukraine war.",
        "South Korea’s annual exports top $1 trillion for the first time.",
    ]
    f = font(SANS, 14)
    half = (len(items) + 1) // 2
    left_items, right_items = items[:half], items[half:]
    yy = y
    for it in left_items:
        yy = para(d, 52, yy, "•  " + it, f, col_w - 12, leading=18)
    yy2 = y
    for it in right_items:
        yy2 = para(d, 52 + col_w + 24, yy2, "•  " + it, f, col_w - 12, leading=18)
    y = max(yy, yy2)
    print("final y:", y, "(limit 996)")
    assert y <= 996, f"layout overflow: {y}"
    img.save("entry.png", optimize=True)
    print("saved entry.png")

if __name__ == "__main__":
    main()
