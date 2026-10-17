from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1]
out=root/"docs/previews"
out.mkdir(parents=True,exist_ok=True)
alpha=Image.open(root/"firmware/assets/clockface_240.png").getchannel("A")
for source in (root/"build-host").glob("preview_*.ppm"):
    im=Image.open(source).convert("RGBA")
    im.putalpha(alpha)
    im.save(out/(source.stem+".png"))
    print(out/(source.stem+".png"))

