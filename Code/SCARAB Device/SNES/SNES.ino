#define SNES_HEADER_START 0xC0
#define SNES_HEADER_END 0xE0
#define SNES_HEADER_SIZE SNES_HEADER_END - SNES_HEADER_START
#define SNES_ROMSEL_HIGH PORTC |= 0b00000001
#define SNES_ROMSEL_LOW PORTC &= 0b11111110
#define SNES_READ_HIGH PORTG |= 0b00000010
#define SNES_READ_LOW PORTG &= 0b11111101
#define SNES_WRITE_HIGH PORTG |= 0b00000001
#define SNES_WRITE_LOW PORTG &= 0b11111110
#define SNES_A0to7 PORTA
#define SNES_A8to15 PORTF
#define SNES_A16to23 PORTK
#define SNES_D0toD7IN PINL
#define SNES_D0toD7OUT PORTL
#define SNES_RESET_LOW PORTG &= 0b11111011
#define SNES_RESET_HIGH PORTG |= 0b00000100
#define NOP __asm__ __volatile__("nop\n\t")

void snes_setup() {
  //OUTPUT
  DDRA = 0xFF;
  DDRF = 0xFF;
  DDRK = 0xFF;
  DDRG = 0xFF;
  DDRC = 0xFF;
  //INPUT
  DDRL = 0x00;
  PORTL = 0xFF;
  SNES_WRITE_HIGH;
  SNES_ROMSEL_LOW;
  SNES_READ_HIGH;
  SNES_RESET_HIGH;
}

void prepSnesRead() {
  DDRL = 0x00;
  SNES_WRITE_HIGH;
  SNES_READ_LOW;
  delayMicroseconds(10);
}

void prepSnesWrite() {
  DDRL = 0xFF;
  SNES_WRITE_LOW;
  SNES_READ_HIGH;
  delayMicroseconds(10);
}

void readSnesHeader(uint8_t buff[], int start, int end, char romType) {
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

void testDataPinsSnes(char romType) {
  uint8_t pinHeadBuff[SNES_HEADER_SIZE];
  readSnesHeader(pinHeadBuff, SNES_HEADER_START, SNES_HEADER_END, romType);
  uint8_t high = 0;
  uint8_t low = 0;
  for (uint8_t i = 0; i < SNES_HEADER_SIZE; i++) {
    high |= pinHeadBuff[i];
    low |= ~(pinHeadBuff[i]);
  }
  Serial.write(low);
  Serial.write(high);
}

uint16_t calcSnesChecksum(uint64_t romSize, char romLayout) {
  prepSnesRead();
  uint16_t crc = 0x0000;
  switch(romLayout) {
    case 'L': {
      for (uint64_t x = 0; x < romSize; x++) {
        uint8_t bank = (x / 0x8000) + 0x80;
        uint16_t address = (x % 0x8000) + 0x8000;
        crc += readSnesCartridge(bank, address);
      }
      break;
    }
  }
  return crc;
}

byte readSnesCartridge(uint8_t bank, uint16_t address) {
  SNES_A0to7 = address & 0xFF;
  SNES_A8to15 = (address >> 8) & 0xFF;
  SNES_A16to23 = bank;
  NOP;
  NOP;
  NOP;
  NOP;
  NOP;
  NOP;
  byte temp = SNES_D0toD7IN;
  return temp;
}

void writeSnesCartridge(uint8_t bank, uint16_t address, uint8_t byte) {
  SNES_A16to23 = bank;
  SNES_A8to15 = (address >> 8) & 0xFF;
  SNES_A0to7 = address & 0xFF;
  SNES_D0toD7OUT = byte;
  delayMicroseconds(1);
  SNES_WRITE_LOW;
  NOP;
  NOP;
  NOP;
  NOP;
  NOP;
  NOP;
  SNES_WRITE_HIGH;
  delayMicroseconds(1);
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