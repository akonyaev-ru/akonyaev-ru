import os
import html
from PIL import Image

RAMP = " .:-=+*#%@"

CHAR_W = 6
LINE_H = 10
ROWS = 40

def make_svg(src_path, out_path, flip=False):
    im = Image.open(src_path).convert("RGBA")
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        
    orig_w, orig_h = im.size
    cols = int((orig_w / orig_h) * ROWS * (LINE_H / CHAR_W))
    
    im = im.resize((cols, ROWS), Image.LANCZOS)
    px = im.load()
    im_l = im.convert("L")
    px_l = im_l.load()
    
    rows_markup = []
    for y in range(ROWS):
        markup = ""
        current_color = None
        current_text = ""
        
        for x in range(cols):
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
                        markup += f'<tspan fill="{current_color}">{html.escape(current_text)}</tspan>'
                current_text = char
                current_color = color
            else:
                current_text += char
                
        if current_text:
            if current_color is None:
                markup += " " * len(current_text)
            else:
                markup += f'<tspan fill="{current_color}">{html.escape(current_text)}</tspan>'
                
        rows_markup.append(markup)

    w = cols * CHAR_W
    h = ROWS * LINE_H
    
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        '<style>',
        '  :root {',
        '    --bg: transparent;',
        '  }',
        '</style>',
    ]
    
    y = LINE_H - 2
    for markup in rows_markup:
        # no animations, just static text
        parts.append(f'<text x="0" y="{y}" font-size="{LINE_H}" xml:space="preserve">{markup}</text>')
        y += LINE_H
        
    parts.append("</svg>")
    svg = "".join(parts)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {out_path} {w}x{h}")

HERE = os.path.dirname(os.path.abspath(__file__))
make_svg(os.path.join(HERE, "..", "Маг.png"), os.path.join(HERE, "..", "mage.svg"))
make_svg(os.path.join(HERE, "..", "Рыцарь.png"), os.path.join(HERE, "..", "knight.svg"), flip=True)
