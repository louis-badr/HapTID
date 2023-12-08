#include <Arduino.h>
#include "whitenoise.h"
#include "sample.h"
// #include "ring.h"


const int pwmRes = 12;
const int sampleRate = 16000;

const int shdnPins[3] = {22, 19, 4};  // keep pin on HIGH to run the amp - each amp controls two motors
const int motorPins[6] = {32, 33, 25, 26, 27, 12};  // in order from left to right

const int pwmRange = pow(2, pwmRes) - 1;
const int pwmFreq = (8 * pow(10, 7)) / pow(2, pwmRes);  // 80 MHz / 2^12 = 19531.25 Hz > sampleRate
int arrayPosition = 0;  // position in the array being played
int arrayLength = 0;  // length of the array being played
hw_timer_t * timer = NULL; // we only need one timer for this program
int receivedValue = 0;  // value received from the serial port


// Function to print an array
void printArray(int arr[], int size) {
  for (int i = 0; i < size; i++) {
    Serial.print(arr[i]);
    Serial.print(" ");
  }
  Serial.println(); // Print a newline character for better formatting
}

// Generates a sine table at a given frequency and sample rate
int* generateSineTable(int frequency, int sampleRate)
{
  int samplesPerPeriod = sampleRate / frequency;
  int* sineTable = new int[samplesPerPeriod];
  for (int i = 0; i < samplesPerPeriod; i++)
  {
    sineTable[i] = (int)(sin(2 * PI * i / samplesPerPeriod) * pwmRange / 2 + pwmRange / 2);
  }
  return sineTable;
}

int sineTable150Length = sampleRate / 150;
int sineTable190Length = sampleRate / 190;
int* sineTable150 = generateSineTable(150, sampleRate); // 150 Hz sine wave fo the motor on the index finger
int* sineTable190 = generateSineTable(190, sampleRate); // 190 Hz sine wave fo the motor on the index finger

void IRAM_ATTR onTimer()
{
  if (receivedValue > 0)
  {
    if(arrayPosition <= arrayLength)
    {
      if (receivedValue <= 100)
      {
        ledcWrite(0, whitenoise_data[arrayPosition] * receivedValue / 100);
      }else if (receivedValue <= 200)
      {
        ledcWrite(1, sineTable150[arrayPosition] * (receivedValue - 100) / 100);
      } else if (receivedValue <= 300)
      {
        ledcWrite(1, sineTable150[arrayPosition] * (receivedValue - 200) / 100);
      }
      arrayPosition++;
    } else
    {
      arrayPosition = 0;
    }
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
  printArray(sineTable150, sineTable150Length);
  // init interrupt timer
  timer = timerBegin(0, 80, true);
  timerAttachInterrupt(timer, &onTimer, true);
  timerAlarmWrite(timer, 1000000 / sampleRate, true);  // nombre de us (1 000 000 us = 1s pour rappel)
  timerAlarmEnable(timer);
}

void loop()
{
  if (Serial.available() > 0) {
    receivedValue = Serial.parseInt();
    Serial.println(receivedValue);
    // 501 to 506 are clicks - left to right
    if (receivedValue >= 301 && receivedValue <= 306)
    {
      
    } else if (receivedValue <= 100)
    {
      arrayPosition = 0;
      arrayLength = whitenoise_length;
    } else if (receivedValue <= 200)
    {
      arrayPosition = 0;
      arrayLength = sineTable150Length;
    } else if (receivedValue <= 300)
    {
      arrayPosition = 0;
      arrayLength = sineTable190Length;
    }
  }
}