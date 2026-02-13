import time
import serial
import sys
import serial.tools.list_ports
from PySide6 import QtWidgets

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

app = QtWidgets.QApplication()
scarab = None
tryAgain = True
romType = b'\x00'

class MainMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SCARAB Test")
        self.setFixedSize(800, 600)
        button = QtWidgets.QPushButton("gaming")
        self.setCentralWidget(button)

window = MainMenu()
window.show()
app.exec()

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
    if val == "SCARAB":
        print("SCARAB Identified!")
    else:
        scarab.close()
        scarab = None
        print("Arduino connected, but not SCARAB.")
        sys.exit()
    while 1:
        print("Make a choice.")
        print("1. Detect Cartridge")
        print("2. Dump Save")
        print("3. Check Health")
        print("4. Exit")
        choice = input("Choice: ")
        match int(choice):
            case 1:
                scarab.write(b'\x11')
                header = scarab.read(32)
                if header[21] >> 5 != 1:
                    print("Name: ", header[0:22].decode())
                    scarab.write(b'\x12')
                    time.sleep(0.2)
                    romType = scarab.read()
                    print("Rom Type: ", romType.decode())
                else:
                    print("Name: ", header[0:21].decode())
                    match (header[21] & 15):
                        case 0:
                            print("LoRom")
                            romType = 'L'
                        case 1:
                            print("HiRom")
                            romType = 'H'
                        case 5:
                            print("ExHiRom")
                            romType = 'X'
                cart_chipset = header[22] & 15
                print("Chipset: ", SNES_CHIPSET[cart_chipset])
                if cart_chipset > 0x2:
                    print("Coprocessor:  ", SNES_COPROCESSORS[header[22] >> 4])
                print("ROM Size: ", 1 << header[23], "KB")
            case 2:
                print(2)
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
                        if results[0] != 255:
                            print("Not toggled low: ", bin(~results[0]))
                        if results[1] != 255:
                            print("Not toggled high: ", bin(~results[1]))
                        if results[1] == 255 and results[0] == 255:
                            print("All pins toggled correctly.")
            case 4:
                sys.exit()
else:
    print("No SCARAB Present.")
