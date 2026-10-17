"""Fetch exact original inputs; reject files whose SHA-256 differs."""
from pathlib import Path
from urllib.request import urlopen,Request
import hashlib,json
R=Path(__file__).resolve().parent;out=R/"data";out.mkdir(exist_ok=True)
for s in json.loads((R/"sources.json").read_text()):
 p=out/s["filename"]
 if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==s["sha256"]:print("OK",p.name);continue
 with urlopen(Request(s["url"],headers={"User-Agent":"NonlinearClock research reproduction"}),timeout=120) as r:data=r.read()
 if hashlib.sha256(data).hexdigest()!=s["sha256"]:raise SystemExit("Quelldatei verändert: "+p.name)
 p.write_bytes(data);print("Verified",p.name)
