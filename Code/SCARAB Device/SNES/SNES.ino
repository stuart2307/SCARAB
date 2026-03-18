#define SNES_HEADER_START 0xC0
#define SNES_HEADER_END 0xE0
#define SNES_HEADER_SIZE SNES_HEADER_END - SNES_HEADER_START
#define ROMSEL_HIGH PORTC |= 0b00000001
#define ROMSEL_LOW PORTC &= 0b11111110
#define READ_HIGH PORTG |= 0b00000010
#define READ_LOW PORTG &= 0b11111101
#define WRITE_HIGH PORTG |= 0b00000001
#define WRITE_LOW PORTG &= 0b11111110
#define A0to7 PORTA
#define A8to15 PORTF
#define A16to23 PORTK
#define D0toD7IN PINL
#define D0toD7OUT PORTL
#define RESET_LOW PORTG &= 0b11111011
#define RESET_HIGH PORTG |= 0b00000100
#define EEPROM_CONTROL_ADDRESS 0x50
#include <Wire.h>
//#include <serialEEPROM.h>
//serialEEPROM myEEPROM(0x50, 128, 16);

void setup() {
  //OUTPUT
  DDRA = 0xFF;
  DDRF = 0xFF;
  DDRK = 0xFF;
  DDRG = 0xFF;
  DDRC = 0xFF;
  //INPUT
  DDRL = 0x00;
  PORTL = 0xFF;
  //Pin /ROMSEL
  WRITE_HIGH;
  ROMSEL_LOW;
  READ_HIGH;
  RESET_HIGH;
  Serial.begin(2000000);
}

void prepSnesRead() {
  DDRL = 0x00;
  PORTL = 0xFF;
  WRITE_HIGH;
  READ_LOW;
  delayMicroseconds(10);
}

void prepSnesWrite() {
  DDRL = 0xFF;
  WRITE_LOW;
  READ_HIGH;
  delayMicroseconds(10);
}

void readHeader(uint8_t buff[], int start, int end, char romType) {
  uint16_t address;
  uint8_t bank = 0x00;
  if (romType == 'L') { address = 0x7F00; }
  else if (romType == 'H') { address = 0xFF00; }
  else { address = 0xFF00; bank = 0x40;}
  prepSnesRead();
  for (uint8_t count = SNES_HEADER_START; count < SNES_HEADER_END; count++) {
    buff[count - SNES_HEADER_START] = readSnesCartridge(bank, address + count);
  }
}

void testDataPins(char romType) {
  uint8_t pinHeadBuff[SNES_HEADER_SIZE];
  readHeader(pinHeadBuff, SNES_HEADER_START, SNES_HEADER_END, romType);
  uint8_t high = 0;
  uint8_t low = 0;
  for (uint8_t i = 0; i < SNES_HEADER_SIZE; i++) {
    high |= pinHeadBuff[i];
    low |= ~(pinHeadBuff[i]);
  }
  Serial.write(low);
  Serial.write(high);
}

byte readSnesCartridge(uint8_t bank, uint16_t address) {
  A16to23 = bank;
  A8to15 = (address >> 8) & 0xFF;
  A0to7 = address & 0xFF;
  delayMicroseconds(3);
  return D0toD7IN;
}

void writeSnesCartridge(uint8_t bank, uint16_t address, uint8_t byte) {
  A16to23 = bank;
  A8to15 = (address >> 8) & 0xFF;
  A0to7 = address & 0xFF;
  D0toD7OUT = byte;
  delayMicroseconds(2);
  WRITE_LOW;
  delayMicroseconds(3);
  WRITE_HIGH;
  delayMicroseconds(2);
}

void dumpSnesSave(uint64_t saveSize, char romLayout) {
  uint8_t buffer[32];
  prepSnesRead();
  switch (romLayout) {  
    case 'L': {
      for (uint32_t x = 0; x < saveSize; x++) {
        uint8_t bank = 0x70 + (x / 0x8000);
        uint16_t address = x % 0x8000;
        buffer[x%32] = readSnesCartridge(bank, address);
        if (x%32 == 31) {
          Serial.write(buffer, 32);
        }
      }
      break;
    }
  }
  Serial.write(buffer, 32);
}

void restoreSnesSave(uint64_t saveSize, char romLayout) {
  uint8_t buffer[32];
  Serial.flush();
  prepSnesWrite();
  switch (romLayout) {  
    case 'L': {
      for (uint32_t x = 0; x < saveSize; x++) {
        if ((x)%32 == 0) {
          Serial.write('M');
          while (Serial.available() < 32) {}
          Serial.readBytes(buffer, 32);
          Serial.write('K');
        }
        uint8_t bank = 0x70 + (x / 0x8000);
        uint16_t address = x % 0x8000;
        writeSnesCartridge(bank, address, buffer[x%32]);
      }
      break;
    }
  }
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
        char data[8];
        //myEEPROM.read(0x00, (uint8_t*)data, 8);
        Serial.write(data, 8);
        break;
      }
      case 0x03:{
        char dataSet[8] = {'S','N','E','S',' ',' ',' ',' '};
        //myEEPROM.write(0x00, (uint8_t*)dataSet, 8);
        break;
      }
      case 0x11:{
        uint8_t buffer[64];
        readHeader(buffer, SNES_HEADER_START, SNES_HEADER_END, 'H');
        Serial.write(buffer, SNES_HEADER_SIZE);
        break;}
      case 0x12:{
        uint8_t header[64];
        readHeader(header, SNES_HEADER_START, SNES_HEADER_END, 'H');
        uint8_t headerCheck[64];
        readHeader(headerCheck, SNES_HEADER_START, SNES_HEADER_END, 'L');
        boolean loRom = true;
        for (uint8_t count = 0; count < SNES_HEADER_SIZE && loRom; count++) {
          loRom = header[count] == headerCheck[count];
        }
        if (loRom) {Serial.write('L');}
        else {
          readHeader(headerCheck, SNES_HEADER_START, SNES_HEADER_END, 'X');
          boolean exHiRom = true;
          for (uint8_t count = 0; count < SNES_HEADER_SIZE && exHiRom; count++) {
            exHiRom = header[count] == headerCheck[count];
          }
          if (exHiRom) {Serial.write('X');}
          else {Serial.write('H');}
        }
        break;}
      case 0x20:{
        testDataPins('H');
        break;}
      case 0x40:{
        while(Serial.available() < 2){}
        uint8_t ramPow = Serial.read();
        char romType = Serial.read();
        uint64_t ramSize = 1024 * pow(2, ramPow);
        dumpSnesSave(ramSize, romType);
        break;
      }
      case 0x41:{
        while(Serial.available() < 2){}
        uint8_t ramPow = Serial.read();
        char romType = Serial.read();
        uint64_t ramSize = 1024 * pow(2, ramPow);
        prepSnesWrite();
        restoreSnesSave(ramSize, romType);
        break;
      }
      case 0x42:{
        char dataSet[8] = {'S', 'N', 'E', 'S', 'T', 'E', 'S', 'T'};
        prepSnesWrite();
        for (uint16_t i = 0x00; i < 0x08; i++) {
          writeSnesCartridge(0x70, i, dataSet[i]);
        }
        break;
      }
    }
  }
}
