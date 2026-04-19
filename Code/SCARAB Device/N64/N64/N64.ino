#define NOP __asm__ __volatile__("nop\n\t")
#define READ_HIGH PORTC |= 0b00000100
#define READ_LOW PORTC &= 0b11111011
#define WRITE_HIGH PORTC |= 0b00001000
#define WRITE_LOW PORTC &= 0b11110111
#define ALEL_HIGH PORTC |= 0b00000010
#define ALEL_LOW PORTC &= 0b11111101
#define ALEH_HIGH PORTC |= 0b00000001
#define ALEH_LOW PORTC &= 0b11111110
#define DIR_CART PORTG |= 0b00000001
#define DIR_SCARAB PORTG &= 0b11111110
#define OE_HIGH PORTG |= 0b00000010
#define OE_LOW PORTG &= 0b11111101
#define AD0toAD7out PORTL
#define AD8toAD15out PORTK
#define AD0toAD7in PINL
#define AD8toAD15in PINK
bool isChecked;

void setup() {
  // put your setup code here, to run once:
  DDRG = 0xFF;
  DDRC = 0xFF;
  DDRL = 0xFF; //LOWER
  DDRK = 0xFF; //UPPER
  READ_HIGH;
  WRITE_HIGH;
  ALEL_HIGH;
  ALEH_HIGH;
  OE_LOW;
  PORTG |= 0b00000100;
  delay(300);
  Serial.begin(2000000);
  isChecked = false;
}

void n64WriteSetup() {
  DDRL = 0xFF; //LOWER
  PORTL = 0x00;
  DDRK = 0xFF; //UPPER
  PORTK = 0x00;
  DIR_CART;
  delayMicroseconds(5);
}

void n64ReadSetup() {
  DDRL = 0x00; //LOWER
  DDRK = 0x00; //UPPER
  PORTL = 0xFF;
  PORTK = 0xFF;
  DIR_SCARAB;
  delayMicroseconds(5);
}

void n64WriteAddress(uint32_t address) {
  n64WriteSetup();

  uint16_t adrLow = address & 0xFFFF;
  uint16_t adrHigh = (address >> 16) & 0xFFFF;

  READ_HIGH;
  WRITE_HIGH;
  ALEL_HIGH;
  ALEH_HIGH;

  AD0toAD7out = adrHigh & 0xFF;
  AD8toAD15out = (adrHigh >> 8) & 0xFF;

  delay(5);

  ALEH_LOW;

  AD0toAD7out = adrLow & 0xFF;
  AD8toAD15out = (adrLow >> 8) & 0xFF;

  delay(5);delay(5);

  ALEL_LOW;

  n64ReadSetup();
}

uint16_t n64ReadData() {
  READ_LOW;
  delay(5);NOP;NOP;NOP;NOP;
  uint16_t tempWord = ((AD8toAD15in & 0xFF) << 8) | (AD0toAD7in & 0xFF);
  READ_HIGH;
  return tempWord;
}

void loop() {
  while(!isChecked) {
    // Set the address
    byte sdBuffer[64];
    delayMicroseconds(5);
    // Read first 64 bytes of rom
    for (int c = 0; c < 64; c += 2) {
      n64WriteAddress(0x10000000 + c);
      // split word
      word myWord = n64ReadData();
      byte loByte = myWord & 0xFF;
      byte hiByte = myWord >> 8;

      // write to buffer
      sdBuffer[c] = hiByte;
      sdBuffer[c + 1] = loByte;
    }
    // Pull ale_H(PC1) high
    ALEH_HIGH;
    for(int i = 0; i < 64; i++)
    {
      Serial.print(sdBuffer[i], HEX);
      Serial.print(" ");
    }
    Serial.println();
    Serial.write(sdBuffer, 64);
    Serial.println();
    isChecked = true;
  }

}
