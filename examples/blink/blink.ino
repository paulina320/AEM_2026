#define LED_PIN PC13

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
  delay(1000);

  Serial.println("STM32 Black Pill is starting...");
}

void loop() {
  Serial.print("some data");
} 