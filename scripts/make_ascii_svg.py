import os
import sys
import html
from PIL import Image

SRC = "source-prepped-color.png"
OUT = "avi-ascii.svg"

COLS = 100
ROWS = 53
CELL_W = 8
CELL_H = 15
RAMP = " .`:-=+*cs#%@"  # bright(sparse) -> dark(dense)
WHITE_FLOOR = 0.80

PAD = 20
TITLEBAR_H = 30
STATUS_H = 30
ART_W = COLS * CELL_W
ART_H = ROWS * CELL_H
CANVAS_W = ART_W + PAD * 2
CANVAS_H = TITLEBAR_H + ART_H + STATUS_H + PAD

BG = "var(--bg)"
BG2 = "var(--bg2)"
FRAME = "var(--frame)"
TITLE_TEXT = "var(--title-text)"
INK = "var(--ink)"
CURSOR = "var(--cursor)"

ROW_DUR = 0.11
STAGGER = 0.11

im = Image.open(SRC).convert("RGBA")
im = im.resize((COLS, ROWS), Image.LANCZOS)
px = im.load()

# Pre-calculate luminance for character mapping
im_l = im.convert("L")
px_l = im_l.load()

STATIC = False

rows_markup = []
for y in range(ROWS):
    markup = ""
    current_color = None
    current_text = ""
    
    for x in range(COLS):
        r, g, b, a = px[x, y]
        if a < 128:
            color = None
            char = " "
        else:
            color = f"#{r:02x}{g:02x}{b:02x}"
            lum = px_l[x, y] / 255.0
            idx = int((1.0 - lum) * (len(RAMP) - 1) + 0.5)
            idx = max(0, min(len(RAMP) - 1, idx))
            char = RAMP[idx]
            
        if color != current_color:
            if current_text:
                if current_color is None:
                    markup += " " * len(current_text)
                else:
                    safe = html.escape(current_text)
                    markup += f'<tspan fill="{current_color}">{safe}</tspan>'
            current_color = color
            current_text = char
        else:
            current_text += char
            
    if current_text:
        if current_color is None:
            markup += " " * len(current_text)
        else:
            safe = html.escape(current_text)
            markup += f'<tspan fill="{current_color}">{safe}</tspan>'
            
    rows_markup.append(markup)

art_top = TITLEBAR_H + PAD * 0.35

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, '
    f'Menlo, Consolas, monospace">'
)
parts.append('''
<style>
  :root {
    --bg: #ffffff;
    --bg2: #f6f8fa;
    --frame: #d0d7de;
    --title-text: #57606a;
    --ink: #24292f;
    --cursor: #24292f;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #0d1117;
      --bg2: #111722;
      --frame: #30363d;
      --title-text: #7d8590;
      --ink: #c9d1d9;
      --cursor: #c9d1d9;
    }
  }
</style>
''')
parts.append('<defs>'
             f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
             f'</linearGradient></defs>')

parts.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg)"/>')
parts.append(f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" '
             f'fill="none" stroke="{FRAME}" stroke-width="1"/>')

parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
             f'text-anchor="middle">Paulina - Pride of the Empire</text>')

font_size = CELL_H * 0.86

parts.append('<g id="portrait-layer">')

for ry, markup in enumerate(rows_markup):
    y = art_top + ry * CELL_H + CELL_H * 0.74
    row_y = art_top + ry * CELL_H
    delay = ry * STAGGER
    
    text = (f'<text xml:space="preserve" x="{PAD}" y="{y:.1f}" '
            f'font-size="{font_size:.1f}">{markup}</text>')

    parts.append(
        f'<clipPath id="r{ry}"><rect x="{PAD}" y="{row_y:.1f}" height="{CELL_H}" width="0">'
        f'<animate attributeName="width" from="0" to="{ART_W}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/></rect></clipPath>'
    )
    parts.append(f'<g clip-path="url(#r{ry})">{text}</g>')
    parts.append(
        f'<rect y="{row_y+1:.1f}" width="{CELL_W}" height="{CELL_H-2}" fill="{CURSOR}" opacity="0">'
        f'<animate attributeName="x" from="{PAD}" to="{PAD+ART_W}" begin="{delay:.3f}s" '
        f'dur="{ROW_DUR:.2f}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0.85" begin="{delay:.3f}s"/>'
        f'<set attributeName="opacity" to="0" begin="{delay+ROW_DUR:.3f}s"/></rect>'
    )

parts.append('</g>')
parts.append('<g transform="translate(568, 247)">')
parts.append('<g>')
parts.append('<animateTransform attributeName="transform" type="scale" values="0; 0; 1; 0; 0" keyTimes="0; 0.78; 0.84; 0.90; 1" dur="10s" repeatCount="indefinite" />')
parts.append('<animateTransform attributeName="transform" type="rotate" values="0; 0; 90; 180; 180" keyTimes="0; 0.78; 0.84; 0.90; 1" dur="10s" repeatCount="indefinite" additive="sum" />')
parts.append('<path d="M0,-20 Q0,0 -20,0 Q0,0 0,20 Q0,0 20,0 Q0,0 0,-20 Z" fill="#fff">')
parts.append('<animate attributeName="opacity" values="0; 0; 1; 0; 0" keyTimes="0; 0.78; 0.84; 0.90; 1" dur="10s" repeatCount="indefinite" />')
parts.append('</path>')
parts.append('</g></g>')

status_line_y = TITLEBAR_H + ART_H + PAD * 0.35
status_y = status_line_y + 19
parts.append(f'<line x1="0" y1="{status_line_y:.1f}" x2="{CANVAS_W}" y2="{status_line_y:.1f}" stroke="{FRAME}"/>')
parts.append(f'<text x="{PAD}" y="{status_y:.1f}" fill="{TITLE_TEXT}" font-size="13">'
             f'Paulina - Pride of the Empire</text>')
parts.append(f'<rect x="{PAD+196}" y="{status_y-12:.1f}" width="8" height="14" fill="{INK}">'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
             f'dur="1s" repeatCount="indefinite"/></rect>')

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;")
