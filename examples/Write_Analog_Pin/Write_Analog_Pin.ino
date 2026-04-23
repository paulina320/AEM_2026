#include <SPI.h>
#include "MAX11300.h"

#define M_PI 3.1415926535897932384626433832795f

#define CNVT_PIN PB0
#define CS_PIN   PA4
#define BTN_PIN  PA0

#define OUT_PIN0 0

MAX11300 pixi(&SPI, CNVT_PIN, CS_PIN);


void setup() {

  Serial.begin(115200);

  pinMode(BTN_PIN, INPUT_PULLUP);  

  // Initialize the MAX11300
  pixi.begin();

  delay(1); // Allow chip to stabilize

  pixi.setDACref(DACInternal);
  pixi.setPinMode(OUT_PIN0, analogOut); //FUNCID

  delay(200); // from datasheet

  pixi.setPinDACrange(OUT_PIN0, DACZeroTo10); //FUNCPRM

  delayMicroseconds(200); // from datasheet

  pixi.writeAnalogPin(OUT_PIN0, 0);
  
  
  Serial.println("Setup complete");
}

int16_t generateSample(uint16_t sample_rate_hz, float frequency_hz, float amplitude ){
    static float phase_offset_rad = 0.0f;

    float phase = 2.0f * M_PI * frequency_hz * 1.0f / sample_rate_hz + phase_offset_rad;
    float sample = (amplitude * sinf(phase) + amplitude) / 2;
    
    phase_offset_rad = fmodf(phase, 2.0f * M_PI);

    return (int16_t)sample;
}
  

void loop() {
  static unsigned long lastUpdateTime = 0;
  const unsigned long updateInterval = 20; // 20 microseconds interval
  
  unsigned long currentTime = micros();
  
  // Wait until it's time for the next update
  if (currentTime - lastUpdateTime >= updateInterval) {
    lastUpdateTime = currentTime;
    
    int buttonState = digitalRead(BTN_PIN);
    
    if(buttonState == LOW) {
      int16_t val = generateSample(50000, 150, 50);
      Serial.println(val + 210);
      pixi.writeAnalogPin(OUT_PIN0, val + 55);
    }
  }
}