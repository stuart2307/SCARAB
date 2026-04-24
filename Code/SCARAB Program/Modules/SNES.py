#SCARAB SNES Module class
#Copyright (C) 2026 Stuart Rossiter
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

import serial

from Modules import Module_Base

class snes_module(Module_Base.scarab_module):
    
    """
    SNES/Super Nintendo cartridge module.

    Identification strategy:
      1. Read header from location 0x00FFC0 to 0x00FFDF
      2. Parse header for necessary information.

    SNES header byte positions (32 bytes):
        0-20    Cartridge Title (21 bytes uppercase ASCII. Unused bytes should be spaces.)
        21      ROM speed and memory map mode (LoROM/HiROM/ExHiROM)
        22      Chipset (Indicates if a cartridge contains extra RAM, a battery, and/or a coprocessor)
        23      ROM size: 1<<N kilobytes, rounded up (so 8=256KB, 12=4096KB and so on)
        24      RAM size: 1<<N kilobytes (so 1=2KB, 5=32KB, and so on)
        25      Country (Implies NTSC/PAL)
        26      Developer ID
        27      ROM version (0 = first)
        28-29   Checksum complement (Checksum ^ $FFFF)
        30-31   Checksum
    """
    SNES_CHIPSET = [
        "ROM Only",
        "ROM + RAM",
        "ROM + RAM + Battery",
        "ROM + Coprocessor",
        "ROM + Coprocessor + RAM",
        "ROM + Coprocessor + RAM + Battery",
        "ROM + Coprocessor + Battery",
    ]

    SNES_COPROCESSORS = {
        0x0: "DSP",
        0x1: "GSU",
        0x2: "OBC1",
        0x3: "SA-1",
        0x4: "S-DD1",
        0x5: "S-RTC",
        0xE: "Other",
        0xF: "Custom",
    }
    
    def getIdString(self):
        return "SNES"
    
    def detectCartridge(self, device: serial.Serial, cartDetails: dict) -> bool:
        device.write(b'\x11')
        header = device.read(32)
        if len(set(header)) == 1:
            cartDetails.clear()
            return False
        else:
            if header[21] >> 5 != 1:
                cartDetails["name"] = header[0:22].decode(errors="replace").strip()
                #print("Name: ", currentRom)
                device.write(b'\x12')
                cartDetails["romtype"] = device.read()
                device.reset_input_buffer()
                print("Rom Type: ", cartDetails["romtype"])
            else:
                cartDetails["name"] = header[0:21].decode(errors="replace").strip()
                #print("Name: ", currentRom)
                match (header[21] & 15):
                    case 0:
                        print("LoRom")
                        cartDetails["romtype"] = b'L'
                    case 1:
                        print("HiRom")
                        cartDetails["romtype"] = b'H'
                    case 5:
                        print("ExHiRom")
                        cartDetails["romtype"] = b'X'
            cartDetails["chipset"] = self.SNES_CHIPSET[header[22] & 15]
            print("Chipset: ", cartDetails["chipset"])
            if header[22] & 15 > 0x2:
                cartDetails["coprocessor"] = self.SNES_COPROCESSORS[header[22] >> 4]
                #print("Coprocessor:  ", self.SNES_COPROCESSORS[header[22] >> 4])
            cartDetails["romsize"] = str(1 << header[23]) + "KB"
            cartDetails["romexp"] = header[23]
            #print("ROM Size: ", 1 << header[23], "KB")
            if "RAM" not in cartDetails["chipset"]:
                cartDetails["saveexp"] = 0
                cartDetails["savesize"] = 0
            else:
                cartDetails["saveexp"] = header[24]
                cartDetails["savesize"] = 1024 * (1 << header[24])
            #print("RAM Size: ", 1 << header[24], "KB")
            cartDetails["checksum"] = f"0x{((header[30]) | header[31] << 8):04X}"
            return True

    def testPins(self, device: serial.Serial, cartDetails: dict) -> bool:
        print("Checking data pin toggling against header...")
        device.write(b'\x20')
        device.write(cartDetails["romtype"])
        results = device.read(2)
        device.reset_input_buffer()
        if results[0] != 255:
            print("Not toggled low: ", bin(~results[0]))
        if results[1] != 255:
            print("Not toggled high: ", bin(~results[1]))
        if results[1] == 255 and results[0] == 255:
            print("All pins toggled correctly.")
            return True
        return False

    def calculateChecksum(self, device: serial.Serial, cartDetails: dict):
        device.write(b'\x30')
        device.write(bytes((cartDetails["romexp"],)))
        device.write(cartDetails["romtype"])
        checksum = device.read(2)
        print(checksum)
        checksum = f"0x{(checksum[0] << 8) | (checksum[1]):04X}"
        print(cartDetails["checksum"])
        print(checksum)
        return cartDetails["checksum"] == checksum

    def testSaveRetention(self, device: serial.Serial, cartDetails: dict):
        return True

    def dumpSave(self, device: serial.Serial, cartDetails: dict) -> bytes:
        device.write(b'\x40')
        device.write(bytes((cartDetails["saveexp"],)))
        device.write(cartDetails["romtype"])
        ramSize = 1024*(1 << int(cartDetails["saveexp"]))
        buffer = device.read_until(expected= bytes("SCARABSAVEDATA", "utf-8", "replace"),size=ramSize)
        print(len(buffer))
        return buffer

    def restoreSave(self, device: serial.Serial, cartDetails: dict, buffer: bytes):
        device.write(b'\x41')
        device.write(bytes((cartDetails["saveexp"],)))
        device.write(cartDetails["romtype"])
        for i in range(0, len(buffer), 32):
            while device.in_waiting < 1:
                continue
            if device.read() == b'M':
                chunk = buffer[i:i+32]
                device.write(chunk)
                while device.in_waiting < 1:
                    continue
                if device.read() != b'K':
                    return False
            else:
                return False
        return True