int count;
int count2;
void setup() {
  Serial.print("\n");
  // put your setup code here, to run once:
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
  pinMode(10, OUTPUT);
  //Pin /RD
  pinMode(11, OUTPUT);
  //Pin /WR
  pinMode(12, OUTPUT);
  digitalWrite(12, HIGH);
  digitalWrite(10, LOW);
  digitalWrite(11, HIGH);
  Serial.begin(2000000);
  count = 0x7FE0 - 0x7FC0;
  count2 = 1;
}

void loop() {
  // put your main code here, to run repeatedly:
  delayMicroseconds(200);
  while (count >= 0) {
    PORTL = 0x00;
    PORTK = 0xFF;
    PORTF = 0xE0 - count;
    digitalWrite(11, LOW);
    delayMicroseconds(10);
    uint8_t val = PINC;
    digitalWrite(11, HIGH);
    Serial.write(val);
    delayMicroseconds(5);
    count--;
  }
}
