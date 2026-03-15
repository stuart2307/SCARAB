import serial
from abc import ABC, abstractmethod

class scarab_module():
    @abstractmethod
    def identify(self, device: serial.Serial):
        pass
    
    @abstractmethod
    def read(self, device: serial.Serial):
        pass
    
    @abstractmethod
    def write(self, device: serial.Serial):
        pass
    
    @abstractmethod
    def dumpSave(self, device: serial.Serial):
        pass
    
    @abstractmethod
    def restoreSave(self, device: serial.Serial):
        pass