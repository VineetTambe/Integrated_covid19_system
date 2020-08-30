#include <LowPower.h>

const byte motorpin = 8;
const byte interrupt_pin = 2;
volatile byte state = LOW;

void setup() {
  Serial.begin(9600);
  pinMode(motorpin,OUTPUT);
}

void loop() {
  // the interrupt must be attached each loop
  attachInterrupt(digitalPinToInterrupt(interrupt_pin),interrupt_routine,RISING);
  LowPower.powerDown(SLEEP_FOREVER,ADC_OFF,BOD_OFF); // sleep until interrupt
  detachInterrupt(digitalPinToInterrupt(interrupt_pin)); // remove interrupt
  // the usual wake routine that turns on the LED
  if (state==HIGH){
    digitalWrite(motorpin,HIGH);
    Serial.println("HIGH");
    delay(500);
  }
  if (state==HIGH){
    state = LOW;
    digitalWrite(motorpin,LOW);
  }
}

void interrupt_routine(){
  state = HIGH;
}
