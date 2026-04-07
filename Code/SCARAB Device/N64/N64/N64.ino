#define NOP __asm__ __volatile__("nop\n\t")
#define READ_HIGH PORTH |= 0b00100000
#define READ_LOW PORTH &= 0b11011111
#define WRITE_HIGH PORTH |= 0b01000000
#define WRITE_LOW PORTH &= 0b10111111
#define ALEL_HIGH PORTH |= 0b00010000
#define ALEL_LOW PORTH &= 0b11101111
#define ALEH_HIGH PORTH |= 0b00001000
#define ALEH_LOW PORTH &= 0b11110111
#define DIR_CART PORTB |= 1
#define DIR_SCARAB PORTB &= 0b11111110
#define AD0toAD7out PORTF
#define AD8toAD15out PORTK
#define AD0toAD7in PINF
#define AD8toAD15in PINK
bool isChecked;

void setup() {
  // put your setup code here, to run once:
  DDRH = 0xFF;
  DDRB = 0XFF;
  DDRF = 0xFF; //LOWER
  DDRK = 0xFF; //UPPER
  READ_HIGH;
  WRITE_HIGH;
  ALEL_HIGH;
  ALEH_HIGH;
  delay(300);
  Serial.begin(2000000);
  isChecked = false;
}

void n64WriteSetup() {
  DDRF = 0xFF; //LOWER
  PORTF = 0x00;
  DDRK = 0xFF; //UPPER
  PORTK = 0x00;
  DIR_CART;
  delayMicroseconds(1);
}

void n64ReadSetup() {
  DDRF = 0x00; //LOWER
  DDRK = 0x00; //UPPER
  DIR_SCARAB;
  delayMicroseconds(1);
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

  NOP;

  ALEH_LOW;

  AD0toAD7out = adrLow & 0xFF;
  AD8toAD15out = (adrLow >> 8) & 0xFF;

  NOP;NOP;

  ALEL_LOW;

  n64ReadSetup();
}

uint16_t n64ReadData() {
  READ_LOW;
  NOP;NOP;NOP;NOP;NOP;
  uint16_t tempWord = ((AD8toAD15in & 0xFF) << 8) | (AD0toAD7in & 0xFF);
   NOP;NOP;NOP;NOP;NOP;
  tempWord = ((AD8toAD15in & 0xFF) << 8) | (AD0toAD7in & 0xFF);
   NOP;NOP;NOP;NOP;NOP;
  tempWord = ((AD8toAD15in & 0xFF) << 8) | (AD0toAD7in & 0xFF);
   NOP;NOP;NOP;NOP;NOP;
  READ_HIGH;
  return tempWord;
}

void loop() {
  while(!isChecked) {
    // Set the address
    byte sdBuffer[64];
    // Read first 64 bytes of rom
    for (int c = 0; c < 64; c += 2) {
      // split word
      n64WriteAddress(0x10000000+c);
      NOP;NOP;NOP;NOP;NOP;
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
    isChecked = true;
  }

}
