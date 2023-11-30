#include <Arduino.h>
#include "AudioTools.h"

bool playTone = false;

const int shdnPins[3] = {22, 19, 4};  // keep pin on HIGH to run the amp - each amp controls two motors
const int motorPins[6] = {32, 33, 25, 26, 27, 12};  // in order from left to right

AudioInfo info(16000, 1, 16);
SineWaveGenerator<int16_t> sineWave(32000); // subclass of SoundGenerator with max amplitude of 32000
GeneratedSoundStream<int16_t> sineTone(sineWave);  // Stream generated from sine wave
VolumeStream volume(sineTone);
LinearVolumeControl lvc;
PWMAudioOutput pwm;          // PWM output
StreamCopy copier(pwm, sineTone);
PWMConfig config = pwm.defaultConfig();

void setup()
{
    Serial.begin(115200);
    Serial.setTimeout(10);
    // init shdn pins and turn on amps
    for (int i = 0; i <= 2; i++) {
    pinMode(shdnPins[i], OUTPUT);
    digitalWrite(shdnPins[i], HIGH);
    }
    // init motor pins and turn off motors
    for (int i = 0; i <= 5; i++) {
    pinMode(motorPins[i], OUTPUT);
    digitalWrite(motorPins[i], LOW);
    }
    config.sample_rate = 16000;
    config.channels = 1;
    config.bits_per_sample = 16;
    config.resolution = 11;
    config.start_pin = motorPins[0];
    volume.setVolumeControl(lvc);
    volume.begin(config);
    pwm.begin(config);
}

void loop()
{
    if (Serial.available() > 0)
    {
        int receivedValue = Serial.parseInt();
        Serial.print("Received: ");
        Serial.println(receivedValue);
        if (receivedValue > 0 && receivedValue <= 20000)
        {
            playTone = true;
            Serial.print("Playing tone at ");
            Serial.print(receivedValue);
            Serial.println(" Hz");
            volume.setVolume(0.5);
            sineWave.begin(info, receivedValue);
        }
        else if (receivedValue == 0)
        {
            playTone = false;
            Serial.println("Stopping tone");
        }
        else
        {
            Serial.println("Invalid value");
        }
    }
    if (playTone)
    {
        copier.copy();
    }
}