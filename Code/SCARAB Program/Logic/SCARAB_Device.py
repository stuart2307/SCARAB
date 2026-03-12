import serial, serial.tools.list_ports

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
    def open(self):
        for x in serial.tools.list_ports.comports():
            for y in MEGA_IDS:
                if y[0] == x.vid and y[1] == x.pid:
                    scarab = serial.Serial(x.device, 2000000)
                    break
            if scarab != None:
                break