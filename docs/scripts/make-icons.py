#!/usr/bin/env python3
"""Génère les PNG du dossier icons/ (stdlib uniquement). Relancer depuis fx-lab-app/ :
    python3 scripts/make-icons.py
"""
import struct, zlib, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "icons")

def write_png(path, w, h, rgba):
    def chunk(tag, data):
        crc = zlib.crc32(tag + data) & 0xffffffff
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)
    raw = bytearray()
    stride = w * 4
    for y in range(h):
        raw.append(0)
        raw.extend(rgba[y*stride:(y+1)*stride])
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)

def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

def mix(dst, i, r, g, b, a):
    if a <= 0: return
    da = dst[i+3] / 255.0
    sa = a
    out_a = sa + da * (1 - sa)
    if out_a <= 0: return
    def ch(s, d):
        return int((s * sa + d * da * (1 - sa)) / out_a + 0.5)
    dst[i]   = clamp(ch(r, dst[i]), 0, 255)
    dst[i+1] = clamp(ch(g, dst[i+1]), 0, 255)
    dst[i+2] = clamp(ch(b, dst[i+2]), 0, 255)
    dst[i+3] = clamp(int(out_a * 255 + 0.5), 0, 255)

def fill(dst, w, h, r, g, b, a=1.0):
    aa = int(a * 255)
    for i in range(0, w*h*4, 4):
        dst[i] = r; dst[i+1] = g; dst[i+2] = b; dst[i+3] = aa

def aa_disk(dst, w, h, cx, cy, rad, col, feather=1.2):
    r, g, b, a = col
    r0 = max(0, int(cy - rad - 2)); r1 = min(h-1, int(cy + rad + 2))
    c0 = max(0, int(cx - rad - 2)); c1 = min(w-1, int(cx + rad + 2))
    for y in range(r0, r1+1):
        for x in range(c0, c1+1):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            cov = clamp((rad - d) / feather + 0.5, 0, 1)
            if cov: mix(dst, (y*w+x)*4, r, g, b, a * cov)

def aa_ring(dst, w, h, cx, cy, rad, thick, col, feather=1.2):
    r, g, b, a = col
    outer = rad + thick/2; inner = rad - thick/2
    r0 = max(0, int(cy - outer - 2)); r1 = min(h-1, int(cy + outer + 2))
    c0 = max(0, int(cx - outer - 2)); c1 = min(w-1, int(cx + outer + 2))
    for y in range(r0, r1+1):
        for x in range(c0, c1+1):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            cov = clamp((outer - d) / feather + 0.5, 0, 1) * clamp((d - inner) / feather + 0.5, 0, 1)
            if cov: mix(dst, (y*w+x)*4, r, g, b, a * cov)

def aa_roundrect(dst, w, h, x0, y0, x1, y1, rad, col, feather=1.2):
    r, g, b, a = col
    for y in range(max(0, int(y0-2)), min(h, int(y1+3))):
        for x in range(max(0, int(x0-2)), min(w, int(x1+3))):
            px, py = x + 0.5, y + 0.5
            cx = clamp(px, x0+rad, x1-rad)
            cy = clamp(py, y0+rad, y1-rad)
            if x0+rad <= px <= x1-rad and y0+rad <= py <= y1-rad:
                mix(dst, (y*w+x)*4, r, g, b, a); continue
            d = math.hypot(px - cx, py - cy)
            cov = clamp((rad - d) / feather + 0.5, 0, 1)
            if cov: mix(dst, (y*w+x)*4, r, g, b, a * cov)

def aa_rect(dst, w, h, x0, y0, x1, y1, col, feather=1.0):
    r, g, b, a = col
    for y in range(max(0, int(y0-2)), min(h, int(y1+3))):
        for x in range(max(0, int(x0-2)), min(w, int(x1+3))):
            px, py = x + 0.5, y + 0.5
            dx = max(x0 - px, 0, px - x1)
            dy = max(y0 - py, 0, py - y1)
            outside = math.hypot(dx, dy) if dx or dy else 0
            inside = min(px - x0, x1 - px, py - y0, y1 - py)
            sdf = outside - (0 if outside else inside)
            cov = clamp(0.5 - sdf / feather, 0, 1)
            if cov: mix(dst, (y*w+x)*4, r, g, b, a * cov)

def draw_icon(size, maskable=False):
    w = h = size
    dst = bytearray(w * h * 4)
    fill(dst, w, h, 0x0f, 0x14, 0x19, 1)
    s = size / 512.0
    pad = 72 * s if maskable else 28 * s
    aa_roundrect(dst, w, h, pad, pad, size-pad, size-pad, 96*s if not maskable else 140*s,
                 (0x1a, 0x23, 0x32, 1.0), feather=1.4*s)
    cx = cy = size / 2
    aa_disk(dst, w, h, cx, cy, 168*s, (0x0f, 0x14, 0x19, 1.0), feather=1.5*s)
    aa_ring(dst, w, h, cx, cy, 168*s, 18*s, (0x3b, 0x82, 0xf6, 1.0), feather=1.4*s)
    candles = [
        (-90, -10,  55, -40,  80, (0xef, 0x44, 0x44, 1.0)),
        (-18, -50,  30, -90,  55, (0x22, 0xc5, 0x5e, 1.0)),
        ( 54, -95,   5, -130, 40, (0x22, 0xc5, 0x5e, 1.0)),
    ]
    bw = 32 * s; ww = 5 * s
    for ox, blo, bhi, wlo, whi, col in candles:
        x = cx + ox * s
        aa_rect(dst, w, h, x - ww/2, cy + wlo*s, x + ww/2, cy + whi*s, (0xe8, 0xee, 0xf7, 0.95), feather=0.9*s)
        y0, y1 = cy + blo*s, cy + bhi*s
        if y0 > y1: y0, y1 = y1, y0
        aa_roundrect(dst, w, h, x - bw/2, y0, x + bw/2, y1, 5*s, col, feather=0.9*s)
    aa_disk(dst, w, h, cx + 118*s, cy - 118*s, 18*s, (0x3b, 0x82, 0xf6, 1.0), feather=1.2*s)
    aa_disk(dst, w, h, cx + 118*s, cy - 118*s, 8*s, (0xe8, 0xee, 0xf7, 1.0), feather=1.0*s)
    return dst

def main():
    os.makedirs(OUT, exist_ok=True)
    for size, name in [(192, "icon-192.png"), (512, "icon-512.png"), (180, "apple-touch-icon.png"), (32, "favicon-32.png")]:
        write_png(os.path.join(OUT, name), size, size, draw_icon(size, False))
    for size, name in [(192, "icon-maskable-192.png"), (512, "icon-maskable-512.png")]:
        write_png(os.path.join(OUT, name), size, size, draw_icon(size, True))
    print("icons written in", OUT)

if __name__ == "__main__":
    main()
