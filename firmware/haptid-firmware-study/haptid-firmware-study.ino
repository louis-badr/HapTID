#include <Arduino.h>
#include "whitenoise.h"
#include "sample.h"
#include "tone150.h"
// #include "ring.h"


const int pwmRes = 12;
const int sampleRate = 16000;

const int shdnPins[3] = {22, 19, 4};  // keep pin on HIGH to run the amp - each amp controls two motors
const int motorPins[6] = {32, 33, 25, 26, 27, 12};  // in order from left to right

const int pwmMax = pow(2, pwmRes) - 1;
const int pwmFreq = (8 * pow(10, 7)) / pow(2, pwmRes);  // 80 MHz / 2^12 = 19531.25 Hz > sampleRate
int arrayPosition = 0;  // position in the array being played
int arrayLength = 0;  // length of the array being played
hw_timer_t * timer = NULL; // we only need one timer for this program
int receivedValue = 0;  // value received from the serial port
int soundValue = 0;

// Function to print an array
void printArray(int arr[], int size) {
  for (int i = 0; i < size; i++) {
    Serial.print(arr[i]);
    Serial.print(" ");
  }
  Serial.println(); // Print a newline character for better formatting
}

// Generates a sine table at a given frequency and sample rate
uint16_t* generateSineTable(int frequency, int sampleRate)
{
  int samplesPerPeriod = sampleRate / frequency;
  uint16_t* sineTable = new uint16_t[samplesPerPeriod];
  for (int i = 0; i < samplesPerPeriod; i++)
  {
    sineTable[i] = (uint16_t)(sin(2 * PI * i / samplesPerPeriod) * pwmMax / 2 + pwmMax / 2);
  }
  return sineTable;
}

int sineTable150Length = sampleRate / 150;
int sineTable190Length = sampleRate / 190;
uint16_t* sineTable150 = generateSineTable(150, sampleRate); // 150 Hz sine wave fo the motor on the index finger
uint16_t* sineTable190 = generateSineTable(190, sampleRate); // 190 Hz sine wave fo the motor on the index finger
unsigned long clickTimer = 0;
bool isClicking = false;

void IRAM_ATTR onTimer()
{
  if (soundValue > 0)
  {
    if(arrayPosition < arrayLength)
    {
      if (soundValue <= 100)
      {
        ledcWrite(0, whitenoise_data[arrayPosition] * soundValue / 100);
      }else if (soundValue <= 200)
      {
        ledcWrite(1, sineTable150[arrayPosition] * (soundValue - 100) / 100);
      } else if (soundValue <= 300)
      {
        ledcWrite(1, sineTable190[arrayPosition] * (soundValue - 200) / 100);
      }
      arrayPosition++;
    } else
    {
      arrayPosition = 0;
    }
  }
}


void playStartSequence()
{
  for (int i = 0; i <= 5; i++)
  {
    ledcWrite(i, 0);
    ledcWrite(i, pwmMax);
    delay(7);
    ledcWrite(i, 0);
    delay(250);
  }
  delay(500);
  // do it in reverse
  for (int i = 5; i >= 0; i--)
  {
    ledcWrite(i, 0);
    ledcWrite(i, pwmMax);
    delay(7);
    ledcWrite(i, 0);
    delay(250);
  }
}

void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(10);
  // Serial.print("APB Freq = ");
  // Serial.print(getApbFrequency());
  // Serial.println(" Hz");
  // init shdn pins and turn on amps
  for (int i = 0; i <= 2; i++)
  {
    pinMode(shdnPins[i], OUTPUT);
    digitalWrite(shdnPins[i], HIGH);
  }
  // init motor pins
  for (int i = 0; i <= 5; i++)
  {
    ledcSetup(i, pwmFreq, pwmRes);
    ledcAttachPin(motorPins[i], i);
  }
  // init interrupt timer
  timer = timerBegin(0, 80, true);
  timerAttachInterrupt(timer, &onTimer, true);
  timerAlarmWrite(timer, 1000000 / sampleRate, true);  // nombre de us (1 000 000 us = 1s pour rappel)
  timerAlarmEnable(timer);
  delay(3000);
  playStartSequence();
}

void loop()
{
  if (Serial.available() > 0) {
    receivedValue = Serial.parseInt();
    // Serial.println(receivedValue);
    // 501 to 506 are clicks - left to right
    if (receivedValue >= 301 && receivedValue <= 306)
    {
      // if the motor is not clicking
      if (!isClicking)
      {
        ledcWrite(receivedValue - 301, 0);
        ledcWrite(receivedValue - 301, pwmMax);
        // set the click time
        clickTimer = millis();
        // set the motor to clicking
        isClicking = true;
      }
    } else 
    {
      soundValue = receivedValue;
      if (soundValue <= 100)
      {
        arrayPosition = 0;
        arrayLength = whitenoise_length;
      } else if (soundValue <= 200)
      {
        arrayPosition = 0;
        arrayLength = sineTable150Length;
      } else if (soundValue <= 300)
      {
        arrayPosition = 0;
        arrayLength = sineTable190Length;
      }
    }
  }
  // if the motor is clicking
  if (isClicking)
  {
    // if more than 10 ms have passed since the click
    if (millis() - clickTimer > 7)
    {
      // turn off the motor
      ledcWrite(receivedValue - 301, 0);
      // set the motor to not clicking
      isClicking = false;
    }
  }
}