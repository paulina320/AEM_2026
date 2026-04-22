#include "MAX11300.h"

#define CNVT_PIN PB0
#define CS_PIN   PA4

MAX11300 pixi(&SPI, CNVT_PIN, CS_PIN);


void setup() {
  Serial.begin(115200);
  while (!Serial) {
    delay(10);
  }

  pixi.begin();
  pixi.setADCmode(ContinuousSweep);

  Serial.println("MAX11300 temperature monitor");
}

void loop() {
  double internalTemp = pixi.readInternalTemp();
  double externalTemp1 = pixi.readExternalTemp1();
  double externalTemp2 = pixi.readExternalTemp2();

  Serial.print("Internal: ");
  Serial.print(internalTemp, 3);
  Serial.print(" C, External1: ");
  Serial.print(externalTemp1, 3);
  Serial.print(" C, External2: ");
  Serial.print(externalTemp2, 3);
  Serial.println(" C");

  delay(1000);
}
