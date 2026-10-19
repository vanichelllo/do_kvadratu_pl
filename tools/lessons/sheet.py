"""Контактний аркуш: python3 sheet.py <папка> <тег> <вихід.png> [масштаб] — усі слайди тегу в сітці 3×N."""
import sys, glob, re
from PIL import Image
d, tag, out = sys.argv[1:4]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
files = sorted(glob.glob(f'{d}/{tag}-*.png'), key=lambda f: int(re.search(r'-(\d+)\.png$', f).group(1)))
ims = [Image.open(f) for f in files]
w, h = int(ims[0].width * scale), int(ims[0].height * scale)
cols = 3; rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (w * cols, h * rows), 'white')
for i, im in enumerate(ims): sheet.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
sheet.save(out); print(out, sheet.size)
