import time
import serial
import sys
import serial.tools.list_ports
import re
import os
from PySide6.QtWidgets import QApplication
import SCARAB_GUI
from GUI_Wrappers import base_menu

MEGA_IDS = [
    (0x2341, 0x0010),
    (0x2341, 0x0042),
    (0x2A03, 0x0010),
    (0x2A03, 0x0042),
    (0x1A86, 0x7523),
    (0x0403, 0x6001),
    (0x10C4, 0xEA60),
]

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

app = QApplication()
app.setStyle("Fusion")

window = base_menu()
controller = SCARAB_GUI.SCARABGUI(window)
window.show()

scarab = None
tryAgain = True
romType = b'\x00'
header = []
currentRom = ""
currentModule = ""
while tryAgain and scarab == None:
    for x in serial.tools.list_ports.comports():
        for y in MEGA_IDS:
            if y[0] == x.vid and y[1] == x.pid:
                scarab = serial.Serial(x.device, 2000000)
                break
        if scarab != None:
            break
    if scarab == None:
        choice = input("Device not found. Try again? [Y/N]")
        tryAgain = choice.capitalize().startswith(("Y"))
if scarab != None:
    print("Device Found!")
    time.sleep(2)
    scarab.write(b'\x01')
    val = scarab.read(6).decode()
    print(val)
    if val == "SCARAB":
        print("SCARAB Identified!")
    else:
        print(scarab.port)
        scarab.close()
        scarab = None
        print("Arduino connected, but not SCARAB.")
        sys.exit()
    while 1:
        print("Make a choice.")
        print("1. Detect Cartridge")
        print("2. Detect Module")
        print("3. Check Health")
        print("4. Dump Save")
        print("5. Restore Save")
        print("6. Exit")
        choice = input("Choice: ")
        match int(choice):
            case 1:
                scarab.write(b'\x11')
                header = scarab.read(32)
                if len(set(header)) == 1:
                    print("No cartridge inserted.")
                else:
                    if header[21] >> 5 != 1:
                        currentRom = header[0:22].decode(errors="replace")
                        print("Name: ", currentRom)
                        scarab.write(b'\x12')
                        time.sleep(0.2)
                        romType = scarab.read()
                        scarab.reset_input_buffer()
                        print("Rom Type: ", romType.decode(errors="replace"))
                    else:
                        currentRom = header[0:21].decode(errors="replace")
                        print("Name: ", currentRom)
                        match (header[21] & 15):
                            case 0:
                                print("LoRom")
                                romType = b'L'
                            case 1:
                                print("HiRom")
                                romType = b'H'
                            case 5:
                                print("ExHiRom")
                                romType = b'X'
                    cart_chipset = header[22] & 15
                    print("Chipset: ", SNES_CHIPSET[cart_chipset])
                    if cart_chipset > 0x2:
                        print("Coprocessor:  ", SNES_COPROCESSORS[header[22] >> 4])
                    print("ROM Size: ", 1 << header[23], "KB")
                    print("RAM Size: ", 1 << header[24], "KB")
            case 2:
                scarab.write(b'\x02')
                time.sleep(0.2)
                typeMod = scarab.read(8)
                scarab.reset_input_buffer()
                print(typeMod.decode(errors="replace"))
                currentModule = "SNES" #Hardcoded for now, EEPROM being annoying.
            case 3:
                print("Make a choice.")
                print("1. Test Pins")
                print("2. Test Save Retention")
                print("3. Test Corruption")
                print("4. Exit")
                test = input("Choice: ")
                match int(test):
                    case 1:
                        print("Checking data pin toggling against header...")
                        scarab.write(b'\x20')
                        scarab.write(romType)
                        results = scarab.read(2)
                        scarab.reset_input_buffer()
                        if results[0] != 255:
                            print("Not toggled low: ", bin(~results[0]))
                        if results[1] != 255:
                            print("Not toggled high: ", bin(~results[1]))
                        if results[1] == 255 and results[0] == 255:
                            print("All pins toggled correctly.")
                    case 3:
                        scarab.write(b'\x03')
            case 4:
                scarab.write(b'\x40')
                scarab.write(bytes([header[24]]))
                scarab.write(romType)
                ramSize =1024*(1 << header[24])
                print(ramSize)
                now = time.gmtime()
                gameName = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', currentRom.strip())
                os.makedirs("Saves/" + currentModule + "/" + gameName, exist_ok=True)
                filename = "Saves/" + currentModule + "/" + gameName + "/" + gameName + "_" + str(now.tm_mday) + "_" + str(now.tm_mon) + "_" + str(now.tm_year) + "_" + str(now.tm_hour) + "_" + str(now.tm_min) + "_" + str(now.tm_sec) + ".sav"
                save = open(filename, "wb")
                buffer = scarab.read_until(size=ramSize)
                save.write(buffer)
                print("Buffer in!")
                print("Saved as " + filename)
                print(4)
            case 5:
                scarab.write(b'\x41')
                scarab.write(bytes([header[24]]))
                scarab.write(romType)
                ramSize =32*(1 << header[24])
                sfile = open("test.srm", "rb")
                for i in range(ramSize):
                    while scarab.in_waiting < 1:
                        continue
                    if scarab.read() == b'M':
                        scarab.write(sfile.read(32))
                        while scarab.in_waiting < 1:
                            continue
                        if scarab.read() != b'K':
                            sys.exit()
                print("File Restored.")
            case 6:
                scarab.close()
                sys.exit()
else:
    print("No SCARAB Present.")
