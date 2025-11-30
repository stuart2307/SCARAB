import serial
import time

def read_until_silence(ser, silence_period=0.05):
    """Reads from serial until no data is received for `silence_period` seconds"""
    buffer = bytearray()
    last = time.time()
    while True:
        chunk = ser.read(1024)
        if chunk:
            buffer.extend(chunk)
            last = time.time()
        elif time.time() - last > silence_period:
            break
    return bytes(buffer)

# open serial port
scarab = serial.Serial("/dev/ttyACM0", 2000000, timeout=0.01)
time.sleep(2)  # Arduino reset

# send command
scarab.write(b'\x67')

# read all response
data = read_until_silence(scarab)
print(data.decode(errors="ignore"))
