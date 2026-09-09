#include <Adafruit_NeoPixel.h>

#define LED_PIN 35
#define NUMPIXELS 1

Adafruit_NeoPixel pixel(NUMPIXELS, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  pixel.begin();
}

void loop() {
  pixel.setPixelColor(0, pixel.Color(255, 0, 0));
  pixel.show();
  delay(1000);

  pixel.setPixelColor(0, pixel.Color(0, 255, 0));
  pixel.show();
  delay(1000);

  pixel.setPixelColor(0, pixel.Color(0, 0, 255));
  pixel.show();
  delay(1000);

  pixel.setPixelColor(0, pixel.Color(0, 0, 0));
  pixel.show();
  delay(1000);
}
