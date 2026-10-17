"""Request BOOTSEL using the SDK's standard USB CDC 1200-baud reset."""
import argparse
import time
import serial
from serial.tools import list_ports

def request_bootsel(name,timeout=2.0):
    if len([p for p in list_ports.comports() if p.device==name])!=1:
        raise RuntimeError("Specified serial device is not present")
    error=None
    try:
        # The SDK may disconnect immediately when Windows sets 1200 baud,
        # before pyserial has finished opening the handle.
        with serial.Serial(name,1200,timeout=.1,write_timeout=2) as port:
            port.dtr=True
            time.sleep(.1)
            port.dtr=False
    except serial.SerialException as exc:
        error=exc
    deadline=time.monotonic()+timeout
    while time.monotonic()<deadline:
        if not any(p.device==name for p in list_ports.comports()):
            return
        time.sleep(.05)
    if error:
        raise error
    raise RuntimeError("Device did not leave application mode; use the BOOT/RESET buttons")

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port",required=True,help="Clock USB CDC port")
    args=parser.parse_args()
    request_bootsel(args.port)
    print("Application USB port disconnected; wait for the RPI-RP2 BOOTSEL volume.")
if __name__=="__main__":main()

