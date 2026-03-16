import os
import re
import sys
import serial

from Modules import Module_Base
from time import sleep, gmtime

class snes_module(Module_Base.scarab_module):
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
    
    def getIdString():
        return "SNES"
    
    def detectCartridge(self, device: serial.Serial, cartDetails: dict):
        device.write(b'\x11')
        header = device.read(32)
        if len(set(header)) == 1:
            return False
        else:
            if header[21] >> 5 != 1:
                cartDetails["name"] = header[0:22].decode(errors="replace")
                #print("Name: ", currentRom)
                device.write(b'\x12')
                sleep(0.2)
                cartDetails["romtype"] = device.read()
                device.reset_input_buffer()
                #print("Rom Type: ", self.romType.decode(errors="replace"))
            else:
                cartDetails["name"] = header[0:21].decode(errors="replace")
                #print("Name: ", currentRom)
                match (header[21] & 15):
                    case 0:
                        #print("LoRom")
                        cartDetails["romtype"] = b'L'
                    case 1:
                        #print("HiRom")
                        cartDetails["romtype"] = b'H'
                    case 5:
                        #print("ExHiRom")
                        cartDetails["romtype"] = b'X'
            cartDetails["chipset"] = header[22] & 15
            print("Chipset: ", self.SNES_CHIPSET[cartDetails["chipset"]])
            if cartDetails["chipset"] > 0x2:
                cartDetails["coprocessor"] = self.SNES_COPROCESSORS[header[22] >> 4]
                #print("Coprocessor:  ", self.SNES_COPROCESSORS[header[22] >> 4])
            cartDetails["romsize"] = 1 << header[23]
            #print("ROM Size: ", 1 << header[23], "KB")
            cartDetails["ramsize"] = 1 << header[24]
            #print("RAM Size: ", 1 << header[24], "KB")
            return True

    def testPins(self, device: serial.Serial, cartDetails: dict):
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

    def calculateChecksum(self, device: serial.Serial, cartDetails: dict):
        pass

    def testSaveRetention(self, device: serial.Serial, cartDetails: dict):
        pass

    def dumpSave(self, device: serial.Serial, cartDetails: dict):
        device.write(b'\x40')
        device.write(bytes(cartDetails["ramsize"]))
        device.write(cartDetails["romtype"])
        ramSize =1024*(cartDetails["ramsize"])
        #print(ramSize)
        now = gmtime()
        gameName = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', cartDetails["name"].strip())
        os.makedirs("Saves/SNES/" + gameName, exist_ok=True)
        filename = "Saves/SNES/" + gameName + "/" + gameName + "_" + str(now.tm_mday) + "_" + str(now.tm_mon) + "_" + str(now.tm_year) + "_" + str(now.tm_hour) + "_" + str(now.tm_min) + "_" + str(now.tm_sec) + ".sav"
        save = open(filename, "wb")
        buffer = device.read_until(size=ramSize)
        save.write(buffer)
        #print("Buffer in!")
        #print("Saved as " + filename)

    def restoreSave(self, device: serial.Serial, path, cartDetails: dict):
        device.write(b'\x41')
        device.write(bytes(cartDetails["ramsize"]))
        device.write(cartDetails["romtype"])
        chunks =32*(cartDetails["ramsize"])
        sfile = open(path, "rb")
        for i in range(chunks):
            while device.in_waiting < 1:
                continue
            if device.read() == b'M':
                device.write(sfile.read(32))
                while device.in_waiting < 1:
                    continue
                if device.read() != b'K':
                    return False
        return True