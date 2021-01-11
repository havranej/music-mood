
#include <Adafruit_NeoPixel.h>

#define PIN        6
#define NUMPIXELS 16
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
#define DELAYVAL 150

int red = 0;
int green = 150;
int blue = 150;

int playback_status = 0; // 0 = paused / 1 = playing
int current_pixel = 0;

void setup() {
  Serial.begin(9600);
  pixels.begin();
}


void loop() {
  if(Serial.available() > 0){
    playback_status = Serial.read();
    if(playback_status){
      red = Serial.read();
      green = Serial.read();
      blue = Serial.read();
    }
  }

  if(!playback_status){
    pixels.setPixelColor(current_pixel, pixels.Color(0, 0, 0));
  }
  
  current_pixel = (current_pixel + 1) % NUMPIXELS;
  pixels.setPixelColor(current_pixel, pixels.Color(red, green, blue));
  
  pixels.show();
  delay(DELAYVAL);
}
