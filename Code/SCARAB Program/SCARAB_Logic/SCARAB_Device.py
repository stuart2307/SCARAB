import importlib
import inspect
import pkgutil
from sys import modules
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

class scarab_device():
    def __init__(self):
        super().__init__()
        self.scarab = None
        self.cartridge = dict()
        self.modules = dict()
        self.currentModule: Module_Base.scarab_module
        self.loadSupportedModules()
        
    def loadSupportedModules(self):
        for _, moduleName, _ in pkgutil.iter_modules(Modules.__path__):
            module = importlib.import_module("Modules." + moduleName)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, Module_Base.scarab_module) and obj is not Module_Base.scarab_module:
                    self.modules[obj.getIdString()] = obj()
        
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
        typeMod = self.scarab.read(16)
        self.scarab.reset_input_buffer()
        typeMod = typeMod.decode(errors="replace").strip()
        self.currentModule = self.modules[typeMod] or None
        
    def dumpSave(self):
        return self.currentModule.dumpSave(self.scarab, self.cartridge)
    
    def restoreSave(self, buffer: bytes):
        return self.currentModule.restoreSave(self.scarab, self.cartridge, buffer)
        