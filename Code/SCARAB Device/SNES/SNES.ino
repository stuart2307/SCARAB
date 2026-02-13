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
#define D0to7 PINL
#define RESET_LOW PORTG &= 0b11111011
#define RESET_HIGH PORTG |= 0b00000100
#define EEPROM_CONTROL_ADDRESS 0x50
#include <Wire.h>
#include <serialEEPROM.h>

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

void readHeader(uint8_t buff[], int start, int end, char romType) {
  uint8_t high = 0x00;
  uint8_t mid = 0x00;
  if (romType == 'L') { mid = 0x7F; }
  else if (romType == 'H') { mid = 0xFF; }
  else { mid = 0xFF; high = 0x40; }
  for (uint8_t count = SNES_HEADER_START; count < SNES_HEADER_END; count++) {
    A16to23 = high;
    A8to15 = mid;
    A0to7 = count;
    delayMicroseconds(10);
    READ_LOW;
    delayMicroseconds(2);
    uint8_t val = D0to7;
    READ_HIGH;
    delayMicroseconds(5);
    buff[count - 0xC0] = val;
    
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
        serialEEPROM myEEPROM(0x50, 128, 16);
        myEEPROM.read(0x00, data, 8);
        Serial.write(data, 8);
        break;
      }
      case 0x03:{
        char dataSet[8] = {'S','N','E','S',' ',' ',' ',' '};
        serialEEPROM myEEPROM(0x50, 128, 16);
        myEEPROM.write(0x00, (uint8_t*)dataSet, 8);
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
        char type = Serial.read();
        testDataPins(type);
        break;}
    }
  }
}
