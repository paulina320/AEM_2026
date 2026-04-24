#include <Wire.h>
#include "DFRobot_BMP280.h"

typedef DFRobot_BMP280_IIC BMP;
BMP bmp280Low(&Wire, BMP::eSdoLow);
BMP bmp280High(&Wire, BMP::eSdoHigh);
BMP *bmp280 = nullptr;

#define SEA_LEVEL_PRESSURE 1013.25f

void scanI2CBus() {
  Serial.println("Scanning I2C bus...");
  bool found = false;
  for (uint8_t address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    if (Wire.endTransmission() == 0) {
      found = true;
      Serial.print("Found device at 0x");
      if (address < 16) {
        Serial.print('0');
      }
      Serial.println(address, HEX);
    }
  }
  if (!found) {
    Serial.println("No I2C devices found.");
  }
  Serial.println();
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Wire.begin(PB7, PB6);
  Wire.setClock(100000);

  Serial.println("BMP280 demo on STM32 Black Pill");
  Serial.println("Expected wiring:");
  Serial.println("  VIN -> 3V3");
  Serial.println("  GND -> GND");
  Serial.println("  SDA -> PB7");
  Serial.println("  SCL -> PB8");
  Serial.println();

  scanI2CBus();

  if (bmp280Low.begin() == BMP::eStatusOK) {
    bmp280 = &bmp280Low;
    Serial.println("BMP280 initialized at address 0x76.");
  } else if (bmp280High.begin() == BMP::eStatusOK) {
    bmp280 = &bmp280High;
    Serial.println("BMP280 initialized at address 0x77.");
  } else {
    Serial.println("BMP280 init failed at 0x76 and 0x77.");
    Serial.println("Check wiring, power, and whether the sensor is really on the I2C bus.");
    while (1) {
      delay(2000);
    }
  }
}

void loop() {
  float temperature = bmp280->getTemperature();
  uint32_t pressure = bmp280->getPressure();
  float altitude = bmp280->calAltitude(SEA_LEVEL_PRESSURE, pressure);

  Serial.print("Temperature = ");
  Serial.print(temperature);
  Serial.println(" *C");

  Serial.print("Pressure = ");
  Serial.print(pressure);
  Serial.println(" Pa");

  Serial.print("Altitude = ");
  Serial.print(altitude);
  Serial.println(" m");

  Serial.println();
  delay(2000);
}
