import os
import sys
import numpy as np
from PIL import Image
from rembg import remove, new_session

HERE = os.path.dirname(os.path.abspath(__file__))
INP = "Собака.jpg"
OUT = "source-prepped-color.png"

# We don't even need rembg because it's a solid background!
# Let's just do a simple floodfill or color keying since it's pixel art.
im = Image.open(INP).convert("RGBA")
data = np.array(im)
bg_color = data[0, 0] # Top-left pixel is background

# Create mask where color matches bg_color (with some tolerance)
tolerance = 45
diff = np.abs(data[:, :, :3].astype(int) - bg_color[:3].astype(int))
mask = np.all(diff < tolerance, axis=-1)

# Set alpha to 0 for background
data[mask, 3] = 0

Image.fromarray(data).save(OUT)
print("Saved color prepped image to", OUT)
