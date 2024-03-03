#include <Arduino.h>
#include "whitenoise.h"
// #include "sample.h"
// #include "tone150.h"
// #include "ring.h"


const int pwmRes = 12;
const int sampleRate = 16000;
const int clickDuration = 7;  // length of the click in ms
const int sineClickDuration = 50; // length of the sine click in ms

const int shdnPins[3] = {22, 19, 4};  // keep pin on HIGH to run the amp - each amp controls two motors
const int motorPins[6] = {32, 33, 25, 26, 27, 12};  // in order from left to right

const int pwmMax = pow(2, pwmRes) - 1;
const int pwmFreq = (8 * pow(10, 7)) / pow(2, pwmRes);  // 80 MHz / 2^12 = 19531.25 Hz > sampleRate

int arrayPosition = 0;  // position in the array being played
int arrayLength = 0;  // length of the array being played
int sineClickArrayPosition = 0;  // position for the sine click - the length of the array is fixed

hw_timer_t * timer = NULL;  // we only need one timer since the sample rate is the same for all sounds

int receivedValue = 0;  // value received from the serial port
int soundValue = 0;
int clickValue;
int sineClickOutput = -1;
int sineClickVolume;
unsigned long clickTimer = 0;

// Debugging function to print an array
void printArray(uint16_t arr[], int size) {
  for (int i = 0; i < size; i++) {
    Serial.print(arr[i]);
    Serial.print(" ");
  }
  Serial.println();
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
int sineTable250Length = sampleRate / 250;
uint16_t* sineTable150 = generateSineTable(150, sampleRate); // 150 Hz sine wave for the motor on the index finger
uint16_t* sineTable190 = generateSineTable(190, sampleRate); // 190 Hz sine wave for the motor on the index finger
uint16_t* sineTable250 = generateSineTable(250, sampleRate); // 250 Hz sine wave for the sine click

// Interrupt function to play the noise and the sine waves
void IRAM_ATTR onTimer()
{
  if (soundValue > 0)
  {
    if(arrayPosition < arrayLength)
    {
      if (soundValue <= 100000)
      {
        ledcWrite(0, whitenoise_data[arrayPosition] * soundValue / 100000);
      }else if (soundValue <= 200000)
      {
        ledcWrite(2, sineTable150[arrayPosition] * (soundValue - 100000) / 100000);
      } else if (soundValue <= 300000)
      {
        ledcWrite(4, sineTable150[arrayPosition] * (soundValue - 200000) / 100000);
      } else if (soundValue <= 400000)
      {
        ledcWrite(2, sineTable190[arrayPosition] * (soundValue - 300000) / 100000);
      } else if (soundValue <= 500000)
      {
        ledcWrite(4, sineTable190[arrayPosition] * (soundValue - 400000) / 100000);
      } else if (soundValue <= 600000)
      {
        ledcWrite(4, sineTable190[arrayPosition] * (soundValue - 500000) / 100000);
      }
      arrayPosition++;
    } else
    {
      arrayPosition = 0;
    }
  }
  if (sineClickVolume > 0)
  {
    if (sineClickArrayPosition < sineTable250Length)
    {
      ledcWrite(sineClickOutput, sineTable250[sineClickArrayPosition] * sineClickVolume / 100000.0);
      sineClickArrayPosition++;
    } else
    {
      sineClickArrayPosition = 0;
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
  
  delay(2000);
  playStartSequence();
}

void loop()
{
  if (Serial.available() > 0)
  {
    receivedValue = Serial.parseInt();
    // Serial.println(receivedValue);
    // -1 to -7 are clicks, -700001 to -1300000 are sine clicks
    if (receivedValue < 0)
    {
      if (receivedValue < -7){
        sineClickOutput = -receivedValue/100000 - 7;
        sineClickVolume = -receivedValue % 100000;
        sineClickArrayPosition = 0;
      } else
      {
        clickValue = abs(receivedValue) - 1;
        if (clickValue != 6)
        {
          ledcWrite(clickValue, 0);
          ledcWrite(clickValue, pwmMax);
        } else
        {
          for (int i = 1; i <= 5; i++)
          {
            ledcWrite(i, 0);
            ledcWrite(i, pwmMax);
          }
        }
      }
      // set the click time
      clickTimer = millis();
    } else 
    {
      soundValue = receivedValue;
      if (soundValue <= 100000)
      {
        arrayPosition = 0;
        arrayLength = whitenoise_length;
      } else if (soundValue <= 300000)
      {
        arrayPosition = 0;
        arrayLength = sineTable150Length;
      } else if (soundValue <= 500000)
      {
        arrayPosition = 0;
        arrayLength = sineTable190Length;
      }
    }
  }
  // if the motor is clicking
  if (clickValue != 0)
  {
    // if more than X ms have passed since the click
    if (millis() - clickTimer >= clickDuration)
    {
      // turn off the motor
      if (clickValue != 6)
      {
        ledcWrite(clickValue, 0);
      } else
      {
        for (int i = 1; i <= 5; i++)
        {
          ledcWrite(i, 0);
        }
      }
      // set the motor to not clicking
      clickValue = 0;
    }
  }
  // if the motor is sine clicking
  if (sineClickOutput != -1)
  {
    if (millis() - clickTimer >= sineClickDuration)
    {
      // turn off the motor
      ledcWrite(sineClickOutput, 0);
      // set the motor to not clicking
      sineClickOutput = -1;
      sineClickVolume = 0;
    }
  }
}