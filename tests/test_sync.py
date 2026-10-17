import importlib.util
from pathlib import Path
import unittest
from datetime import datetime
spec=importlib.util.spec_from_file_location("sync_clock",Path(__file__).resolve().parents[1]/"tools/sync_clock.py")
sync_clock=importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync_clock)

class Port:
    def __init__(self,lines): self.lines=list(lines);self.written=[]
    def write(self,value): self.written.append(value)
    def flush(self): pass
    def readline(self): return self.lines.pop(0) if self.lines else b""

class Tests(unittest.TestCase):
    def test_formats(self):
        self.assertEqual(sync_clock.commands_for(datetime(2024,2,29,0,3,4)),("T:2024:02:29","T:00:03:04"))
    def test_banner_is_ignored(self):
        p=Port([b"Commands\n",b"OK DATE 2026:10:17\n"])
        self.assertEqual(sync_clock.exchange(p,"T:2026:10:17","OK DATE"),"OK DATE 2026:10:17")
        self.assertEqual(p.written,[b"T:2026:10:17\n"])
    def test_rejection(self):
        with self.assertRaises(RuntimeError):
            sync_clock.exchange(Port([b"ERR Invalid\n"]),"T:2023:02:29","OK DATE")
    def test_timeout(self):
        with self.assertRaises(TimeoutError):
            sync_clock.exchange(Port([]),"S","STATUS",timeout=.001)
if __name__=="__main__":unittest.main()

