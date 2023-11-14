#include <ESPTrueRandom.h>

const int ledcResolution = 8;
const int pwmFrequency = 500;
const int maxDutyCycle = 1 << ledcResolution;
// keep pin on HIGH to run the amp - each amp controls two motors
const int shdnPins[3] = {22, 19, 4};
// in order from left to right
const int motorPins[6] = {32, 33, 25, 26, 27, 12};

unsigned long serialTimer;
unsigned long clickTimer;
float volume = 0;
float previousValue = 0;
float receivedValue = 0;
bool isClicking = false;

void setup() {
  Serial.begin(115200);
  // init shdn pins and turn on amps
  for (int i = 0; i <= 2; i++) {
    pinMode(shdnPins[i], OUTPUT);
    digitalWrite(shdnPins[i], HIGH);
  }
  // init ledc channels, attach motor pins and turn the motors off jic
  for (int i = 0; i <= 5; i++) {
    ledcSetup(i, pwmFrequency, ledcResolution);
    ledcAttachPin(motorPins[i], i);
    ledcWrite(i, 0);
  }
  delay(3000);
  playStartingSequence();
  delay(1000);
}

void loop() {
  // listen to serial for commands
  if (Serial.available() >= 0) {
    // read the incoming float value
    receivedValue = Serial.parseFloat();
    if (isClicking == false && receivedValue >= 2 && receivedValue <= 7) {
      // start click
      ledcWrite(int(receivedValue - 2), maxDutyCycle - 1);
      // start timer
      clickTimer = millis();
      isClicking = true;
      Serial.print("Start click moteur : ");
      Serial.println(int(receivedValue-1));
    }
    if (receivedValue >= 0 && receivedValue <= 1) {
      volume = receivedValue;
      Serial.print("New volume value : ");
      Serial.println(volume);
    }
    previousValue = receivedValue;
  }
  if (isClicking == true && millis() - clickTimer >= 10) {
    // stop click
    ledcWrite(int(receivedValue - 2), 0);
    isClicking = false;
    Serial.print("Stop click moteur : ");
    Serial.println(int(receivedValue-1));
  }
  ledcWrite(0, ESPTrueRandom.random(maxDutyCycle) * volume);
  delayMicroseconds(50);
}

// plays a click on the selected motor (1 to 6) at volume (0 to 1)
void playClick(int motorNo, int volume) {
  unsigned long starttime = millis();
  volume *= maxDutyCycle - 1;
  ledcWrite(motorNo - 1, volume);
  while (millis() - starttime <= 10) {}
  ledcWrite(motorNo - 1, 0);
}

void playStartingSequence() {
  // play a click on each motor in order
  for (int i = 1; i <= 6; i++) {
    playClick(i, 1);
    delay(250);
  }
  delay(250);
  // play a click on each motor in reverse order
  for (int i = 6; i >= 1; i--) {
    playClick(i, 1);
    delay(250);
  }
  delay(750);
  // play a click on all motors at the same time
  for (int i = 1; i <= 6; i++) {
    playClick(i, 1);
  }
}
