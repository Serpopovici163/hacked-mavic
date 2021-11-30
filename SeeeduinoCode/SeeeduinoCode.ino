#include <Adafruit_NeoPixel.h>
#include <IBusBM.h>

#define LEFT_LED 2
#define RELAY 4
#define ECHO 5
#define TRIG 6
#define RIGHT_LED 13

#define STAT1 A0
#define STAT2 A1
#define STAT3 A2

#define DELAY 10

Adafruit_NeoPixel lights(8, 3, NEO_GRB + NEO_KHZ800);
IBusBM IBus;
long cycleStartTime, currentTime;
int flightStatus = 0;

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
}

void hazardLightCycle() {
  currentTime = millis();
  if (currentTime < (cycleStartTime + 100)) {
    lights.setPixelColor(0, 255, 255, 0);
    lights.setPixelColor(1, 0, 0, 0);
    lights.setPixelColor(2, 0, 0, 0);
    lights.setPixelColor(3, 255, 255, 0);
    lights.setPixelColor(4, 255, 255, 0);
    lights.setPixelColor(5, 255, 255, 0);
    digitalWrite(RIGHT_LED, HIGH);
  } else if (currentTime < (cycleStartTime + 200)) {
    lights.setPixelColor(0, 0, 0, 0);
    lights.setPixelColor(3, 0, 0, 0);
    digitalWrite(RIGHT_LED, HIGH);
  } else if (currentTime < (cycleStartTime + 300)) {
    lights.setPixelColor(0, 255, 255, 0);
    lights.setPixelColor(3, 255, 255, 0);
    digitalWrite(RIGHT_LED, HIGH);
  } else if (currentTime < (cycleStartTime + 400)) {
    lights.setPixelColor(0, 0, 0, 0);
    lights.setPixelColor(3, 0, 0, 0);
    digitalWrite(RIGHT_LED, HIGH);
  } else if (currentTime < (cycleStartTime + 500)) {
    lights.setPixelColor(0, 0, 0, 0);
    lights.setPixelColor(1, 255, 255, 0);
    lights.setPixelColor(2, 255, 255, 0);
    lights.setPixelColor(3, 0, 0, 0);
    lights.setPixelColor(4, 0, 0, 0);
    lights.setPixelColor(5, 0, 0, 0);
    digitalWrite(LEFT_LED, HIGH);
  } else if (currentTime < (cycleStartTime + 600)) {
    lights.setPixelColor(1, 0, 0, 0);
    lights.setPixelColor(2, 0, 0, 0);
    digitalWrite(LEFT_LED, HIGH);
  } else if (currentTime < (cycleStartTime + 700)) {
    lights.setPixelColor(1, 255, 255, 0);
    lights.setPixelColor(2, 255, 255, 0);
    lights.setPixelColor(4, 0, 0, 0);
    lights.setPixelColor(5, 0, 0, 0);
    digitalWrite(LEFT_LED, HIGH);
  } else if (currentTime < (cycleStartTime + 800)) {
    lights.setPixelColor(1, 0, 0, 0);
    lights.setPixelColor(2, 0, 0, 0);
    digitalWrite(LEFT_LED, HIGH);
  } else {
    cycleStartTime = currentTime;
  }
}

void noWifi() {
  currentTime = millis();
  if (currentTime < (cycleStartTime + 1000)) {
    lights.setPixelColor(0, 255, 0, 0);
    lights.setPixelColor(1, 0, 0, 0);
    digitalWrite(LEFT_LED, HIGH);
    digitalWrite(RIGHT_LED, LOW);
  } else if (currentTime < (cycleStartTime + 2000)) {
    lights.setPixelColor(0, 0, 0, 0);
    lights.setPixelColor(1, 255, 0, 0);
    digitalWrite(LEFT_LED, LOW);
    digitalWrite(RIGHT_LED, HIGH);
  } else {
    cycleStartTime = currentTime;
  }
}

void noLock() {
  currentTime = millis();
  if (currentTime < (cycleStartTime + 1000)) {
    lights.setPixelColor(0, 255, 255, 0);
    lights.setPixelColor(1, 0, 0, 0);
    digitalWrite(LEFT_LED, HIGH);
    digitalWrite(RIGHT_LED, LOW);
  } else if (currentTime < (cycleStartTime + 2000)) {
    lights.setPixelColor(0, 0, 0, 0);
    lights.setPixelColor(1, 255, 255, 0);
    digitalWrite(LEFT_LED, LOW);
    digitalWrite(RIGHT_LED, HIGH);
  } else {
    cycleStartTime = currentTime;
  }
}

void readyToGo() {
  currentTime = millis();
  if (currentTime < (cycleStartTime + 100)) {
    lights.setPixelColor(4, 0, 255, 0);
    lights.setPixelColor(5, 0, 255, 0);
  } else if (currentTime < (cycleStartTime + 200)) {
    lights.setPixelColor(4, 0, 0, 0);
    lights.setPixelColor(5, 0, 0, 0);
  } else if (currentTime < (cycleStartTime + 300)) {
    lights.setPixelColor(4, 0, 255, 0);
    lights.setPixelColor(5, 0, 255, 0);
  } else if (currentTime < (cycleStartTime + 400)) {
    lights.setPixelColor(4, 0, 0, 0);
    lights.setPixelColor(5, 0, 0, 0);
  } else {
    cycleStartTime = currentTime;
  }
}

void userControl() {
  currentTime = millis();
  if (currentTime < (cycleStartTime + 100)) {
    lights.setPixelColor(4, 0, 255, 0);
    lights.setPixelColor(5, 0, 255, 0);
  } else if (currentTime < (cycleStartTime + 200)) {
    lights.setPixelColor(4, 0, 0, 0);
    lights.setPixelColor(5, 0, 0, 0);
  } else if (currentTime < (cycleStartTime + 300)) {
    lights.setPixelColor(4, 0, 255, 0);
    lights.setPixelColor(5, 0, 255, 0);
  } else if (currentTime < (cycleStartTime + 1000)) {
    lights.setPixelColor(4, 0, 0, 0);
    lights.setPixelColor(5, 0, 0, 0);
  } else {
    cycleStartTime = currentTime;
  }
}

void beacon() {
  for (int i = 0; i < 6; i++) {
    lights.setPixelColor(i, 255, 255, 255);
  }
}

void cancer() {
  currentTime = millis();
  if (currentTime < (cycleStartTime + 50)) {
    for (int i = 0; i < 6; i++) {
      lights.setPixelColor(i, 255, 255, 255);
    }
  } else if (currentTime < (cycleStartTime + 100)) {
    for (int i = 0; i < 6; i++) {
      lights.setPixelColor(i, 0, 0, 0);
    }
  } else {
    cycleStartTime = currentTime;
  }
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
  //clear leds
  digitalWrite(LEFT_LED, LOW);
  digitalWrite(RIGHT_LED, LOW);
  for (int i = 0; i < 6; i++)
    lights.setPixelColor(i, 0, 0, 0);
  
  //check IBus related functions
  if (LEDState())
    policeLightCycle();

  if (controlState())
    digitalWrite(RELAY, HIGH);
  else
    digitalWrite(RELAY, LOW);

  //check status pins
  //if leds are overriden, ignore this part
  if (!LEDState()) {
    flightStatus = 0;
    if (analogRead(STAT1) > 800)
      flightStatus += 1;
    if (analogRead(STAT2) > 800)
      flightStatus += 2;
    if (analogRead(STAT3) > 800)
      flightStatus += 4;

    if (flightStatus == 0) {
      for (int i = 0; i < 6; i++) {
        lights.setPixelColor(i, 255, 0, 0);
      }
    } else if (flightStatus == 1) {
      noWifi();
    } else if (flightStatus == 2) {
      noLock();
    } else if (flightStatus == 3) {
      readyToGo();
    } else if (flightStatus == 4) {
      hazardLightCycle();
    } else if (flightStatus == 5) {
      policeLightCycle();
    } else if (flightStatus == 6) {
      beacon();
    } else if (flightStatus == 7) {
      cancer();
    }
  }

  //lastly override everything if drone is being flown by user
  if (!controlState() && IBus.readChannel(2) > 1050 && !LEDState() && IBus.readChannel(5) > 1500) {
    for (int i = 0; i < 6; i++)
      lights.setPixelColor(i, 0, 0, 0);
    digitalWrite(LEFT_LED, LOW);
    digitalWrite(RIGHT_LED, LOW);
    userControl();
  }
    
  lights.show();
  delay(DELAY);
}
