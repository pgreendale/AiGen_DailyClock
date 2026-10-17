#!/usr/bin/env python3
"""Set the device to the computer's local date/time over USB CDC."""
import argparse
from datetime import datetime
import math
import sys
import time

def commands_for(moment):
    return (f"T:{moment.year:04d}:{moment.month:02d}:{moment.day:02d}",
            f"T:{moment.hour:02d}:{moment.minute:02d}:{moment.second:02d}")

def exchange(port,command,expected,timeout=3.0):
    port.write((command+"\n").encode("ascii"))
    port.flush()
    deadline=time.monotonic()+timeout
    while time.monotonic()<deadline:
        line=port.readline().decode("ascii",errors="replace").strip()
        if line.startswith("ERR"):
            raise RuntimeError(f"Device rejected {command!r}: {line}")
        if line.startswith(expected):
            return line
    raise TimeoutError(f"No {expected!r} acknowledgement for {command!r}")

def sync(port,brightness=None):
    # Arrange transmission at a whole local second. Prepare the matching date
    # first, including the case where this second is already on the next day.
    target=math.ceil(time.time()+0.15)
    moment=datetime.fromtimestamp(target)
    date_command,time_command=commands_for(moment)
    print(exchange(port,date_command,"OK DATE "+date_command[2:]))
    while time.time()<target:
        time.sleep(min(.01,max(0,target-time.time())))
    if time.time()-target>.25:
        # A suspended/overloaded host must not transmit a stale clock value.
        moment=datetime.now()
        date_command,time_command=commands_for(moment)
        print(exchange(port,date_command,"OK DATE "+date_command[2:]))
    print(exchange(port,time_command,"OK TIME "+time_command[2:]))
    if brightness is not None:
        print(exchange(port,f"B:{brightness}","OK B "))
    print(exchange(port,"S","STATUS "))

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port",help="COM port, e.g. COM7; Linux: /dev/ttyACM0")
    parser.add_argument("--brightness",type=int,choices=range(1,11),metavar="1..10")
    parser.add_argument("--list",action="store_true",help="List serial ports")
    parser.add_argument("--dry-run",action="store_true",help="Print commands without connecting")
    args=parser.parse_args(argv)
    if args.dry_run:
        print("\n".join(commands_for(datetime.now())))
        if args.brightness is not None:
            print(f"B:{args.brightness}")
        return 0
    try:
        import serial
        from serial.tools import list_ports
    except ImportError:
        parser.error("Install pyserial first: python -m pip install -r tools/requirements.txt")
    ports=list(list_ports.comports())
    if args.list:
        for p in ports:
            print(f"{p.device}: {p.description} [{p.hwid}]")
        return 0
    chosen=args.port
    if not chosen:
        candidates=[p for p in ports if "nonlinear" in (p.product or "").lower()]
        if not candidates:
            candidates=[p for p in ports if p.vid==0x2e8a]
        if len(candidates)!=1:
            parser.error("Cannot uniquely identify the clock. Use --list, then --port COMx.")
        chosen=candidates[0].device
    try:
        # 115200 is a USB CDC line-coding value, not a physical baud-rate limit.
        with serial.Serial(chosen,115200,timeout=.1,write_timeout=2) as port:
            port.dtr=True
            time.sleep(.35)
            port.reset_input_buffer()
            sync(port,args.brightness)
    except (serial.SerialException,OSError,RuntimeError,TimeoutError) as exc:
        print(f"Clock sync failed: {exc}",file=sys.stderr)
        return 1
    return 0

if __name__=="__main__":
    raise SystemExit(main())

