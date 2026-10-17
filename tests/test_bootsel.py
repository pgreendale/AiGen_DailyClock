import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch
try:
    import serial
except ImportError:
    serial=None

@unittest.skipIf(serial is None,"pyserial is required for the USB bootloader helper tests")
class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location("enter_bootsel",Path(__file__).resolve().parents[1]/"tools/enter_bootsel.py")
        cls.module=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.module)
    def test_windows_reset_during_open(self):
        with patch.object(self.module.list_ports,"comports",side_effect=[[SimpleNamespace(device="COM3")],[]]),\
             patch.object(self.module.serial,"Serial",side_effect=serial.SerialException("Device disappeared")):
            self.module.request_bootsel("COM3")
    def test_missing_device(self):
        with patch.object(self.module.list_ports,"comports",return_value=[]):
            with self.assertRaises(RuntimeError):
                self.module.request_bootsel("COM3")
if __name__=="__main__":unittest.main()

