"""Find installed Pico tools and save ignored local configuration."""
import argparse,json,os,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def find(patterns):
 hits=[p for pat in patterns for p in Path.home().glob(pat)]
 return str(sorted(hits,reverse=True)[0]) if hits else None
def require(value,label,folder=False):
 if not value:raise SystemExit(label+" fehlt. Expliziten Parameter angeben oder Pico-Extension-Werkzeuge installieren.")
 p=Path(value).expanduser().resolve()
 if not (p.is_dir() if folder else p.is_file()):raise SystemExit(label+": Pfad ungültig: "+str(p))
 return str(p)
def main():
 p=argparse.ArgumentParser(description=__doc__)
 for k in ("sdk","toolchain","cmake","ninja","tinyusb","picotool","pioasm"):p.add_argument("--"+k)
 p.add_argument("--rotation",type=int,choices=(0,180),default=180);a=p.parse_args()
 ext=".exe" if os.name=="nt" else ""
 sdk=a.sdk or os.getenv("PICO_SDK_PATH") or find([".pico-sdk/sdk/*/pico_sdk_init.cmake"])
 if not sdk:raise SystemExit("Pico SDK fehlt: --sdk PFAD angeben")
 sdk=Path(sdk)
 if sdk.name=="pico_sdk_init.cmake":sdk=sdk.parent
 sdk=Path(require(sdk,"SDK",True))
 if not (sdk/"pico_sdk_init.cmake").is_file():raise SystemExit("SDK enthält kein pico_sdk_init.cmake")
 arm=a.toolchain or os.getenv("PICO_TOOLCHAIN_PATH")
 if not arm:
  cc=shutil.which("arm-none-eabi-gcc") or find([".pico-sdk/toolchain/*/bin/arm-none-eabi-gcc"+ext])
  arm=str(Path(cc).parent.parent) if cc else None
 arm=require(arm,"Arm Toolchain",True)
 if not (Path(arm)/"bin"/("arm-none-eabi-gcc"+ext)).is_file():raise SystemExit("Toolchain muss bin/arm-none-eabi-gcc enthalten")
 c={"sdk":str(sdk),"toolchain":arm,"rotation":a.rotation}
 for key,patterns in [("cmake",[".pico-sdk/cmake/*/bin/cmake"+ext]),("ninja",[".pico-sdk/ninja/*/ninja"+ext,".pico-sdk/ninja/*/bin/ninja"+ext])]:
  c[key]=require(getattr(a,key) or shutil.which(key) or find(patterns),key)
 c["tinyusb"]=require(a.tinyusb or sdk/"lib/tinyusb","TinyUSB",True)
 if not (Path(c["tinyusb"])/"src/tusb.c").is_file():raise SystemExit("SDK-Submodule fehlen: git submodule update --init --recursive im SDK ausführen")
 for key,patterns in [("picotool",[".pico-sdk/picotool/*/picotool"]),("pioasm",[".pico-sdk/tools/*/pioasm"])]:
  value=getattr(a,key) or find(patterns)
  if value:c[key]=require(value,key,True)
 path=R/"cmake/local-tools.json";path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(c,indent=2)+"\n")
 print(json.dumps(c,indent=2));print("Weiter: python tools/build.py")
if __name__=="__main__":main()
