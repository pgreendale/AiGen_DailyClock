"""Audit the actual package, including hidden/ignored files, without storing host details."""
from pathlib import Path
import os,re,json,hashlib,struct,base64,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
errors=[];review=[]
def add(path,category):errors.append({"file":path.relative_to(R).as_posix(),"category":category})
blocked_dirs={"build","build-host","dist","__pycache__",".venv",".git"}
files=[]
for p in sorted(R.rglob("*")):
 rel=p.relative_to(R)
 if p.is_symlink():add(p,"symlink")
 if p.is_dir() and p.name in blocked_dirs:add(p,"generated directory or repository metadata")
 if p.is_file():files.append(p)
private=[]
for key in ("USERNAME","COMPUTERNAME","USERPROFILE","HOMEPATH"):
 value=os.environ.get(key,"")
 if len(value)>3:private.append(value)
private.extend([str(R),str(R.parent)])
patterns=[
 ("network address",r"(?<![\d.])(?:192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})(?![\d.])"),
 ("user home path",r"(?:[A-Za-z]:[/\\](?:Users|Documents and Settings)[/\\]|/(?:Users|home)/)[^/\\\s\"<>]+"),
 ("UNC share path",r"\\{2}[A-Za-z0-9_.-]+\\[A-Za-z0-9_.$-]+"),
 ("private key",r"-{5}BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-{5}"),
 ("access token",r"(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16}|sk-proj-[A-Za-z0-9_-]{30,})"),
]
def scan_text(p,text):
 for value in private:
  if re.search(r"(?<![A-Za-z0-9])"+re.escape(value)+r"(?![A-Za-z0-9])",text,re.I):add(p,"current host identifier or absolute workspace path");break
 for category,pat in patterns:
  if re.search(pat,text):add(p,category)
 # Absolute Windows paths may only be clearly fictional documentation examples.
 for match in re.finditer(r"(?<![A-Za-z0-9])[A-Za-z]:[/\\][^\s\"'<>)]*",text):
  path=match.group()
  if path not in {"D:/"} and not path.startswith("C:/Pfad/"):add(p,"absolute Windows path")
def scan_png(p,data):
 pos=8
 while pos<len(data):
  size=struct.unpack(">I",data[pos:pos+4])[0];kind=data[pos+4:pos+8]
  if kind in {b"tEXt",b"zTXt",b"iTXt",b"eXIf",b"tIME"}:add(p,"PNG text/EXIF/time metadata")
  pos+=12+size
for p in files:
 rel=p.relative_to(R).as_posix()
 if rel=="cmake/local-tools.json":add(p,"machine-local configuration")
 if p.suffix.lower() in {".exe",".elf",".uf2",".obj",".o",".pyc",".zip",".pdf",".xlsx",".ods"}:add(p,"generated or unreviewed binary")
 try:data=p.read_bytes()
 except OSError:add(p,"unreadable file");continue
 # Scan raw strings in UTF-8/Latin-1 and UTF-16 as well as ordinary source files.
 scan_text(p,data.decode("utf-8",errors="replace"))
 scan_text(p,data.decode("utf-16-le",errors="ignore"))
 if p.suffix==".png":scan_png(p,data)
 if p.suffix==".svg":
  root=ET.fromstring(data)
  if any(e.tag.rsplit("}",1)[-1]=="metadata" for e in root.iter()):add(p,"SVG metadata")
  for encoded in re.findall(rb"data:image/png;base64,([A-Za-z0-9+/=\s]+)",data):
   scan_png(p,base64.b64decode(encoded))
 if p.suffix==".md":
  for target in re.findall(r"\]\(([^)]+)\)",data.decode("utf-8-sig")):
   if target.startswith(("http:","https:","#","mailto:")):continue
   target=target.split("#")[0]
   if target and not (p.parent/target).exists():add(p,"broken documentation link")
result={"relative_document_links":"passed" if not any(e["category"]=="broken documentation link" for e in errors) else "failed",
 "physical_package_scan":"passed" if not errors else "failed","files_checked":len(files),
 "includes_hidden_and_ignored_files":True,"includes_binary_strings_and_image_metadata":True,
 "host_specific_patterns_embedded_in_scanner":False,"findings":errors,
 "intentional_public_content":["pgreendale author credit","project name and relative repository paths","required build tools and documented versions","public third-party names, licenses, contacts and source URLs","explicitly fictional command examples"]}
if errors:raise SystemExit(json.dumps(result,indent=2,ensure_ascii=False))
(R/"docs/evidence/package-check.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
manifest=[]
for p in files:
 if p.relative_to(R).as_posix() in {"docs/evidence/integrity.sha256","docs/evidence/package-check.json"}:continue
 manifest.append(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.relative_to(R).as_posix())
(R/"docs/evidence/integrity.sha256").write_text("\n".join(sorted(manifest))+"\n",encoding="utf-8")
print(json.dumps(result,indent=2,ensure_ascii=False))
