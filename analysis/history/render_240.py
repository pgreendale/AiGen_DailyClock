from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
base=Path(__file__).resolve().parent
im=Image.open(base/"Ziffernblatt.png").convert("RGB")
a=np.asarray(im)
# Identify the coloured dial, excluding the colour legend below it.
colour=(a.max(axis=2).astype(int)-a.min(axis=2).astype(int)>35)
colour[int(im.height*.80):]=False
yy,xx=np.where(colour)
box=(int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1)
crop=im.crop(box)
if abs(crop.width-crop.height)>3: raise RuntimeError("Dial crop is not square")
dial=crop.resize((240,240),Image.Resampling.LANCZOS).convert("RGBA")
# Supersampled coverage mask gives a clean circular display boundary.
mask=Image.new("L",(240*4,240*4),0)
ImageDraw.Draw(mask).ellipse((0,0,240*4-1,240*4-1),fill=255)
mask=mask.resize((240,240),Image.Resampling.LANCZOS)
dial.putalpha(mask)
out=base/"Ziffernblatt_240x240.png"
dial.save(out)
check=Image.open(out)
assert check.size==(240,240) and check.mode=="RGBA"
print({"output":str(out),"size":check.size,"mode":check.mode,"source_crop":box})

