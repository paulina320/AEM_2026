#include "MAX11300.h"
#include <math.h>

// Blackpill PIN definitions
#define CNVT_PIN PB0
#define CS_PIN   PA4
#define PWM_PELTIER_PIN PB6
#define COOLING_PELTIER_PIN PB7 // NOTE: cooling and heating should not be HIGH simultaneously
#define HEATING_PELTIER_PIN PB8

// MAX11300 pin definitions
#define PIXI_IN_PIN 0

MAX11300 pixi(&SPI, CNVT_PIN, CS_PIN);

// Temperature conversion constants
const float Vin = 3.3;        // Supply voltage
const float Ri = 22000.0;     // Known resistor value in ohms

// Steinhart-Hart coefficients, check docs/Thermistor_conversion.txt on how these are calculated.
const float A = 1.40e-03;     // Coefficient A
const float B = 2.37e-04;     // Coefficient B  
const float C = 9.90e-08;     // Coefficient C

const float proportionalGain = 5.0; // Proportional gain for temp control loop

float targetTemp = 35.0;
float measuredTemp = 0.0;
uint32_t duty = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    delay(10);
  }

  pixi.begin();
  pixi.setPinMode(PIXI_IN_PIN, analogIn);
  pixi.setPinADCrange(PIXI_IN_PIN, ADCZeroTo10);
  pixi.setPinADCref(PIXI_IN_PIN, ADCInternal);
  pixi.setADCmode(ContinuousSweep);

  pinMode(COOLING_PELTIER_PIN, OUTPUT);
  pinMode(HEATING_PELTIER_PIN, OUTPUT);
  pinMode(PWM_PELTIER_PIN, OUTPUT);

  Serial.println("MAX11300 initialized");
}

void loop() {
  // Read analog value from the temperature sensor
  uint16_t adcValue = pixi.readAnalogPin(PIXI_IN_PIN);
  
  // Convert ADC reading to temperature
  measuredTemp = ConvertToCelsius(adcValue);
  
  Serial.print("ADC: ");
  Serial.print(adcValue);
  Serial.print(", Measured: ");
  Serial.print(measuredTemp, 3);
  Serial.print(" C, Target: ");
  Serial.print(targetTemp, 3);
  Serial.println(" C");

  // Simple proportional control loop
  float error = targetTemp - measuredTemp;
  duty = (uint16_t)(abs(error) * proportionalGain); // Proportional gain

  digitalWrite(HEATING_PELTIER_PIN, error > 0);
  digitalWrite(COOLING_PELTIER_PIN, error < 0);

  duty = constrain(duty, 0, 255);

  analogWrite(PWM_PELTIER_PIN, duty); // Write PWM signal to control Peltier

  delay(50); 
}

float ConvertToCelsius(uint16_t adcValue) {
  // Convert ADC value to voltage (assuming 12-bit ADC, 0-10V range (ADCZeroTo10 config for Pixi))
  float Vo = (float(adcValue) / 4096.0) * 10;
  
  // Calculate thermistor resistance using voltage divider equation
  // Vo = Vin * Ro / (Ri + Ro)
  // Solving for Ro: Ro = Ri / ((Vin/Vo) - 1)
  float Ro = Ri / ((Vin / Vo) - 1.0);
  
  // Apply Steinhart-Hart equation: T = 1 / (A + B*ln(R) + C*ln(R)^3)
  float logR = log(Ro);
  float temperatureK = 1.0 / (A + B * logR + C * logR * logR * logR);
  
  // Convert from Kelvin to Celsius
  float temperatureC = temperatureK - 273.15;
  
  return temperatureC;
}

