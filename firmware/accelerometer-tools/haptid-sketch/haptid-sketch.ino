#include "Arduino.h"

const int pwmRes = 14;
const int sampleRate = 4000;

const int shdnPins[3] = {22, 19, 4};  // keep pin on HIGH to run the amp - each amp controls two motors
const int motorPins[6] = {32, 33, 25, 26, 27, 12};  // in order from left to right

const int pwmMax = pow(2, pwmRes) - 1;
const int pwmFreq = (8 * pow(10, 7)) / pow(2, pwmRes);  // 80 MHz / 2^13 = 9765.625 Hz > sampleRate

hw_timer_t * timer = NULL;

uint16_t sineTable[sampleRate] = {0};
int arrayPosition = 0;
int arrayLength = 0;

int receivedValue = 0;

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


// Interrupt function to play the signals
void IRAM_ATTR onTimer()
{
  if (receivedValue > 0)
  {
    if (arrayPosition < arrayLength)
    {
      ledcWrite(5, sineTable[arrayPosition]);
      arrayPosition++;
    }
    else
    {
      arrayPosition = 0;
    }
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
    // on reçoit un entier entre 100000 et 99999999
    // les trois premiers chiffres donnent la fréquence du signal de 1 à 999 Hz
    // les chiffres suivants donnent le volume du signal de 0 à 99.999
    receivedValue = Serial.parseInt();
    Serial.print("Received: ");
    Serial.println(receivedValue);
    if (receivedValue == 0)
    {
      for (int i = 0; i <= 5; i++)
      {
        ledcWrite(i, 0);
      }
      Serial.println("Stopping tone");
    }
    else if (receivedValue >= 100000 && receivedValue <= 99999999)
    {
      int receivedFreq = receivedValue / 100000;
      int receivedVol = receivedValue % 100000;
      arrayLength = sampleRate / receivedFreq;
      // clear the old sine table
      for (int i = 0; i < arrayLength; i++)
      {
        sineTable[i] = 0;
      }
      // generate a new sine table
      for (int i = 0; i < arrayLength; i++)
      {
        sineTable[i] = (uint16_t)(sin(2 * PI * i / arrayLength) * pwmMax / 2 + pwmMax / 2);
      }
      // apply the volume
      for (int i = 0; i < arrayLength; i++)
      {
        sineTable[i] = (uint16_t)(sineTable[i] * receivedVol / 100000);
      }
      Serial.print("Playing tone at ");
      Serial.print(receivedFreq);
      Serial.print(" Hz with volume ");
      Serial.print(receivedVol / 1000.0);
      Serial.println("%");
    }
    else
    {
      Serial.println("Invalid value");
    }
  }
}