import serial
from abc import ABC, abstractmethod


class scarab_module(ABC):
    @abstractmethod
    def getApiId(self):
        pass
    
    @abstractmethod
    def getIdString(self):
        pass
    
    @abstractmethod
    def detectCartridge(self, device: serial.Serial, cartDetails: dict) -> bool:
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