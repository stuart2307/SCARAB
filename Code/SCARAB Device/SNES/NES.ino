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
#define NOP __asm__ __volatile__("nop\n\t")

void nes_setup() {
  DDRF = 0xFF;   //PRG low address
  DDRC = 0xFF;   //PRG high address
  DDRK = 0xFF;   //CHR low address
  DDRL = 0xFF;   //CHR high address
  DDRA = 0x00;   //PRG data
  DDRB = 0x00;   //CHR data
  DDRH = 0xFF;   //Control

  NES_CPU_RW_READ;
  NES_CHAR_READ_HIGH;
  NES_CHAR_WRITE_HIGH;
  NES_ROMSEL_HIGH;

  Serial.begin(2000000);
  Wire.begin();
  Wire.setWireTimeout(1000, true);
}

void prepPrgRead() {
  DDRA = 0x00;
  NES_CPU_RW_READ;
  delayMicroseconds(10);
}

void prepPrgWrite() {
  DDRA = 0xFF;
  NES_CPU_RW_WRITE;
  delayMicroseconds(10);
}

void prepChrRead() {
  DDRB = 0x00;
  NES_CHAR_WRITE_HIGH;
  NES_CHAR_READ_LOW;
  delayMicroseconds(10);
}

uint8_t readPrg(uint16_t address) {
  NES_PRG_LOW_ADD = address & 0xFF;
  NES_PRG_UPP_ADD = (address >> 8) & 0xFF;
  NOP;NOP;NOP;NOP;NOP;NOP;
  return NES_PRG_DATA;
}

void writePrg(uint16_t address, uint8_t data) {
  NES_PRG_LOW_ADD = address & 0xFF;
  NES_PRG_UPP_ADD = (address >> 8) & 0xFF;
  PORTA = data;
  NOP;NOP;NOP;NOP;NOP;NOP;
  NOP;NOP;NOP;NOP;NOP;NOP;
  delayMicroseconds(1);
}

uint8_t readChr(uint16_t address) {
  NES_CHAR_LOW_ADD = address & 0xFF;
  NES_CHAR_UPP_ADD = (address >> 8) & 0xFF;
  NOP;NOP;NOP;NOP;NOP;NOP;
  return NES_CHAR_DATA;
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

void dumpPrgRom(uint8_t mapper, uint8_t banks) {
  uint8_t buffer[64];
  switch (mapper) {

    case 0: { //NROM
      prepPrgRead();
      NES_ROMSEL_LOW;
      uint32_t size = (uint32_t)banks * 0x4000;
      for (uint32_t x = 0; x < size; x++) {
        buffer[x % 64] = readPrg(0x8000 + (x & 0x7FFF));
        if (x % 64 == 63) Serial.write(buffer, 64);
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
          if (x % 64 == 63) Serial.write(buffer, 64);
        }
        NES_ROMSEL_HIGH;
      }
      prepPrgRead();
      NES_ROMSEL_LOW;
      for (uint16_t x = 0; x < 0x4000; x++) {
        buffer[x % 64] = readPrg(0xC000 + x);
        if (x % 64 == 63) Serial.write(buffer, 64);
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
          if (x % 64 == 63) Serial.write(buffer, 64);
        }
        NES_ROMSEL_HIGH;
      }
      prepPrgRead();
      NES_ROMSEL_LOW;
      for (uint16_t x = 0; x < 0x2000; x++) {
        buffer[x % 64] = readPrg(0xE000 + x);
        if (x % 64 == 63) Serial.write(buffer, 64);
      }
      NES_ROMSEL_HIGH;
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
        if (x % 64 == 63) Serial.write(buffer, 64);
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
          buffer[x % 64] = readChr(x);
          if (x % 64 == 63) Serial.write(buffer, 64);
        }
      }
      break;
    }

    case 3: { //MMC3
      for (uint8_t bank = 0; bank < banks; bank++) {
        uint8_t regIndex = (bank < 4) ? (bank / 2) : (bank - 2);
        mmc3SelectBank(regIndex, bank);
        prepChrRead();
        uint16_t baseAddr = (uint16_t)bank * 0x0400;
        for (uint16_t x = 0; x < 0x0400; x++) {
          buffer[x % 64] = readChr(baseAddr + x);
          if (x % 64 == 63) Serial.write(buffer, 64);
        }
      }
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

    case 3: { // MMC3
      for (uint8_t bank = 0; bank < banks; bank++) {
        uint8_t regIndex = (bank < 4) ? (bank / 2) : (bank - 2);
        mmc3SelectBank(regIndex, bank);
        prepChrRead();
        uint16_t baseAddr = (uint16_t)bank * 0x0400;
        for (uint16_t x = 0; x < 0x0400; x++) {
          uint8_t val = readChr(baseAddr + x);
          high |= val;
          low |= ~val;
        }
      }
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

    case 3: { //MMC3
      for (uint8_t bank = 0; bank < banks; bank++) {
        uint8_t regIndex = (bank < 4) ? (bank / 2) : (bank - 2);
        mmc3SelectBank(regIndex, bank);
        prepChrRead();
        uint16_t baseAddr = (uint16_t)bank * 0x0400;
        for (uint16_t x = 0; x < 0x0400; x++) {
          crc = crc32Update(crc, readChr(baseAddr + x));
        }
      }
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

void eeprom_write_page(byte deviceaddress, uint8_t eeaddr, const byte* data, byte length) {
  Wire.beginTransmission(deviceaddress);
  Wire.write(int(eeaddr));
  for (int i = 0; i < length; i++) Wire.write(data[i]);
  Wire.endTransmission();
  delay(1);
}

int eeprom_read_buffer(byte deviceaddr, uint8_t eeaddr, byte* buffer, byte length) {
  Wire.beginTransmission(deviceaddr);
  Wire.write(int(eeaddr));
  Wire.endTransmission(false);
  Wire.requestFrom(deviceaddr, length);
  int i;
  for (i = 0; i < length && Wire.available(); i++) buffer[i] = Wire.read();
  return i;
}

void loop() {
  if (Serial.available() > 0) {
    uint8_t op = Serial.read();
    switch (op) {
      case 0x01: {
        Serial.print("SCARAB");
        break;
      }

      case 0x02: {
        byte myBuff[8];
        eeprom_read_buffer(EEPROM_CONTROL_ADDRESS, 0x00, myBuff, 0x08);
        Serial.write(myBuff, 8);
        break;
      }

      case 0x03: {
        byte myBuff[8];
        while (Serial.available() < 8) {}
        for (int i = 0; i < 8; i++) myBuff[i] = Serial.read();
        eeprom_write_page(EEPROM_CONTROL_ADDRESS, 0x00, myBuff, 0x08);
        Serial.println("OK");
        break;
      }

      case 0x20: {
        while (Serial.available() < 2) {}
        uint8_t mapper = Serial.read();
        uint8_t banks = Serial.read();
        testPrgDataPins(mapper, banks);
        break;
      }
      case 0x21: {
        while (Serial.available() < 2) {}
        uint8_t mapper = Serial.read();
        uint8_t banks = Serial.read();
        testChrDataPins(mapper, banks);
        break;
      }

      case 0x30: {
        while (Serial.available() < 2) {}
        uint8_t mapper = Serial.read();
        uint8_t banks = Serial.read();
        uint32_t crc = calcPrgCrc32(mapper, banks);
        Serial.write((crc >> 24) & 0xFF);
        Serial.write((crc >> 16) & 0xFF);
        Serial.write((crc >>  8) & 0xFF);
        Serial.write(crc & 0xFF);
        break;
      }

      case 0x31: {
        while (Serial.available() < 2) {}
        uint8_t mapper = Serial.read();
        uint8_t banks = Serial.read();
        uint32_t crc = calcChrCrc32(mapper, banks);
        Serial.write((crc >> 24) & 0xFF);
        Serial.write((crc >> 16) & 0xFF);
        Serial.write((crc >>  8) & 0xFF);
        Serial.write(crc & 0xFF);
        break;
      }

      case 0x40: {
        while (Serial.available() < 2) {}
        uint8_t mapper = Serial.read();
        uint8_t banks = Serial.read();
        dumpPrgRom(mapper, banks);
        break;
      }

      case 0x41: {
        while (Serial.available() < 2) {}
        uint8_t mapper = Serial.read();
        uint8_t banks = Serial.read();
        dumpChrRom(mapper, banks);
        break;
      }

      case 0x50: {
        dumpNesSave();
        break;
      }

      case 0x51: {
        restoreNesSave();
        break;
      }
    }
  }
}
