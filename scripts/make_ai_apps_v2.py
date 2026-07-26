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
    "n8n.png"
]

src_dir = r"g:\Мой диск\Агенты\Разработчики"
dest_dir = r"g:\Мой диск\Агенты\Разработчики\akonyaev-ru\assets"
os.makedirs(dest_dir, exist_ok=True)

def crop_to_non_white(img):
    rgb = img.convert('RGB')
    bg = Image.new('RGB', rgb.size, (255, 255, 255))
    diff = ImageChops.difference(rgb, bg)
    bbox = diff.getbbox()
    if bbox:
        return img.crop(bbox)
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
        img = crop_to_non_white(img)
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
