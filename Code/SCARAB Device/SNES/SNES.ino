#define SNES_HEADER_START 0xC0
#define SNES_HEADER_END 0xE0
#define SNES_HEADER_SIZE SNES_HEADER_END - SNES_HEADER_START
#define ROMSEL 10
#define READ 11
#define WRITE 12
#define PIN_TEST_COUNT 200

void setup() {
  //Port F: A0-A7, OUTPUT
  DDRF = 0xFF;
  //Port K: A8-A15, OUTPUT
  DDRK = 0xFF;
  //Port L: D49-D42, OUTPUT
  DDRL = 0xFF;
  //Port C: D37-D30, INPUT
  DDRC = 0x00;
  //Port A: D22-D29, INPUT
  DDRA = 0x00;
  //Pin /ROMSEL
  pinMode(ROMSEL, OUTPUT);
  //Pin /RD
  pinMode(READ, OUTPUT);
  //Pin /WR
  pinMode(WRITE, OUTPUT);
  digitalWrite(WRITE, HIGH);
  digitalWrite(ROMSEL, LOW);
  digitalWrite(READ, HIGH);
  Serial.begin(2000000);
}

void readHeader(uint8_t buff[], int start, int end, char romType) {
  uint8_t high = 0x00;
  uint8_t mid = 0x00;
  if (romType == 'L') { mid = 0x7F; }
  else if (romType == 'H') { mid = 0xFF; }
  else { mid = 0xFF; high = 0x40; }
  for (uint8_t count = SNES_HEADER_START; count < SNES_HEADER_END; count++) {
    PORTL = high;
    PORTK = mid;
    PORTF = count;
    delayMicroseconds(10);
    digitalWrite(READ, LOW);
    delayMicroseconds(10);
    uint8_t val = PINC;
    digitalWrite(READ, HIGH);
    buff[count - 0xC0] = val;
    delayMicroseconds(5);
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
