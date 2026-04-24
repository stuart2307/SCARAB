#define NES_PRG_DATA PINA
#define NES_PRG_LOW_ADD PORTF
#define NES_PRG_UPP_ADD PORTC
#define NES_CHAR_DATA PINB
#define NES_CHAR_LOW_ADD PORTK
#define NES_CHAR_UPP_ADD PORTL
#define NES_CPU_RW_READ PORTH |= 0b00001000
#define NES_CPU_RW_WRITE PORTH &= 0b11110111
#define NES_CHAR_READ_LOW PORTH &= 0b11101111
#define NES_CHAR_READ_HIGH PORTH |= 0b00010000
#define NES_CHAR_WRITE_LOW PORTH &= 0b11011111
#define NES_CHAR_WRITE_HIGH PORTH |= 0b00100000
#define NES_ROMSEL_LOW PORTH &= 0b10111111
#define NES_ROMSEL_HIGH PORTH |= 0b01000000
#define NES_M2_LOW  PORTG &= 0b11111100
#define NES_M2_HIGH PORTG |= 0b00000011
#define NOP __asm__ __volatile__("nop\n\t")

void nes_setup() {
  DDRF = 0xFF;   //PRG low address
  DDRC = 0xFF;   //PRG high address
  DDRK = 0xFF;   //CHR low address
  DDRL = 0xFF;   //CHR high address
  DDRA = 0x00;   //PRG data
  DDRB = 0x00;   //CHR data
  DDRH = 0xFF;   //Control
  DDRG |= 0b00000011;  // G0 as output
  
  NES_M2_LOW;
  NES_CPU_RW_READ;
  NES_CHAR_READ_HIGH;
  NES_CHAR_WRITE_HIGH;
  NES_ROMSEL_HIGH;
  delay(1);
}

void prepPrgRead() {
  DDRA = 0x00;
  NES_CPU_RW_READ;
  delayMicroseconds(10);
}

void prepPrgWrite() {
  DDRA = 0xFF;
  delayMicroseconds(10);
}

void prepChrRead() {
  DDRB = 0x00;
  NES_CHAR_WRITE_HIGH;
  NES_CHAR_READ_LOW;
  delayMicroseconds(10);
}

void setRomsel(unsigned int address) {
  if (address & 0x8000) {
    NES_ROMSEL_LOW;
  } else {
    NES_ROMSEL_HIGH;
  }
}

uint8_t readPrg(uint16_t address) {
  prepPrgRead();
  NES_CPU_RW_READ;
  NES_ROMSEL_HIGH;
  NES_PRG_LOW_ADD = address & 0xFF;
  NES_PRG_UPP_ADD = (address >> 8) & 0xFF;
  delayMicroseconds(1);
  
  NES_M2_HIGH;
  setRomsel(address);
  uint8_t data = NES_PRG_DATA;
  return data;
}

void writePrg(uint16_t address, uint8_t data) {
  NES_M2_LOW;
  NES_ROMSEL_HIGH;
  prepPrgWrite();
  NES_CPU_RW_WRITE;
  PORTA = data;

  NES_PRG_LOW_ADD = address & 0xFF;
  NES_PRG_UPP_ADD = (address >> 8) & 0xFF;
  NES_M2_HIGH;
  setRomsel(address);
  delayMicroseconds(1);
  NES_M2_LOW;
  NES_ROMSEL_HIGH;

  NES_CPU_RW_READ;
  prepPrgRead();
  NES_CPU_RW_READ;
  NES_PRG_LOW_ADD = 0;
  NES_PRG_UPP_ADD = 0;
  NES_M2_HIGH;
}

uint8_t readChr(uint16_t address) {
  prepChrRead();
  NES_M2_HIGH;
  NES_ROMSEL_HIGH; 
  NES_CHAR_LOW_ADD = address & 0xFF;
  NES_CHAR_UPP_ADD = (address >> 8) & 0xFF;
  NES_CHAR_READ_LOW;
  delayMicroseconds(1);
  uint8_t data = NES_CHAR_DATA;
  NES_CHAR_READ_HIGH;
  return data;
}

void mmc1Reset() {
  prepPrgWrite();
  NES_ROMSEL_LOW;
  writePrg(0x8000, 0x80);
  NES_ROMSEL_HIGH;
  delayMicroseconds(10);
}

void mmc1WriteReg(uint16_t address, uint8_t value) {
  prepPrgWrite();
  NES_ROMSEL_LOW;
  for (uint8_t i = 0; i < 5; i++) {
    writePrg(address, (value >> i) & 0x01);
    delayMicroseconds(2);
  }
  NES_ROMSEL_HIGH;
  delayMicroseconds(10);
}

void mmc3SelectBank(uint8_t reg, uint8_t bank) {
  prepPrgWrite();
  NES_ROMSEL_LOW;
  writePrg(0x8000, reg);
  delayMicroseconds(2);
  writePrg(0x8001, bank);
  NES_ROMSEL_HIGH;
  delayMicroseconds(2);
}

void unromSelectBank(uint8_t bank) {
  prepPrgWrite();
  NES_ROMSEL_LOW;
  writePrg(0x8000, bank);
  NES_ROMSEL_HIGH;
  delayMicroseconds(10);
}

void cnromSelectBank(uint8_t bank) {
  prepPrgWrite();
  NES_ROMSEL_LOW;
  writePrg(0x8000, bank);
  NES_ROMSEL_HIGH;
  delayMicroseconds(10);
}

void aoromSelectBank(uint8_t bank) {
  prepPrgWrite();
  NES_ROMSEL_LOW;
  writePrg(0x8000, bank & 0x07); // bits 0-2 = PRG bank, bit 4 = mirroring (not needed for dumping)
  NES_ROMSEL_HIGH;
  delayMicroseconds(10);
}

void dumpPrgRom(uint8_t mapper, uint8_t banks) {
  uint8_t buffer[64];
  switch (mapper) {

    case 0: { //NROM
      prepPrgRead();
      NES_ROMSEL_LOW;
      uint32_t size = (uint32_t)banks * 0x4000;
      for (uint32_t x = 0; x < size; x++) {
        buffer[x % 64] = readPrg(0x8000 + (x & 0x7FFF));
        if (x % 64 == 63) {
          Serial.write(buffer, 64);
          while (Serial.available() < 1) {}
          Serial.read();
        }
      }
      NES_ROMSEL_HIGH;
      break;
    }

    case 1: { //MMC1
      mmc1Reset();
      mmc1WriteReg(0x8000, 0x0C);
      for (uint8_t bank = 0; bank < banks - 1; bank++) {
        mmc1WriteReg(0xE000, bank);
        prepPrgRead();
        NES_ROMSEL_LOW;
        for (uint16_t x = 0; x < 0x4000; x++) {
          buffer[x % 64] = readPrg(0x8000 + x);
          if (x % 64 == 63) {
            Serial.write(buffer, 64);
            while (Serial.available() < 1) {}
            Serial.read();
          }
        }
        NES_ROMSEL_HIGH;
      }
      prepPrgRead();
      NES_ROMSEL_LOW;
      for (uint16_t x = 0; x < 0x4000; x++) {
        buffer[x % 64] = readPrg(0xC000 + x);
        if (x % 64 == 63) {
          Serial.write(buffer, 64);
          while (Serial.available() < 1) {}
          Serial.read();
        }
      }
      NES_ROMSEL_HIGH;
      break;
    }

    case 2: { //UNROM — swappable first 16KB, fixed last 16KB
      for (uint8_t bank = 0; bank < banks - 1; bank++) {
        unromSelectBank(bank);
        prepPrgRead();
        NES_ROMSEL_LOW;
        for (uint16_t x = 0; x < 0x4000; x++) {
          buffer[x % 64] = readPrg(0x8000 + x);
          if (x % 64 == 63) {
            Serial.write(buffer, 64);
            while (Serial.available() < 1) {}
            Serial.read();
          }
        }
        NES_ROMSEL_HIGH;
      }
      // Last bank is fixed at $C000, always visible — no bank switch needed
      prepPrgRead();
      NES_ROMSEL_LOW;
      for (uint16_t x = 0; x < 0x4000; x++) {
        buffer[x % 64] = readPrg(0xC000 + x);
        if (x % 64 == 63) {
          Serial.write(buffer, 64);
          while (Serial.available() < 1) {}
          Serial.read();
        }
      }
      NES_ROMSEL_HIGH;
      break;
    }

    case 3: { //MMC3
      for (uint8_t bank = 0; bank < banks - 1; bank++) {
        mmc3SelectBank(0x06, bank);
        prepPrgRead();
        NES_ROMSEL_LOW;
        for (uint16_t x = 0; x < 0x2000; x++) {
          buffer[x % 64] = readPrg(0x8000 + x);
          if (x % 64 == 63) {
            Serial.write(buffer, 64);
            while (Serial.available() < 1) {}
            Serial.read();
          }
        }
        NES_ROMSEL_HIGH;
      }
      prepPrgRead();
      NES_ROMSEL_LOW;
      for (uint16_t x = 0; x < 0x2000; x++) {
        buffer[x % 64] = readPrg(0xE000 + x);
        if (x % 64 == 63) {
          Serial.write(buffer, 64);
          while (Serial.available() < 1) {}
          Serial.read();
        }
      }
      NES_ROMSEL_HIGH;
      break;
    }

    case 7: { //AOROM — full 32KB swap
      for (uint8_t bank = 0; bank < banks; bank++) {
        aoromSelectBank(bank);
        prepPrgRead();
        NES_ROMSEL_LOW;
        for (uint16_t x = 0; x < 0x8000; x++) {
          buffer[x % 64] = readPrg(0x8000 + x);
          if (x % 64 == 63) {
            Serial.write(buffer, 64);
            while (Serial.available() < 1) {}
            Serial.read();
          }
        }
        NES_ROMSEL_HIGH;
      }
      break;
    }
  }
}

void dumpChrRom(uint8_t mapper, uint8_t banks) {
  uint8_t buffer[64];
  switch (mapper) {

    case 0: { //NROM
      prepChrRead();
      uint32_t size = (uint32_t)banks * 0x2000;
      for (uint32_t x = 0; x < size; x++) {
        buffer[x % 64] = readChr(x & 0x1FFF);
        if (x % 64 == 63) {
          Serial.write(buffer, 64);
          while (Serial.available() < 1) {}
          Serial.read();
        }
      }
      break;
    }

    case 1: { //MMC1
      mmc1Reset();
      mmc1WriteReg(0x8000, 0x00);
      for (uint8_t bank = 0; bank < banks; bank += 2) {
        mmc1WriteReg(0xA000, bank);
        prepChrRead();
        for (uint16_t x = 0; x < 0x2000; x++) {
          buffer[x % 64] = readChr(x);
          if (x % 64 == 63) {
            Serial.write(buffer, 64);
            while (Serial.available() < 1) {}
            Serial.read();
          }
        }
      }
      break;
    }

    case 2: { //UNROM — CHR-RAM, nothing to dump
      // No CHR ROM; caller should not invoke this for UNROM
      break;
    }

    case 3: { //CNROM — full CHR bank swap, each bank is 8KB
      for (uint8_t bank = 0; bank < banks; bank++) {
        cnromSelectBank(bank);
        prepChrRead();
        for (uint16_t x = 0; x < 0x2000; x++) {
          buffer[x % 64] = readChr(x);
          if (x % 64 == 63) {
            Serial.write(buffer, 64);
            while (Serial.available() < 1) {}
            Serial.read();
          }
        }
      }
      break;
    }

    // Note: MMC3 was formerly case 3 — you'll need to renumber it.
    // See note below about the mapper numbering conflict.

    case 7: { //AOROM — CHR-RAM, nothing to dump
      break;
    }
  }
}

void testPrgDataPins(uint8_t mapper, uint8_t banks) {
  uint8_t high = 0x00;
  uint8_t low  = 0x00;
  switch (mapper) {

    case 0: { //NROM
      prepPrgRead();
      NES_ROMSEL_LOW;
      uint32_t size = (uint32_t)banks * 0x4000;
      for (uint32_t x = 0; x < size; x++) {
        uint8_t val = readPrg(0x8000 + (x & 0x7FFF));
        high |= val;
        low  |= ~val;
      }
      NES_ROMSEL_HIGH;
      break;
    }

    case 1: { //MMC1
      mmc1Reset();
      mmc1WriteReg(0x8000, 0x0C);
      for (uint8_t bank = 0; bank < banks; bank++) {
        mmc1WriteReg(0xE000, bank);
        prepPrgRead();
        NES_ROMSEL_LOW;
        for (uint16_t x = 0; x < 0x4000; x++) {
          uint8_t val = readPrg(0x8000 + x);
          high |= val;
          low  |= ~val;
        }
        NES_ROMSEL_HIGH;
      }
      break;
    }

    case 2: { //UNROM
      for (uint8_t bank = 0; bank < banks - 1; bank++) {
        unromSelectBank(bank);
        prepPrgRead();
        NES_ROMSEL_LOW;
        for (uint16_t x = 0; x < 0x4000; x++) {
          uint8_t val = readPrg(0x8000 + x);
          high |= val;
          low  |= ~val;
        }
        NES_ROMSEL_HIGH;
      }
      prepPrgRead();
      NES_ROMSEL_LOW;
      for (uint16_t x = 0; x < 0x4000; x++) {
        uint8_t val = readPrg(0xC000 + x);
        high |= val;
        low  |= ~val;
      }
      NES_ROMSEL_HIGH;
      break;
    }

    case 3: { //MMC3
      for (uint8_t bank = 0; bank < banks; bank++) {
        mmc3SelectBank(0x06, bank);
        prepPrgRead();
        NES_ROMSEL_LOW;
        for (uint16_t x = 0; x < 0x2000; x++) {
          uint8_t val = readPrg(0x8000 + x);
          high |= val;
          low |= ~val;
        }
        NES_ROMSEL_HIGH;
      }
      break;
    }

    case 7: { //AOROM
      for (uint8_t bank = 0; bank < banks; bank++) {
        aoromSelectBank(bank);
        prepPrgRead();
        NES_ROMSEL_LOW;
        for (uint16_t x = 0; x < 0x8000; x++) {
          uint8_t val = readPrg(0x8000 + x);
          high |= val;
          low  |= ~val;
        }
        NES_ROMSEL_HIGH;
      }
      break;
    }
  }
  Serial.write(low);
  Serial.write(high);
}
void testChrDataPins(uint8_t mapper, uint8_t banks) {
  uint8_t high = 0x00;
  uint8_t low  = 0x00;
  switch (mapper) {

    case 0: { // NROM
      prepChrRead();
      uint32_t size = (uint32_t)banks * 0x2000;
      for (uint32_t x = 0; x < size; x++) {
        uint8_t val = readChr(x & 0x1FFF);
        high |= val;
        low |= ~val;
      }
      break;
    }

    case 1: { // MMC1
      mmc1Reset();
      mmc1WriteReg(0x8000, 0x0C);
      for (uint8_t bank = 0; bank < banks; bank++) {
        mmc1WriteReg(0xA000, bank);
        prepChrRead();
        for (uint16_t x = 0; x < 0x1000; x++) {
          uint8_t val = readChr(x);
          high |= val;
          low |= ~val;
        }
      }
      break;
    }

    case 2: { // UNROM — CHR-RAM, skip
      break;
    }

    case 3: { // CNROM
      for (uint8_t bank = 0; bank < banks; bank++) {
        cnromSelectBank(bank);
        prepChrRead();
        for (uint16_t x = 0; x < 0x2000; x++) {
          uint8_t val = readChr(x);
          high |= val;
          low |= ~val;
        }
      }
      break;
    }

    case 7: { // AOROM — CHR-RAM, skip
      break;
    }
  }
  Serial.write(low);
  Serial.write(high);
}

static const uint32_t crc32Table[16] = {
  0x00000000, 0x1DB71064, 0x3B6E20C8, 0x26D930AC,
  0x76DC4190, 0x6B6B51F4, 0x4DB26158, 0x5005713C,
  0xEDB88320, 0xF00F9344, 0xD6D6A3E8, 0xCB61B38C,
  0x9B64C2B0, 0x86D3D2D4, 0xA00AE278, 0xBDBDF21C
};

uint32_t crc32Update(uint32_t crc, uint8_t data) {
  crc ^= data;
  crc = (crc >> 4) ^ crc32Table[crc & 0x0F];
  crc = (crc >> 4) ^ crc32Table[crc & 0x0F];
  return crc;
}

uint32_t calcPrgCrc32(uint8_t mapper, uint8_t banks) {
  uint32_t crc = 0xFFFFFFFF;
  switch (mapper) {

    case 0: { //NROM
      prepPrgRead();
      NES_ROMSEL_LOW;
      uint32_t size = (uint32_t)banks * 0x4000;
      for (uint32_t x = 0; x < size; x++) {
        crc = crc32Update(crc, readPrg(0x8000 + (x & 0x7FFF)));
      }
      NES_ROMSEL_HIGH;
      break;
    }

    case 1: { //MMC1
      mmc1Reset();
      mmc1WriteReg(0x8000, 0x0C);
      for (uint8_t bank = 0; bank < banks - 1; bank++) {
        mmc1WriteReg(0xE000, bank);
        prepPrgRead();
        NES_ROMSEL_LOW;
        for (uint16_t x = 0; x < 0x4000; x++) {
          crc = crc32Update(crc, readPrg(0x8000 + x));
        }
        NES_ROMSEL_HIGH;
      }
      prepPrgRead();
      NES_ROMSEL_LOW;
      for (uint16_t x = 0; x < 0x4000; x++) {
        crc = crc32Update(crc, readPrg(0xC000 + x));
      }
      NES_ROMSEL_HIGH;
      break;
    }

    case 2: { //UNROM
      for (uint8_t bank = 0; bank < banks - 1; bank++) {
        unromSelectBank(bank);
        prepPrgRead();
        NES_ROMSEL_LOW;
        for (uint16_t x = 0; x < 0x4000; x++) {
          crc = crc32Update(crc, readPrg(0x8000 + x));
        }
        NES_ROMSEL_HIGH;
      }
      prepPrgRead();
      NES_ROMSEL_LOW;
      for (uint16_t x = 0; x < 0x4000; x++) {
        crc = crc32Update(crc, readPrg(0xC000 + x));
      }
      NES_ROMSEL_HIGH;
      break;
    }

    case 3: { //MMC3
      for (uint8_t bank = 0; bank < banks - 1; bank++) {
        mmc3SelectBank(0x06, bank);
        prepPrgRead();
        NES_ROMSEL_LOW;
        for (uint16_t x = 0; x < 0x2000; x++) {
          crc = crc32Update(crc, readPrg(0x8000 + x));
        }
        NES_ROMSEL_HIGH;
      }
      prepPrgRead();
      NES_ROMSEL_LOW;
      for (uint16_t x = 0; x < 0x2000; x++) {
        crc = crc32Update(crc, readPrg(0xE000 + x));
      }
      NES_ROMSEL_HIGH;
      break;
    }

    case 7: { //AOROM
      for (uint8_t bank = 0; bank < banks; bank++) {
        aoromSelectBank(bank);
        prepPrgRead();
        NES_ROMSEL_LOW;
        for (uint16_t x = 0; x < 0x8000; x++) {
          crc = crc32Update(crc, readPrg(0x8000 + x));
        }
        NES_ROMSEL_HIGH;
      }
      break;
    }
  }
  return ~crc;
}

uint32_t calcChrCrc32(uint8_t mapper, uint8_t banks) {
  uint32_t crc = 0xFFFFFFFF;
  switch (mapper) {

    case 0: { //NROM
      prepChrRead();
      uint32_t size = (uint32_t)banks * 0x2000;
      for (uint32_t x = 0; x < size; x++) {
        crc = crc32Update(crc, readChr(x & 0x1FFF));
      }
      break;
    }

    case 1: { //MMC1
      mmc1Reset();
      mmc1WriteReg(0x8000, 0x0C);
      for (uint8_t bank = 0; bank < banks; bank++) {
        mmc1WriteReg(0xA000, bank);
        prepChrRead();
        for (uint16_t x = 0; x < 0x1000; x++) {
          crc = crc32Update(crc, readChr(x));
        }
      }
      break;
    }

    case 2: { //UNROM — no CHR ROM
      break;
    }

    case 3: { //CNROM
      for (uint8_t bank = 0; bank < banks; bank++) {
        cnromSelectBank(bank);
        prepChrRead();
        for (uint16_t x = 0; x < 0x2000; x++) {
          crc = crc32Update(crc, readChr(x));
        }
      }
      break;
    }

    case 7: { //AOROM — no CHR ROM
      break;
    }
  }
  return ~crc;
}

void dumpNesSave() {
  uint8_t buffer[64];
  prepPrgRead();
  NES_ROMSEL_LOW;
  for (uint16_t x = 0; x < 0x2000; x++) {
    buffer[x % 64] = readPrg(0x6000 + x);
    if (x % 64 == 63) Serial.write(buffer, 64);
  }
  NES_ROMSEL_HIGH;
}

void restoreNesSave() {
  uint8_t buffer[64];
  Serial.flush();
  prepPrgWrite();
  NES_ROMSEL_LOW;
  for (uint16_t x = 0; x < 0x2000; x++) {
    if (x % 64 == 0) {
      Serial.write('M');
      while (Serial.available() < 64) {}
      Serial.readBytes(buffer, 64);
      Serial.write('K');
    }
    writePrg(0x6000 + x, buffer[x % 64]);
  }
  NES_ROMSEL_HIGH;
}
