#include <Arduino.h>
#include "whitenoise.h"

const int shdnPins[3] = {22, 19, 4};  // keep pin on HIGH to run the amp - each amp controls two motors
const int motorPins[6] = {32, 33, 25, 26, 27, 12};  // in order from left to right

const int pwmRes = 12;
const int sampleRate = 16000;
const int pwmMax = pow(2, pwmRes) - 1;
const int pwmFreq = (8 * pow(10, 7)) / pow(2, pwmRes);  // 80 MHz / 2^12 = 19531.25 Hz > sampleRate

hw_timer_t * timer = NULL;  // we only need one timer since the sample rate is the same for all sounds

const int clickDuration = 10;  // length of the click in ms
const int sineClickDuration = 50; // length of the sine click in ms
int sineClickArrayPosition = 0;  // position for the sine click - the length of the array is fixed
int wristArrayPosition = 0;  // position in the array being played
int fingerArrayPosition = 0;
int fingerArrayLength = 0;  // length of the array being played

int receivedValue = 0;  // value received from the serial port
int wristValue = 0;
int fingerValue = 0;

int clickOutput = -1;
int clickVolume;
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

int sineTable80Length = sampleRate / 80;
int sineTable250Length = sampleRate / 250;
uint16_t* sineTable80 = generateSineTable(80, sampleRate); // 80 Hz sine wave for the motor on the index finger
uint16_t* sineTable250 = generateSineTable(250, sampleRate); // 250 Hz sine wave for the sine click

// Interrupt function to play the noise and the sine waves
void IRAM_ATTR onTimer()
{
  if (wristValue > 0 && wristValue <= 100000)
  {
    ledcWrite(0, whitenoise_data[wristArrayPosition] * wristValue / 100000);
    wristArrayPosition++;
    if (wristArrayPosition >= whitenoise_length)
    {
      wristArrayPosition = 0;
    }
  }
  if (fingerValue > 0)
  {
    if (fingerValue <= 200000)
    {
      ledcWrite(2, sineTable80[fingerArrayPosition] * (fingerValue - 100000) / 100000);
    } else if (fingerValue <= 300000)
    {
      ledcWrite(4, sineTable80[fingerArrayPosition] * (fingerValue - 200000) / 100000);
    } else if (fingerValue <= 400000)
    {
      ledcWrite(2, sineTable250[fingerArrayPosition] * (fingerValue - 300000) / 100000);
    } else if (fingerValue <= 500000)
    {
      ledcWrite(4, sineTable250[fingerArrayPosition] * (fingerValue - 400000) / 100000);
    } else if (fingerValue <= 600000)
    {
      ledcWrite(4, sineTable250[fingerArrayPosition] * (fingerValue - 500000) / 100000);
    }
    fingerArrayPosition++;
    if(fingerArrayPosition >= fingerArrayLength)
    {
      fingerArrayPosition = 0;
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
  Serial.setTimeout(1);
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
    if (receivedValue == 0)
    {
      wristValue = 0;
      fingerValue = 0;
      for (int i = 0; i <= 5; i++)
      {
        ledcWrite(i, 0);
      }
    } else if (receivedValue < 0)  // -1 to -700000 are clicks, -700001 to -1300000 are sine clicks
    {
      if (receivedValue < -700000){
        sineClickOutput = -receivedValue/100000 - 7;
        sineClickVolume = -receivedValue % 100000;
        sineClickArrayPosition = 0;
      } else
      {
        clickOutput = -receivedValue/100000;
        clickVolume = -receivedValue % 100000;
        if (clickOutput != 6)
        {
          ledcWrite(clickOutput, 0);
          ledcWrite(clickOutput, pwmMax * clickVolume / 100000.0);
        } else
        {
          for (int i = 1; i <= 5; i++)
          {
            ledcWrite(i, 0);
            ledcWrite(i, pwmMax * clickVolume / 100000.0);
          }
        }
      }
      // set the click time
      clickTimer = millis();
    } else 
    {
      if (receivedValue <= 100000)
      {
        wristValue = receivedValue;
        wristArrayPosition = 0;
      } else if (receivedValue <= 300000)
      {
        fingerValue = receivedValue;
        fingerArrayPosition = 0;
        fingerArrayLength = sineTable80Length;
      } else if (receivedValue <= 500000)
      {
        fingerValue = receivedValue;
        fingerArrayPosition = 0;
        fingerArrayLength = sineTable250Length;
      }
    }
  }
  // if the motor is clicking
  if (clickOutput != 0)
  {
    // if more than X ms have passed since the click
    if (millis() - clickTimer >= clickDuration)
    {
      // turn off the motor
      if (clickOutput != 6)
      {
        ledcWrite(clickOutput, 0);
      } else
      {
        for (int i = 1; i <= 5; i++)
        {
          ledcWrite(i, 0);
        }
      }
      // set the motor to not clicking
      clickOutput = -1;
      clickVolume = 0;
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