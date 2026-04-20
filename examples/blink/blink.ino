#define LED_PIN PC13

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);
  delay(1000);

  Serial.println("STM32 Black Pill is starting...");
}

void loop() {
  digitalWrite(LED_PIN, LOW); // LED on
  Serial.println("LED ON");
  delay(500);

  digitalWrite(LED_PIN, HIGH); // LED off
  Serial.println("LED OFF");
  delay(500);
} 