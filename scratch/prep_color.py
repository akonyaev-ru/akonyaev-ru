import os
import sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
INP = "Собака.jpg"
OUT = "source-prepped-color.png"

im = Image.open(INP).convert("RGBA")
data = np.array(im)

# Flood fill from (0,0) to remove background without touching dark interior pixels like eyes/nose
h, w = data.shape[:2]
visited = np.zeros((h, w), dtype=bool)
bg_color = data[0, 0, :3].astype(int)
tolerance = 30

queue = [(0, 0)]
visited[0, 0] = True

while queue:
    x, y = queue.pop(0)
    data[y, x, 3] = 0 # set alpha to 0
    
    # check neighbors
    for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx]:
            diff = np.abs(data[ny, nx, :3].astype(int) - bg_color)
            if np.all(diff < tolerance):
                visited[ny, nx] = True
                queue.append((nx, ny))

Image.fromarray(data).save(OUT)
print("Saved color prepped image to", OUT)
