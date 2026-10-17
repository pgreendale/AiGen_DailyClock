"""Build RP2040 firmware using the installed, configured Pico SDK."""
import argparse,json,subprocess,shutil
from pathlib import Path
import os
R=Path(os.path.abspath(__file__)).parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument("--jobs",type=int,default=6);a=p.parse_args()
 path=R/"cmake/local-tools.json"
 if not path.is_file():raise SystemExit("Zuerst python tools/configure.py ausführen.")
 c=json.loads(path.read_text());out=R/"build/rp2040"
 opts=["-S",str(R),"-B",str(out),"-G","Ninja","-DCMAKE_BUILD_TYPE=Release","-DCMAKE_POLICY_VERSION_MINIMUM=3.5","-DPICO_BOARD=pico","-DPICO_PLATFORM=rp2040","-DCLOCK_LCD_ROTATION="+str(c["rotation"])]
 for k,v in [("sdk","PICO_SDK_PATH"),("toolchain","PICO_TOOLCHAIN_PATH"),("tinyusb","PICO_TINYUSB_PATH"),("ninja","CMAKE_MAKE_PROGRAM"),("picotool","picotool_DIR"),("pioasm","pioasm_DIR")]:
  if c.get(k):opts.append("-D"+v+"="+c[k].replace("\\","/"))
 subprocess.run([c["cmake"],*opts],check=True)
 subprocess.run([c["cmake"],"--build",str(out),"--parallel",str(a.jobs)],check=True)
 dest=R/"dist/nonlinear_clock_rp2040.uf2";dest.parent.mkdir(exist_ok=True);shutil.copy2(out/"nonlinear_clock.uf2",dest);print(dest)
if __name__=="__main__":main()
