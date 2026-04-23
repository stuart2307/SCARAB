import importlib
import inspect
from pathlib import Path
import pkgutil
import sys
from Modules import Module_Base
import Modules
import serial, serial.tools.list_ports, time

MEGA_IDS = [
    (0x2341, 0x0010),
    (0x2341, 0x0042),
    (0x2A03, 0x0010),
    (0x2A03, 0x0042),
    (0x1A86, 0x7523),
    (0x0403, 0x6001),
    (0x10C4, 0xEA60),
]
MODULES_PATH = BASE_PATH = (Path(sys.executable).parent if hasattr(sys, '_MEIPASS') else Path(__file__).parent.parent) / "Modules"
MODULES_PATH.mkdir(parents=True, exist_ok=True)

class scarab_device():
    def __init__(self):
        self.scarab = None
        self.cartridge = dict()
        self.modules = dict()
        self.currentModule: Module_Base.scarab_module
        self.loadSupportedModules()
        
    def loadSupportedModules(self):
        for module_file in MODULES_PATH.glob("*.py"):
            if module_file.name.startswith("_"):
                continue
            spec = importlib.util.spec_from_file_location(module_file.stem, module_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, Module_Base.scarab_module) and obj is not Module_Base.scarab_module:
                    mod = obj()
                    self.modules[mod.getIdString()] = mod
        
    def identifyScarab(self) -> bool:
        if self.scarab != None:
            self.scarab.close()
            self.scarab = None
        for x in serial.tools.list_ports.comports():
            for y in MEGA_IDS:
                if y[0] == x.vid and y[1] == x.pid:
                    self.scarab = serial.Serial(x.device, 2000000)
                    break
            if self.scarab != None:
                print("Device Found!")
                time.sleep(2)
                self.scarab.write(b'\x01')
                val = self.scarab.read(6).decode(errors="replace")
                print(val)
                if val == "SCARAB":
                    print("SCARAB Identified!")
                    return True
                else:
                    print("GG go next")
                    self.scarab.close()
                    self.scarab = None
        return False
    
    def identifyModule(self):
        self.scarab.write(b'\x02')
        time.sleep(0.2)
        typeMod = self.scarab.read(8)
        self.scarab.reset_input_buffer()
        typeMod = typeMod.decode(errors="replace").strip()
        try :
            self.currentModule = self.modules[typeMod]
        except KeyError as e:
            self.currentModule = None
        
    def writeEeprom(self, string):
        print("HELLO" + string + "HELLO")
        if len(string) < 8:
            for _ in range(8-len(string)):
                string += ' '
        self.scarab.write(b'\x03')
        self.scarab.write(bytes(string[0:8], "utf-8", "replace"))
        time.sleep(0.1)
        self.scarab.read(2)
        
    def dumpSave(self) -> bytes:
        return self.currentModule.dumpSave(self.scarab, self.cartridge)
    
    def restoreSave(self, buffer: bytes):
        return self.currentModule.restoreSave(self.scarab, self.cartridge, buffer)
    
    #def checkHealth(self, pins, checksum, retention):
    #    return self.currentModule.checkHealth(self.scarab, self.cartridge, pins, checksum, retention)
    
    def testPins(self):
        return self.currentModule.testPins(self.scarab, self.cartridge)
    
    def calcChecksum(self):
        return self.currentModule.calculateChecksum(self.scarab, self.cartridge)
    
    def testRetention(self):
        return self.currentModule.testSaveRetention(self.scarab, self.cartridge)