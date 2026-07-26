import os
import base64
import io
from PIL import Image

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

def remove_white_bg(img):
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    # Simple threshold for white background (e.g. > 240 on all RGB)
    # A better way is flood fill from corners, but let's see.
    # To avoid removing inner white, maybe we just use flood fill.
    # Actually, PIL ImageDraw floodfill is better.
    from PIL import ImageDraw
    ImageDraw.floodfill(img, (0, 0), (255, 255, 255, 0), thresh=15)
    ImageDraw.floodfill(img, (img.width-1, 0), (255, 255, 255, 0), thresh=15)
    ImageDraw.floodfill(img, (0, img.height-1), (255, 255, 255, 0), thresh=15)
    ImageDraw.floodfill(img, (img.width-1, img.height-1), (255, 255, 255, 0), thresh=15)
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
        print(f"File not found: {path}")
        continue
        
    try:
        img = Image.open(path)
        img = remove_white_bg(img)
        # Resize to 50x50 using LANCZOS
        img = img.resize((50, 50), Image.Resampling.LANCZOS)
        
        # Save to buffer
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        b64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        tag = f"""
  <g transform="translate({x_offset}, 0)">
    <!-- Shadow background -->
    <rect width="50" height="50" rx="12" fill="#fff" filter="url(#shadow)"/>
    <!-- Image clipped -->
    <image href="data:image/png;base64,{b64_str}" width="50" height="50" clip-path="url(#squircle)"/>
  </g>"""
        icon_tags.append(tag)
        x_offset += 60
    except Exception as e:
        print(f"Failed to process {filename}: {e}")

SVG_TEMPLATE += "".join(icon_tags) + "\n</svg>"

out_path = r"g:\Мой диск\Агенты\Разработчики\akonyaev-ru\ai-apps.svg"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(SVG_TEMPLATE)
    
print("Successfully generated ai-apps.svg with local images!")
