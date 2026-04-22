
#include <SPI.h>
#include "MAX11300.h"

#define CNVT_PIN PB0
#define CS_PIN   PA4

MAX11300 pixi(&SPI, CNVT_PIN, CS_PIN);

const uint8_t IN_PIN = 6;


void setup() {

  Serial.begin(115200);

  pixi.setPinMode(IN_PIN, analogIn);
  pixi.setPinADCrange(IN_PIN, ADCZeroTo5);
  pixi.setPinADCref(IN_PIN, ADCInternal);
  pixi.setADCmode(ContinuousSweep);

  Serial.println("Setup done");
}

void loop() {
  uint16_t val = pixi.readAnalogPin(IN_PIN);
  Serial.print("Read Analog: ");
  Serial.println(val);
  delay(500);
}
