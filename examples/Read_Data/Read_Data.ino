#include <MAX11300.h>
#include <MAX11300registers.h>

#include <SPI.h>
#include "MAX11300.h"

#define CNVT_PIN PB0
#define CS_PIN   PA4
#define BTN_PIN  PA0

#define IN_PIN6 6
#define IN_PIN7 7

MAX11300 pixi(&SPI, CNVT_PIN, CS_PIN);



void setup() {

  Serial.begin(115200);

  pinMode(BTN_PIN, INPUT_PULLUP);  


  pixi.setPinMode(IN_PIN6, analogIn);
  pixi.setPinADCrange(IN_PIN6, ADCZeroTo2_5);
  pixi.setPinADCref(IN_PIN6, ADCInternal);

  pixi.setPinMode(IN_PIN7, analogIn);
  pixi.setPinADCrange(IN_PIN7, ADCZeroTo2_5);
  pixi.setPinADCref(IN_PIN7, ADCInternal);

  pixi.setADCmode(ContinuousSweep);

  Serial.println("Analog Pin 6, Analog Pin 7");
}

void loop() {
  int buttonState = digitalRead(BTN_PIN);

  if(buttonState == LOW && pixi.isAnalogDataReady(IN_PIN6) && pixi.isAnalogDataReady(IN_PIN7)) {
    uint16_t val6 = pixi.readAnalogPin(IN_PIN6);
    uint16_t val7 = pixi.readAnalogPin(IN_PIN7);
    Serial.print(val6);
    Serial.print(",");
    Serial.println(val7);
  } 
  else {
    delayMicroseconds(5);
  }
}