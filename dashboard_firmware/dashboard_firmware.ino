#include "Arduino.h"

const int pwmRes = 13;
const int sampleRate = 8000;
const int maxSignalDuration = 3000;  // max length of the signal in ms
const int clickDuration = 7;  // length of the click in ms

const int shdnPins[3] = {22, 19, 4};  // keep pin on HIGH to run the amp - each amp controls two motors
const int motorPins[6] = {32, 33, 25, 26, 27, 12};  // in order from left to right

const int pwmMax = pow(2, pwmRes) - 1;
const int pwmFreq = (8 * pow(10, 7)) / pow(2, pwmRes);  // 80 MHz / 2^13 = 9765.625 Hz > sampleRate

hw_timer_t * timer = NULL;

bool listening = false;
int currentMotor = 1;
bool playSignal = false;
int signalDataArrayPosition = 0;
int signalDataArrayLength = 0;
uint16_t signalData[maxSignalDuration*sampleRate/1000] = {0};

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
  if (playSignal)
  {
    if (signalDataArrayPosition < signalDataArrayLength)
    {
      ledcWrite(currentMotor, signalData[signalDataArrayPosition]);
      signalDataArrayPosition++;
    }
    else
    {
      signalDataArrayPosition = 0;
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
    if (listening)
    {
      int receivedInt = Serial.parseInt();
      // Serial.print('k');
      // Serial.print("Received int while listening: ");
      // Serial.println(receivedInt);
      if (receivedInt < 0)
      {
        listening = false;
        Serial.println("Stop Listening");
        // print the signal
        // for (int i = 0; i < signalDataArrayLength; i++)
        // {
        //   Serial.println(signalData[i]);
        // }
        // print the signal length
        Serial.print("Signal length: ");
        Serial.print(signalDataArrayLength);
      }
      else
      {
        signalData[signalDataArrayLength] = receivedInt;
        signalDataArrayLength++;
      }
    }
    else
    {
      char receivedChar = Serial.read(); // Read the character once
      // Serial.print("Received char: ");
      // Serial.println(receivedChar);
      // if we receive 'S', for Stop, we stop the motors
      if (receivedChar == 'S')
      {
        playSignal = false;
        Serial.println("Stop Playing");
      }
      // if we receive 'L', for Load, we start listening for the signal
      else if (receivedChar == 'L')
      {
        Serial.println("Start Listening");
        signalDataArrayLength = 0;
        signalDataArrayPosition = 0;
        // clear the signal array
        for (int i = 0; i < maxSignalDuration*sampleRate/1000; i++)
        {
          signalData[i] = 0;
        }
        listening = true;
      }
      // if we receive a value between 1 and 6, we play the signal on the corresponding motor
      else
      {
        Serial.print("Playing on motor ");
        Serial.println(receivedChar);
        // check if the motor number is valid
        if (receivedChar >= '1' && receivedChar <= '6')
        {
          currentMotor = receivedChar - '1';
          playSignal = true;
        }
      }
    }
  }
}