#include <Adafruit_NeoPixel.h>
#include <IBusBM.h>

#define LEFT_LED 2
#define RELAY 4
#define ECHO 5
#define TRIG 6
#define RIGHT_LED 13
#define DELAY 10

Adafruit_NeoPixel lights(8, 3, NEO_GRB + NEO_KHZ800);
IBusBM IBus;
long cycleStartTime, currentTime;

void setup() {
  pinMode(LEFT_LED, OUTPUT);
  pinMode(RIGHT_LED, OUTPUT);
  pinMode(RELAY, OUTPUT);

  IBus.begin(Serial);

  lights.begin();
  lights.clear();
  lights.show();

  for (long hue = 0; hue < 65536; hue += 256) {
    for (int i = 0; i < 8; i++) {
      lights.setPixelColor(i, lights.ColorHSV(hue));
    }
    lights.show();
    delay(DELAY);
  }

  lights.clear();
  lights.show();
  digitalWrite(LEFT_LED, HIGH);
  digitalWrite(RIGHT_LED, HIGH);
  delay(100);
  digitalWrite(LEFT_LED, LOW);
  digitalWrite(RIGHT_LED, LOW);
  delay(100);
  digitalWrite(LEFT_LED, HIGH);
  digitalWrite(RIGHT_LED, HIGH);
  delay(100);
  digitalWrite(LEFT_LED, LOW);
  digitalWrite(RIGHT_LED, LOW);
  delay(100);
  digitalWrite(LEFT_LED, HIGH);
  digitalWrite(RIGHT_LED, HIGH);
  delay(100);
  digitalWrite(LEFT_LED, LOW);
  digitalWrite(RIGHT_LED, LOW);
  delay(100);
  
  cycleStartTime = millis();
}

void policeLightCycle() {
  currentTime = millis();
  if (currentTime < (cycleStartTime + 50)) { //front and back slow, bottom fast
    lights.setPixelColor(0, 255, 0, 0);
    lights.setPixelColor(1, 0, 0, 0);
    lights.setPixelColor(2, 0, 0, 0);
    lights.setPixelColor(3, 0, 0, 255);
    lights.setPixelColor(4, 255, 0, 0);
    lights.setPixelColor(5, 0, 0, 0);
    digitalWrite(LEFT_LED, HIGH);
    digitalWrite(RIGHT_LED, LOW);
  } else if (currentTime < (cycleStartTime + 100)) {
    lights.setPixelColor(3, 0, 0, 0);
    digitalWrite(LEFT_LED, LOW);
  } else if (currentTime < (cycleStartTime + 150)) {
    lights.setPixelColor(3, 0, 0, 255);
    digitalWrite(LEFT_LED, HIGH);
  } else if (currentTime < (cycleStartTime + 200)) {
    lights.setPixelColor(3, 0, 0, 0);
    digitalWrite(LEFT_LED, LOW);
  } else if (currentTime < (cycleStartTime + 250)) {
    lights.setPixelColor(0, 0, 0, 0);
    lights.setPixelColor(1, 0, 0, 255);
    lights.setPixelColor(2, 255, 0, 0);
    lights.setPixelColor(3, 0, 0, 0);
    lights.setPixelColor(4, 0, 0, 0);
    lights.setPixelColor(5, 0, 0, 255);
    digitalWrite(RIGHT_LED, HIGH);
  } else if (currentTime < (cycleStartTime + 300)) {
    lights.setPixelColor(2, 0, 0, 0);
    digitalWrite(RIGHT_LED, LOW);
  } else if (currentTime < (cycleStartTime + 350)) {
    lights.setPixelColor(2, 255, 0, 0);
    digitalWrite(RIGHT_LED, HIGH);
  } else if (currentTime < (cycleStartTime + 400)) {
    lights.setPixelColor(2, 0, 0, 0);
    digitalWrite(RIGHT_LED, LOW);
  } else if (currentTime < (cycleStartTime + 450)) { //front and back fast, bottom slow
    lights.setPixelColor(0, 255, 0, 0);
    lights.setPixelColor(1, 0, 0, 0);
    lights.setPixelColor(2, 0, 0, 0);
    lights.setPixelColor(3, 0, 0, 255);
    lights.setPixelColor(4, 255, 0, 0);
    lights.setPixelColor(5, 0, 0, 0);
    digitalWrite(LEFT_LED, HIGH);
  } else if (currentTime < (cycleStartTime + 500)) {
    lights.setPixelColor(0, 0, 0, 0);
    lights.setPixelColor(4, 0, 0, 0);
  } else if (currentTime < (cycleStartTime + 550)) {
    lights.setPixelColor(0, 255, 0, 0);
    lights.setPixelColor(4, 255, 0, 0);
    digitalWrite(LEFT_LED, LOW);
    digitalWrite(RIGHT_LED, HIGH);
  } else if (currentTime < (cycleStartTime + 600)) {
    lights.setPixelColor(0, 0, 0, 0);
    lights.setPixelColor(4, 0, 0, 0);
  } else if (currentTime < (cycleStartTime + 650)) {
    lights.setPixelColor(0, 0, 0, 0);
    lights.setPixelColor(1, 0, 0, 255);
    lights.setPixelColor(2, 255, 0, 0);
    lights.setPixelColor(3, 0, 0, 0);
    lights.setPixelColor(4, 0, 0, 0);
    lights.setPixelColor(5, 0, 0, 255);
    digitalWrite(LEFT_LED, HIGH);
    digitalWrite(RIGHT_LED, LOW);
  } else if (currentTime < (cycleStartTime + 700)) {
    lights.setPixelColor(1, 0, 0, 0);
    lights.setPixelColor(5, 0, 0, 0);
  } else if (currentTime < (cycleStartTime + 750)) {
    lights.setPixelColor(1, 0, 0, 255);
    lights.setPixelColor(5, 0, 0, 255);
    digitalWrite(LEFT_LED, LOW);
    digitalWrite(RIGHT_LED, HIGH);
  } else if (currentTime < (cycleStartTime + 800)) {
    lights.setPixelColor(1, 0, 0, 0);
    lights.setPixelColor(5, 0, 0, 0);
  } else {
    cycleStartTime = currentTime;
    digitalWrite(LEFT_LED, LOW);
    digitalWrite(RIGHT_LED, LOW);
  }
  lights.show();
}

bool controlState() {
  if (IBus.readChannel(6) > 1500)
    return true;
  return false;
}

bool LEDState() {
  if (IBus.readChannel(7) > 1500)
    return true;
  return false;
}

void loop() {
  // put your main code here, to run repeatedly:
  
  if (LEDState())
    policeLightCycle();

  if (controlState())
    digitalWrite(RELAY, HIGH);
  else
    digitalWrite(RELAY, LOW);
    
  lights.show();
  delay(DELAY);
}
