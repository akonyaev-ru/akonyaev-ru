import sys
from PIL import Image
import base64
from io import BytesIO

def process_image(input_path):
    img = Image.open(input_path).convert("RGBA")
    data = img.getdata()
    
    new_data = []
    for item in data:
        # If pixel is near white, make it transparent
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0))
        else:
            # Make the logo pure white while preserving alpha
            new_data.append((255, 255, 255, item[3]))
            
    img.putdata(new_data)
    
    # Crop to bounding box of non-transparent pixels
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    # Resize to a reasonable size for a badge
    aspect = img.width / img.height
    new_h = 32
    new_w = int(new_h * aspect)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    
    # Save to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    print(img_str)

if __name__ == "__main__":
    process_image(sys.argv[1])
