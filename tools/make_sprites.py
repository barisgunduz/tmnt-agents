#!/usr/bin/env python3
"""Generates every sprite of the tmnt-agents mod from code. No downloads, no external art.

Usage: python3 tools/make_sprites.py [--out DIR]
Writes <out>/sprites/<id>/{walkR,walkL,idleR,idleL,sleep}.gif, <out>/sprites/<id>/meta.json
and <out>/icons/<id>.png. Characters are drawn facing right on a 32x32 grid, mirrored for
left, then scaled 2x with nearest neighbour.
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

N = 32
SCALE = 2
DEFAULT_OUT = Path(__file__).resolve().parent.parent / "mods" / "tmnt-agents"
OUT = DEFAULT_OUT  # set from the command line in the entry point

K = (20, 20, 24, 255)        # outline / pupil
WHITE = (245, 245, 245, 255)
GREEN = (96, 170, 70, 255)
GREEN_D = (62, 125, 52, 255)
PLASTRON = (222, 205, 140, 255)
SHELL = (130, 88, 48, 255)
SHELL_D = (96, 62, 34, 255)
BELT = (150, 100, 40, 255)
STEEL = (200, 205, 215, 255)
WOOD = (150, 105, 60, 255)

TURTLES = {
    "leonardo": {"name": "Leonardo", "band": (40, 110, 220, 255), "weapon": "katana"},
    "raphael": {"name": "Raphael", "band": (215, 40, 40, 255), "weapon": "sai"},
    "donatello": {"name": "Donatello", "band": (140, 70, 190, 255), "weapon": "bo"},
    "michelangelo": {"name": "Michelangelo", "band": (240, 140, 30, 255), "weapon": "nunchaku"},
}
ORDER = ["leonardo", "raphael", "donatello", "michelangelo", "splinter"]
NAMES = {**{k: v["name"] for k, v in TURTLES.items()}, "splinter": "Splinter"}

FUR = (150, 108, 72, 255)
FUR_D = (112, 78, 50, 255)
FUR_L = (214, 180, 140, 255)
ROBE = (120, 62, 52, 255)
ROBE_D = (88, 44, 38, 255)
PINK = (230, 140, 150, 255)


def rect(d, x0, y0, x1, y1, c):
    d.rectangle([x0, y0, x1, y1], fill=c)


def new():
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


# ---- turtles ---------------------------------------------------------------------------

def weapon_back(d, kind):
    if kind == "katana":
        # strapped diagonally behind the shell: grip up by the shoulder, thin blade running down the back
        d.line([(10, 7), (3, 25)], fill=STEEL, width=1)
        d.line([(12, 1), (10, 6)], fill=K, width=2)
        rect(d, 8, 6, 12, 6, BELT)
    if kind == "bo":
        d.line([(6, 29), (19, 1)], fill=WOOD, width=2)
        d.line([(7, 29), (20, 1)], fill=SHELL_D, width=1)


def weapon_over_shell(d, kind, by):
    return  # katana is drawn behind the body, see weapon_back


def weapon_hand(d, kind):
    if kind == "sai":
        d.line([(22, 18), (28, 11)], fill=STEEL, width=2)
        d.line([(24, 10), (29, 15)], fill=STEEL, width=2)
        d.line([(26, 9), (27, 9)], fill=WHITE)
        rect(d, 21, 17, 23, 19, K)
    elif kind == "nunchaku":
        d.line([(22, 17), (25, 10)], fill=WOOD, width=2)
        d.line([(26, 10), (28, 15)], fill=K)
        d.line([(28, 15), (29, 21)], fill=WOOD, width=2)
    elif kind in ("katana", "bo"):
        rect(d, 21, 16, 22, 18, K)


def turtle_stand(t, legs, bob):
    im, d = new()
    weapon_back(d, t["weapon"])
    by = bob
    # back leg
    bx, bl = legs[0]
    rect(d, 11 + bx, 22 + by, 13 + bx, 29 - bl, GREEN_D)
    rect(d, 11 + bx, 29 - bl, 14 + bx, 29 - bl, K)
    # shell and torso
    rect(d, 7, 12 + by, 14, 23 + by, SHELL)
    rect(d, 7, 12 + by, 8, 23 + by, SHELL_D)
    rect(d, 10, 14 + by, 12, 21 + by, SHELL_D)
    rect(d, 12, 13 + by, 19, 22 + by, GREEN)
    rect(d, 16, 13 + by, 19, 21 + by, PLASTRON)
    rect(d, 12, 21 + by, 19, 22 + by, BELT)
    weapon_over_shell(d, t["weapon"], by)
    # front leg
    fx, fl = legs[1]
    rect(d, 16 + fx, 22 + by, 18 + fx, 29 - fl, GREEN)
    rect(d, 16 + fx, 29 - fl, 20 + fx, 29 - fl, K)
    # head
    rect(d, 14, 4 + by, 23, 12 + by, GREEN)
    rect(d, 14, 4 + by, 23, 4 + by, GREEN_D)
    rect(d, 14, 6 + by, 23, 8 + by, t["band"])
    rect(d, 19, 6 + by, 22, 7 + by, WHITE)
    d.point((22, 7 + by), fill=K)
    rect(d, 20, 11 + by, 22, 11 + by, K)
    # bandana tails
    d.line([(14, 7 + by), (9, 9 + by)], fill=t["band"])
    d.line([(14, 8 + by), (10, 11 + by)], fill=t["band"])
    # arm
    rect(d, 18, 14 + by, 21, 17 + by, GREEN)
    rect(d, 21, 16 + by, 22, 18 + by, GREEN_D)
    weapon_hand(d, t["weapon"])
    return im


def turtle_sleep(t, f):
    im, d = new()
    b = f
    rect(d, 6, 15 + b, 19, 24, SHELL)
    rect(d, 6, 15 + b, 19, 16 + b, SHELL_D)
    rect(d, 9, 18 + b, 16, 22, SHELL_D)
    rect(d, 5, 24, 22, 29, GREEN)
    rect(d, 14, 24, 22, 26, PLASTRON)
    rect(d, 5, 29, 22, 29, GREEN_D)
    # head resting on the front, bigger and higher
    rect(d, 20, 17 + b, 30, 29, GREEN)
    rect(d, 20, 17 + b, 30, 17 + b, GREEN_D)
    rect(d, 20, 20 + b, 30, 22 + b, t["band"])
    rect(d, 25, 20 + b, 29, 21 + b, WHITE)
    rect(d, 25, 21 + b, 29, 21 + b, K)  # closed eye
    rect(d, 26, 26, 29, 26, K)           # sleepy mouth
    d.line([(20, 20 + b), (15, 22 + b)], fill=t["band"], width=2)
    d.line([(20, 22 + b), (16, 26)], fill=t["band"], width=1)
    return im


# ---- splinter ----------------------------------------------------------------------------

def splinter_stand(legs, bob, sway):
    im, d = new()
    by = bob
    # tail
    d.line([(8, 24), (4, 22), (3, 18)], fill=PINK)
    # feet
    rect(d, 12 + legs[0][0], 27, 15 + legs[0][0], 29 - legs[0][1], K)
    rect(d, 17 + legs[1][0], 27, 20 + legs[1][0], 29 - legs[1][1], K)
    # robe
    rect(d, 10, 14 + by, 20, 27, ROBE)
    rect(d, 10, 25, 20 + sway, 27, ROBE_D)
    rect(d, 10, 14 + by, 12, 27, ROBE_D)
    rect(d, 10, 19 + by, 20, 19 + by, BELT)
    # head
    rect(d, 14, 5 + by, 22, 13 + by, FUR)
    rect(d, 21, 8 + by, 26, 12 + by, FUR_L)
    rect(d, 26, 9 + by, 27, 10 + by, PINK)
    rect(d, 14, 4 + by, 16, 6 + by, FUR_D)  # ear
    rect(d, 17, 3 + by, 19, 5 + by, FUR_D)
    rect(d, 20, 7 + by, 21, 8 + by, WHITE)
    d.point((21, 8 + by), fill=K)
    d.line([(22, 11 + by), (26, 13 + by)], fill=WHITE)  # whisker
    # beard
    rect(d, 17, 13 + by, 21, 15 + by, FUR_L)
    # arm and hand
    rect(d, 17, 15 + by, 21, 18 + by, ROBE_D)
    rect(d, 21, 17 + by, 22, 19 + by, FUR)
    # walking cane held in front, crook above the hand, tip on the ground
    d.line([(23, 15 + by), (23, 29)], fill=WOOD, width=2)
    d.line([(22, 14 + by), (25, 14 + by)], fill=WOOD, width=1)
    d.point((25, 15 + by), fill=WOOD)
    rect(d, 21, 17 + by, 23, 19 + by, FUR)
    return im


def splinter_sleep(f):
    im, d = new()
    b = f
    d.line([(7, 30), (5, 26), (3, 22)], fill=PINK)
    rect(d, 6, 20 + b, 22, 29, ROBE)
    rect(d, 6, 20 + b, 22, 21 + b, ROBE_D)
    rect(d, 6, 29, 22, 29, ROBE_D)
    rect(d, 21, 21, 29, 29, FUR)
    rect(d, 26, 25, 31, 29, FUR_L)
    rect(d, 31, 26, 31, 27, PINK)
    rect(d, 22, 18, 24, 21, FUR_D)  # ear
    rect(d, 26, 23, 27, 23, K)
    rect(d, 22, 26, 25, 29, FUR_L)
    return im


# ---- animation sets ----------------------------------------------------------------------

WALK_LEGS = [((-2, 0), (2, 0)), ((0, 1), (0, 0)), ((2, 0), (-2, 0)), ((0, 0), (0, 1))]
WALK_BOB = [0, 1, 0, 1]


def frames(cid):
    t = TURTLES.get(cid)
    if t:
        walk = [turtle_stand(t, WALK_LEGS[i], WALK_BOB[i]) for i in range(4)]
        idle = [turtle_stand(t, ((0, 0), (0, 0)), b) for b in (0, 0, 1, 0)]
        sleep = [turtle_sleep(t, 0), turtle_sleep(t, 1)]
    else:
        walk = [splinter_stand(WALK_LEGS[i], WALK_BOB[i], [-1, 0, 1, 0][i]) for i in range(4)]
        idle = [splinter_stand(((0, 0), (0, 0)), b, 0) for b in (0, 0, 1, 0)]
        sleep = [splinter_sleep(0), splinter_sleep(1)]
    return {"walk": walk, "idle": idle, "sleep": sleep}


def scaled(im):
    return im.resize((N * SCALE, N * SCALE), Image.NEAREST)


def save_gif(path, ims, delay_ms):
    path.parent.mkdir(parents=True, exist_ok=True)
    ims = [scaled(i) for i in ims]
    ims[0].save(path, save_all=True, append_images=ims[1:], duration=delay_ms, loop=0,
                disposal=2, transparency=0, optimize=False)


def union_box(ims):
    box = None
    for im in ims:
        b = scaled(im).getchannel("A").getbbox()
        if b:
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    return box or (0, 0, N * SCALE, N * SCALE)


def build(cid):
    f = frames(cid)
    mirror = lambda ims: [ImageOps.mirror(i) for i in ims]
    sets = {
        "walkR": (f["walk"], 130),
        "walkL": (mirror(f["walk"]), 130),
        "idleR": (f["idle"], 420),
        "idleL": (mirror(f["idle"]), 420),
        "sleep": (f["sleep"], 800),
    }
    d = OUT / "sprites" / cid
    meta = {"version": 1, "id": cid, "name": NAMES[cid], "scale": SCALE}
    for key, (ims, delay) in sets.items():
        save_gif(d / f"{key}.gif", ims, delay)
        x0, y0, x1, y1 = union_box(ims)
        meta[key] = {"path": f"sprites/{cid}/{key}.gif", "w": N * SCALE, "h": N * SCALE,
                     "box": {"x": x0, "y": y0, "w": x1 - x0, "h": y1 - y0}}
    (d / "meta.json").write_text(json.dumps(meta), encoding="utf-8")
    # picker icon: the head close-up, 40x30 doubled to 80x60
    box = (8, 0, 28, 15) if cid == "splinter" else (6, 0, 26, 15)  # Splinter's snout sits further right
    head = f["idle"][0].crop(box).resize((80, 60), Image.NEAREST)
    (OUT / "icons").mkdir(parents=True, exist_ok=True)
    head.save(OUT / "icons" / f"{cid}.png")
    return f


def pizza():
    """A 16x16 pizza slice, crust on top, tip pointing down."""
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    crust, crust_d = (226, 160, 70, 255), (176, 106, 40, 255)
    cheese, edge = (250, 208, 76, 255), (222, 168, 40, 255)
    for y in range(4, 15):
        inset = round((y - 3) * 0.55)
        rect(d, 1 + inset, y, 14 - inset, y, cheese)
        d.point((1 + inset, y), fill=edge)
        d.point((14 - inset, y), fill=edge)
    rect(d, 1, 1, 14, 3, crust)
    rect(d, 1, 3, 14, 3, crust_d)
    for x, y in ((5, 6), (9, 7), (7, 10)):
        rect(d, x, y, x + 1, y + 1, (200, 50, 40, 255))
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pizza().resize((16 * SCALE * 2, 16 * SCALE * 2), Image.NEAREST).save(OUT / "pizza.png")
    sheet = Image.new("RGBA", (len(ORDER) * 70, 5 * 70), (36, 38, 46, 255))
    for ci, cid in enumerate(ORDER):
        f = build(cid)
        rows = [f["walk"][0], f["walk"][2], f["idle"][0], ImageOps.mirror(f["idle"][0]), f["sleep"][0]]
        for ri, im in enumerate(rows):
            sheet.alpha_composite(scaled(im), (ci * 70 + 3, ri * 70 + 3))
    prev = OUT.parent.parent / "preview.png"
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(prev)
    print("ok", OUT, prev)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the tmnt-agents sprites.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="mod folder to write into")
    OUT = parser.parse_args().out
    main()
