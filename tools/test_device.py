"""Integration test on an explicitly selected clock; restores PC local time afterwards."""
import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import time
import serial
from sync_clock import sync

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port",required=True)
    args=parser.parse_args()
    events=[]
    def read_reply(port,command,prefix):
        port.write((command+"\n").encode("ascii"));port.flush()
        deadline=time.monotonic()+3
        while time.monotonic()<deadline:
            line=port.readline().decode("ascii",errors="replace").strip()
            if line.startswith(prefix):
                events.append({"command":command,"reply":line})
                print(command,"=>",line)
                return line
            if line.startswith("ERR") and prefix!="ERR":
                raise AssertionError(line)
        raise TimeoutError(command)
    result={"tested_at_local":datetime.now().isoformat(),"port":args.port,"events":events}
    with serial.Serial(args.port,115200,timeout=.1,write_timeout=2) as port:
        port.dtr=True;time.sleep(.2);port.reset_input_buffer()
        status=read_reply(port,"S","STATUS")
        original_brightness=int(re.search(r" B:(\d+)",status).group(1))
        try:
            pwm=[]
            for i in range(1,11):
                line=read_reply(port,f"B:{i:02d}","OK B ")
                pwm.append(int(re.search(r"PWM (\d+)/10000",line).group(1)))
            assert pwm[0]==100 and pwm[-1]==10000 and all(a<b for a,b in zip(pwm,pwm[1:]))
            for bad in ["X","B:00","B:11","T:24:00:00","T:12:60:00","T:2023:02:29","T:2100:02:29","T:2026:04:31","T:0000:01:01"]:
                read_reply(port,bad,"ERR")
            status=read_reply(port,"S","STATUS")
            assert " B:10 " in status
            read_reply(port,"X"*80+"B:1","ERR Line too long")
            status=read_reply(port,"S","STATUS")
            assert " B:10 " in status
            for date,expected in [
                ("2024:02:28","2024:02:29"),
                ("2100:02:28","2100:03:01"),
                ("2000:02:28","2000:02:29"),
                ("2026:12:31","2027:01:01"),
            ]:
                read_reply(port,"T:"+date,"OK DATE ")
                read_reply(port,"T:23:59:59","OK TIME ")
                time.sleep(1.25)
                status=read_reply(port,"S","STATUS")
                assert "T:"+expected in status and "T:00:00:" in status
            status=read_reply(port,"S","STATUS")
            first=re.search(r"STATUS T:(\d\d):(\d\d):(\d\d)",status)
            first_sec=sum(int(first.group(i))*factor for i,factor in zip([1,2,3],[3600,60,1]))
            time.sleep(1.15)
            status=read_reply(port,"S","STATUS")
            last=re.search(r"STATUS T:(\d\d):(\d\d):(\d\d)",status)
            last_sec=sum(int(last.group(i))*factor for i,factor in zip([1,2,3],[3600,60,1]))
            assert 1 <= (last_sec-first_sec)%86400 <= 2
            result["passed"]=True
        finally:
            sync(port,original_brightness)
    target=Path(__file__).resolve().parents[1]/"docs/hardware-test.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print("PASS: USB commands, all brightness levels, malformed lines, leap/century/year rollovers and timer progression.")
if __name__=="__main__":main()

