
from PIL import Image
import os

image_path = "/Users/doric/.gemini/antigravity/brain/e179bce3-b9c9-44c5-a608-55caf67bb333/generated_diagram.png"

if os.path.exists(image_path):
    img = Image.open(image_path)
    # Calculate new height to maintain aspect ratio
    base_width = 400
    w_percent = (base_width / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    
    img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)
    img.save(image_path)
    print(f"Resized image to {base_width}x{h_size}")
else:
    print("Image not found")
