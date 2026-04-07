import serial
from abc import ABC, abstractmethod
from SCARAB_Logic import Test_Results


class scarab_module(ABC):
    @abstractmethod
    def getIdString(self):
        pass
    
    @abstractmethod
    def detectCartridge(self, device: serial.Serial, cartDetails: dict) -> bool:
        pass
    
    @abstractmethod
    def checkHealth(self, device: serial.Serial, cartDetails:dict, pins: bool, checksum: bool, retention: bool) -> Test_Results.test_result:
        pass
    
    @abstractmethod
    def testPins(self, device: serial.Serial, cartDetails: dict):
        pass
    
    @abstractmethod
    def calculateChecksum(self, device: serial.Serial, cartDetails: dict):
        pass
    
    @abstractmethod
    def testSaveRetention(self, device: serial.Serial, cartDetails: dict):
        pass
    
    @abstractmethod
    def dumpSave(self, device: serial.Serial, cartDetails: dict):
        pass
    
    @abstractmethod
    def restoreSave(self, device: serial.Serial, cartDetails: dict, buffer: bytes):
        pass