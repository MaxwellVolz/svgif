import logging
import os
import numpy as np
from PIL import Image
import svgwrite

# Constants
INPUT_FILE = "./images/blown.gif"
OUTPUT_DIR = "output"
FPS = 60
TWEEN_FRAME_INTERVAL = 5  # Every 5th frame as key frame

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize directories
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Read and process frames
frames = []
with Image.open(INPUT_FILE) as im:
    logging.info("Reading and processing frames.")
    for i in range(im.n_frames):
        im.seek(i)
        frame = im.convert("RGB")
        frames.append(frame)
    logging.info(f"Processed {len(frames)} frames.")

# Select key frames
key_frames = frames[0::TWEEN_FRAME_INTERVAL]

# Generate SVG output
logging.info("Starting SVG generation.")
dwg = svgwrite.Drawing(os.path.join(OUTPUT_DIR, "animated_svg.svg"), profile="tiny")

# Generate CSS for keyframes
css_text = "@keyframes anim-{ \n"
total_frames = len(key_frames)
frame_duration = 100 / total_frames  # Percentage of total animation time for one frame

for i, frame in enumerate(key_frames):
    css_text += f"  {i * frame_duration}% {{ opacity: 1; }}\n"

css_text += "}\n"
dwg.defs.add(dwg.style(css_text))

# Add frames to SVG
for i, img in enumerate(key_frames):
    group = dwg.g(
        id=f"frame_{i}",
        style=f"opacity:0;animation:anim- {total_frames / FPS}s linear infinite;",
    )
    png_data = img.tobytes("raw")
    encoded = base64.b64encode(png_data).decode()
    img_uri = f"data:image/png;base64,{encoded}"
    group.add(dwg.image(href=img_uri, insert=(0, 0)))
    dwg.add(group)

dwg.save()
logging.info("SVG generation completed and saved.")
