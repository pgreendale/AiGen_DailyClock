"""Copy only an RP2040 UF2 to a verified RPI-RP2 BOOTSEL volume."""
import argparse
from pathlib import Path
import shutil
import struct
def validate_uf2(path):
    data=path.read_bytes()
    if not data or len(data)%512: raise ValueError("Not a UF2 file")
    for offset in range(0,len(data),512):
        block=data[offset:offset+512]
        a,b,flags,target,size,index,total,family=struct.unpack_from("<8I",block)
        end,=struct.unpack_from("<I",block,508)
        if (a,b,end)!=(0x0a324655,0x9e5d5157,0x0ab16f30):
            raise ValueError("Invalid UF2 magic")
        if not flags&0x2000 or family!=0xe48bff56:
            raise ValueError("This uploader accepts only RP2040 firmware")
        if size>476 or target<0x10000000 or target+size>0x10200000:
            raise ValueError("UF2 block is outside the 2 MB flash")
    return len(data)//512
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--drive",required=True,help="BOOTSEL drive, e.g. D:/")
    parser.add_argument("--firmware",type=Path,default=Path(__file__).resolve().parents[1]/"dist/nonlinear_clock_rp2040.uf2")
    args=parser.parse_args()
    root=Path(args.drive)
    if not root.is_absolute(): parser.error("--drive must be an absolute path")
    info=(root/"INFO_UF2.TXT").read_text()
    if "Board-ID: RPI-RP2" not in info: raise ValueError("Target is not an RP2040 BOOTSEL volume")
    blocks=validate_uf2(args.firmware)
    print(f"Validated {blocks} RP2040 UF2 blocks; copying to {root}")
    shutil.copyfile(args.firmware,root/args.firmware.name)
    print("UF2 copied. Device should reboot and expose its USB CDC port.")
if __name__=="__main__":main()

