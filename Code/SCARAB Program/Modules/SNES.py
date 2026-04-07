import serial

from Modules import Module_Base
from time import sleep

from SCARAB_Logic import Test_Results

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
    
    def getIdString(self):
        return "SNES"
    
    def detectCartridge(self, device: serial.Serial, cartDetails: dict) -> bool:
        device.write(b'\x11')
        sleep(.2)
        header = device.read(32)
        if len(set(header)) == 1:
            return False
        else:
            if header[21] >> 5 != 1:
                cartDetails["name"] = header[0:22].decode(errors="replace").strip()
                #print("Name: ", currentRom)
                device.write(b'\x12')
                sleep(0.2)
                cartDetails["romtype"] = device.read()
                device.reset_input_buffer()
                print("Rom Type: ", cartDetails["romtype"])
            else:
                cartDetails["name"] = header[0:21].decode(errors="replace")
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
            cartDetails["romsize"] = 1 << header[23]
            cartDetails["romexp"] = header[23]
            #print("ROM Size: ", 1 << header[23], "KB")
            if "RAM" not in cartDetails["chipset"]:
                cartDetails["savesize"] = 0
            else:
                cartDetails["savesize"] = header[24]
            #print("RAM Size: ", 1 << header[24], "KB")
            cartDetails["checksum"] = f"0x{((header[30]) | header[31] << 8):04X}"
            return True

    def checkHealth(self, device, cartDetails, pins, checksum, retention) -> Test_Results.test_result:
        results = Test_Results.test_result()
        if pins:
            results.pins_ok = self.testPins(device, cartDetails)
        if checksum:
            results.checksum_ok = self.calculateChecksum(device, cartDetails)
        if retention:
            results.retention_ok = self.testSaveRetention(device, cartDetails)
        return results

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

    def dumpSave(self, device: serial.Serial, cartDetails: dict):
        device.write(b'\x40')
        device.write(bytes((cartDetails["savesize"],)))
        device.write(cartDetails["romtype"])
        ramSize = 1024*(1 << int(cartDetails["savesize"]))
        #now = gmtime()
        #gameName = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', cartDetails["name"].strip())
        #filename = "Saves/SNES/" + gameName + "/" + gameName + "_" + str(now.tm_mday) + "_" + str(now.tm_mon) + "_" + str(now.tm_year) + "_" + str(now.tm_hour) + "_" + str(now.tm_min) + "_" + str(now.tm_sec) + ".sav"
        buffer = device.read_until(expected= bytes("SCARABSAVEDATA", "utf-8", "replace"),size=ramSize)
        print(len(buffer))
        return buffer
        #print("Buffer in!")
        #print("Saved as " + filename)

    def restoreSave(self, device: serial.Serial, cartDetails: dict, buffer: bytes):
        device.write(b'\x41')
        device.write(bytes(cartDetails["savesize"]))
        device.write(bytes(cartDetails["romtype"]))
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
        return True