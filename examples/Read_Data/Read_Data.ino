
#include <SPI.h>
#include "MAX11300.h"

#define CNVT_PIN PB0
#define CS_PIN   PA4

MAX11300 pixi(&SPI, CNVT_PIN, CS_PIN);

const uint8_t IN_PIN6 = 6;
const uint8_t IN_PIN7 = 7;


void setup() {

  Serial.begin(115200);

  pixi.setPinMode(IN_PIN6, analogIn);
  pixi.setPinADCrange(IN_PIN6, ADCZeroTo5);
  pixi.setPinADCref(IN_PIN6, ADCInternal);

  pixi.setPinMode(IN_PIN7, analogIn);
  pixi.setPinADCrange(IN_PIN7, ADCZeroTo5);
  pixi.setPinADCref(IN_PIN7, ADCInternal);

  pixi.setADCmode(ContinuousSweep);

  Serial.println("Analog Pin 6, Analog Pin 7");
}

void loop() {
  if(pixi.isAnalogDataReady(IN_PIN6) && pixi.isAnalogDataReady(IN_PIN7)) {
    uint16_t val6 = pixi.readAnalogPin(IN_PIN6);
    uint16_t val7 = pixi.readAnalogPin(IN_PIN7);
    Serial.println(val6 + "," + val7);
  }
}