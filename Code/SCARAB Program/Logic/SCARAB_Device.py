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

    def identifyScarab(self):
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
                val = self.scarab.read(6).decode()
                print(val)
                if val == "SCARAB":
                    print("SCARAB Identified!")
                    return True
                else:
                    print("GG go next")
                    self.scarab.close()
                    self.scarab = None
        return False
        