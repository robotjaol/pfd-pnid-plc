#include <Arduino.h>

struct Channel {
  uint8_t pin;
  float minimum;
  float maximum;
};

Channel channels[] = {{34, 0.0f, 250.0f}, {35, 0.0f, 300.0f}, {32, 0.0f, 180.0f}};

float scaleAdc(uint16_t raw, const Channel &channel) {
  const float fraction = constrain(raw / 4095.0f, 0.0f, 1.0f);
  return channel.minimum + fraction * (channel.maximum - channel.minimum);
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
}

void loop() {
  static uint32_t sequence = 0;
  Serial.printf("%lu", static_cast<unsigned long>(sequence++));
  for (const auto &channel : channels) {
    Serial.printf(",%.3f", scaleAdc(analogRead(channel.pin), channel));
  }
  Serial.println();
  delay(100);
}

