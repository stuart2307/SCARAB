#SCARAB Device Module class
#Copyright (C) 2026 Stuart Rossiter
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
import serial
from abc import ABC, abstractmethod


class scarab_module(ABC):
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
    def dumpSave(self, device: serial.Serial, cartDetails: dict) -> bytes:
        pass
    
    @abstractmethod
    def restoreSave(self, device: serial.Serial, cartDetails: dict, buffer: bytes):
        pass