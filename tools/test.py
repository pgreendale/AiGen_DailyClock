"""Native C and Python tests; native gcc/clang/Zig required only for tests."""
import argparse,subprocess,shutil,os,sys
from pathlib import Path
import os
R=Path(os.path.abspath(__file__)).parents[1]
p=argparse.ArgumentParser();p.add_argument("--cc");p.add_argument("--previews",action="store_true");a=p.parse_args()
cc=a.cc or shutil.which("cc") or shutil.which("gcc") or shutil.which("clang") or shutil.which("zig")
if not cc:raise SystemExit("Native C compiler fehlt: --cc PFAD angeben")
base=[cc]+(["cc"] if Path(cc).stem=="zig" else [])
out=R/"build-host";out.mkdir(exist_ok=True)
common=["-std=c11","-O2","-Wall","-Wextra","-Werror","-Ifirmware/include","-Ifirmware/generated"]
src=["firmware/src/"+n+".c" for n in ["calendar","clock_state","protocol","clock_model","clock_render"]]+["firmware/generated/clock_assets.c"]
def run(main,name,args=()):
 exe=out/(name+(".exe" if os.name=="nt" else ""))
 subprocess.run(base+common+[main]+src+["-o",str(exe),"-lm"],cwd=R,check=True)
 subprocess.run([str(exe),*map(str,args)],cwd=R,check=True)
run("tests/test_core.c","test_core")
subprocess.run([sys.executable,"-m","unittest","discover","-s","tests","-p","test_*.py","-v"],cwd=R,check=True)
if a.previews:
 for h,m,s in [(8,15,30),(12,30,0),(23,45,0)]:
  run("tools/preview.c","preview",[out/f"preview_{h:02d}{m:02d}{s:02d}.ppm",h,m,s])
 subprocess.run([sys.executable,"tools/export_previews.py"],cwd=R,check=True)
