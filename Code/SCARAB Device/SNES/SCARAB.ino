#define EEPROM_CONTROL_ADDRESS 0x50
#define NOP __asm__ __volatile__("nop\n\t")
#include <Wire.h>

void setup() {
  Serial.begin(2000000);
  Wire.begin();
  Wire.setWireTimeout(1000, true);
}

void eeprom_write_page(byte deviceaddress, uint8_t eeaddr, const byte * data, byte length)
{
    Wire.beginTransmission(deviceaddress);
    Wire.write(int(eeaddr));
    for (int i = 0; i < length; i++) {
        Wire.write(data[i]);
    }
    Wire.endTransmission();
    delay(10);
}

int eeprom_read_buffer(byte deviceaddr, uint8_t eeaddr, byte * buffer, byte length)
{
    Wire.beginTransmission(deviceaddr);
    Wire.write(int(eeaddr));
    Wire.endTransmission(false);

    Wire.requestFrom(deviceaddr, length);
    int i;
    for (i = 0; i < length && Wire.available(); i++) {
        buffer[i] = Wire.read();
    }
    return i;
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0)
  {
    uint8_t op = Serial.read();
    switch (op) {
      case 0x01:{
        Serial.print("SCARAB");
        break;}
      case 0x02:{
        byte myBuff[8];
        eeprom_read_buffer(0x50, 0x00, myBuff, 0x08);
        String mod = (char *)myBuff;
        if (mod.equalsIgnoreCase("SNES    ")) {snes_setup();}
        if (mod.equalsIgnoreCase("NES     ")) {nes_setup();}
        Serial.write(myBuff, 8);
        break;
      }
      case 0x03:{
        byte myBuff[8];
        while(Serial.available() < 8){}
        for (int i = 0; i < 8; i++) {
          myBuff[i] = Serial.read();
        }
        eeprom_write_page(0x50, 0x00, myBuff, 0x08);
        Serial.println("OK");
        break;
      }
      case 0x11:{
        snes_setup();
        uint8_t buffer[64];
        readSnesHeader(buffer, SNES_HEADER_START, SNES_HEADER_END, 'H');
        Serial.write(buffer, SNES_HEADER_SIZE);
        break;}
      case 0x12:{
        snes_setup();
        uint8_t header[64];
        readSnesHeader(header, SNES_HEADER_START, SNES_HEADER_END, 'H');
        uint8_t headerCheck[64];
        readSnesHeader(headerCheck, SNES_HEADER_START, SNES_HEADER_END, 'L');
        boolean loRom = true;
        for (uint8_t count = 0; count < SNES_HEADER_SIZE && loRom; count++) {
          loRom = header[count] == headerCheck[count];
        }
        if (loRom) {Serial.write('L');}
        else {
          readSnesHeader(headerCheck, SNES_HEADER_START, SNES_HEADER_END, 'X');
          boolean exHiRom = true;
          for (uint8_t count = 0; count < SNES_HEADER_SIZE && exHiRom; count++) {
            exHiRom = header[count] == headerCheck[count];
          }
          if (exHiRom) {Serial.write('X');}
          else {Serial.write('H');}
        }
        break;
      }
      case 0x20:{
        snes_setup();
        testDataPinsSnes('H');
        break;}

      case 0x21: {
        while (Serial.available() < 2) {}
        nes_setup();
        uint8_t mapper = Serial.read();
        uint8_t banks = Serial.read();
        testPrgDataPins(mapper, banks);
        break;
      }
      case 0x22: {
        while (Serial.available() < 2) {}
        nes_setup();
        uint8_t mapper = Serial.read();
        uint8_t banks = Serial.read();
        testChrDataPins(mapper, banks);
        break;
      }
      
      case 0x30:{
        while(Serial.available() < 2){}
        snes_setup();
        uint8_t romPow = Serial.read();
        char romType = Serial.read();
        uint64_t romSize = 1024UL << romPow;
        uint16_t crc = calcSnesChecksum(romSize, romType);
        uint8_t upper = crc >> 8;
        uint8_t lower = crc & 0xFF;
        Serial.write(upper);
        Serial.write(lower);
        break;
      }

      case 0x31: {
        while (Serial.available() < 2) {}
        nes_setup();
        uint8_t mapper = Serial.read();
        uint8_t banks = Serial.read();
        uint32_t crc = calcPrgCrc32(mapper, banks);
        Serial.write((crc >> 24) & 0xFF);
        Serial.write((crc >> 16) & 0xFF);
        Serial.write((crc >>  8) & 0xFF);
        Serial.write(crc & 0xFF);
        break;
      }

      case 0x32: {
        while (Serial.available() < 2) {}
        nes_setup();
        uint8_t mapper = Serial.read();
        uint8_t banks = Serial.read();
        uint32_t crc = calcChrCrc32(mapper, banks);
        Serial.write((crc >> 24) & 0xFF);
        Serial.write((crc >> 16) & 0xFF);
        Serial.write((crc >>  8) & 0xFF);
        Serial.write(crc & 0xFF);
        break;
      }
        
      case 0x40:{
        while(Serial.available() < 2){}
        snes_setup();
        uint8_t ramPow = Serial.read();
        char romType = Serial.read();
        uint64_t ramSize = 1024 * pow(2, ramPow);
        dumpSnesSave(ramSize, romType);
        break;
      }
      case 0x41:{
        while(Serial.available() < 2){}
        snes_setup();
        uint8_t ramPow = Serial.read();
        char romType = Serial.read();
        uint64_t ramSize = 1024 * pow(2, ramPow);
        prepSnesWrite();
        restoreSnesSave(ramSize, romType);
        break;
      }
      case 0x50: {
        nes_setup();
        dumpNesSave();
        break;
      }

      case 0x51: {
        nes_setup();
        restoreNesSave();
        break;
      }
      case 0x60: {
        while (Serial.available() < 2) {}
        nes_setup();
        uint8_t base_page = Serial.read();
        uint8_t num_banks = Serial.read();
        uint16_t base_addr = base_page ? 0xE000 : 0x8000;
        uint8_t buffer[64];
        prepPrgRead();
        NES_ROMSEL_LOW;
        for (uint8_t b = 0; b < num_banks; b++) {
          for (uint16_t x = 0; x < 0x2000; x++) {
            buffer[x % 64] = readPrg(base_addr + x);
            if (x % 64 == 63) {
              Serial.write(buffer, 64);
              Serial.flush();
              while (Serial.available() < 1) {}
              Serial.read();
            }
          }
        }
        NES_ROMSEL_HIGH;
        break;
      }
    case 0x70: {
        while (Serial.available() < 2) {}
        uint8_t mapper = Serial.read();
        uint8_t banks = Serial.read();
        dumpPrgRom(mapper, banks);
        break;
      }

      case 0x71: {
        while (Serial.available() < 2) {}
        uint8_t mapper = Serial.read();
        uint8_t banks = Serial.read();
        dumpChrRom(mapper, banks);
        break;
      }
    }
  }
}