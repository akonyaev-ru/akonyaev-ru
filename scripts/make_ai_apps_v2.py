import os
import base64
import io
from PIL import Image, ImageChops, ImageDraw

image_files = [
    "Antigravity.webp",
    "NotebookLM.png",
    "ChaatGPT.png",
    "Claude.webp",
    "Cursor.jpg",
    "Obsidian.png",
    "n8n.png"
]

src_dir = r"g:\Мой диск\Агенты\Разработчики"
dest_dir = r"g:\Мой диск\Агенты\Разработчики\akonyaev-ru\assets"
os.makedirs(dest_dir, exist_ok=True)

def crop_to_icon(img):
    img = img.convert("RGBA")
    data = img.getdata()
    width, height = img.size
    
    min_x, min_y, max_x, max_y = width, height, -1, -1
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = data[y * width + x]
            if a < 128:
                continue
            if r > 245 and g > 245 and b > 245:
                continue
            if x < min_x: min_x = x
            if x > max_x: max_x = x
            if y < min_y: min_y = y
            if y > max_y: max_y = y
            
    if min_x <= max_x and min_y <= max_y:
        return img.crop((min_x, min_y, max_x+1, max_y+1))
    return img

svg_width = len(image_files) * 50 + (len(image_files) - 1) * 10
SVG_TEMPLATE = f"""<svg width="{svg_width}" height="50" viewBox="0 0 {svg_width} 50" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <clipPath id="squircle">
      <rect width="50" height="50" rx="12"/>
    </clipPath>
    <filter id="shadow" x="-4" y="-2" width="56" height="56" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity="0.15" />
    </filter>
  </defs>
"""

icon_tags = []
x_offset = 0

for filename in image_files:
    path = os.path.join(src_dir, filename)
    if not os.path.exists(path):
        continue
        
    try:
        img = Image.open(path)
        img = crop_to_icon(img)
        
        # Inset by 1.5% to remove any white anti-aliasing artifacts on the edges
        w, h = img.size
        inset_x = int(w * 0.015)
        inset_y = int(h * 0.015)
        img = img.crop((inset_x, inset_y, w - inset_x, h - inset_y))
        
        img = img.convert('RGBA')
        img = img.resize((50, 50), Image.Resampling.LANCZOS)
        
        # Floodfill white from corners
        ImageDraw.floodfill(img, (0, 0), (255, 255, 255, 0), thresh=20)
        ImageDraw.floodfill(img, (49, 0), (255, 255, 255, 0), thresh=20)
        ImageDraw.floodfill(img, (0, 49), (255, 255, 255, 0), thresh=20)
        ImageDraw.floodfill(img, (49, 49), (255, 255, 255, 0), thresh=20)
        
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        b64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        tag = f"""
  <g transform="translate({x_offset}, 0)">
    <image href="data:image/png;base64,{b64_str}" width="50" height="50" clip-path="url(#squircle)" filter="url(#shadow)"/>
  </g>"""
        icon_tags.append(tag)
        x_offset += 60
    except Exception as e:
        print(f"Failed {filename}: {e}")

SVG_TEMPLATE += "".join(icon_tags) + "\n</svg>"

out_path = r"g:\Мой диск\Агенты\Разработчики\akonyaev-ru\ai-apps.svg"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(SVG_TEMPLATE)
