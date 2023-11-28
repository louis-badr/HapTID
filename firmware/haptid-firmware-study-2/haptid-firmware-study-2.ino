#include "AudioTools.h"
#include "whitenoise16000.h"


const int shdnPins[3] = {22, 19, 4};  // keep pin on HIGH to run the amp - each amp controls two motors
const int motorPins[6] = {32, 33, 25, 26, 27, 12};  // in order from left to right

int receivedValue = 0;  // single int value received from serial between 0 and 506
bool playNoise = false;
bool playTone = false;
unsigned long clickTimer;
bool isClicking = false;
int motorClicking;

AudioInfo info(16000, 1, 16);
SineWaveGenerator<int16_t> sineWave(32000); // subclass of SoundGenerator with max amplitude of 32000
GeneratedSoundStream<int16_t> sineTone(sineWave);  // Stream generated from sine wave
MemoryStream wav(wav_data, wav_data_len);
PWMAudioOutput pwm;          // PWM output 
EncodedAudioStream out(&pwm, new WAVDecoder()); // Decoder stream

StreamCopy copierTone(pwm, sineTone);
StreamCopy copierWav(out, wav);
PWMConfig config = pwm.defaultConfig();

void setup() {
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
  AudioLogger::instance().begin(Serial, AudioLogger::Info);
  out.begin();
  wav.setLoop(true);
  wav.begin();
  config.sample_rate = 16000;
  config.channels = 1;
  config.bits_per_sample = 16;
  config.resolution = 11;
}

void loop() {
  if (Serial.available() > 0) {
    receivedValue = Serial.parseInt();
    Serial.println(receivedValue);
    // 501 to 506 are clicks - left to right
    if (receivedValue >= 501 && receivedValue <= 506) {
      digitalWrite(motorPins[receivedValue - 501], HIGH);
      clickTimer = millis();
      isClicking = true;
      motorClicking = receivedValue - 501;
    }
    // 200 to 300 or 400 to 500 for volume of low frequency tone on index finger
    if (receivedValue >= 200 && receivedValue <= 500) {
      if (receivedValue == 200 || receivedValue == 400) {
        digitalWrite(motorPins[5], LOW);
        playTone = false;
      } else if (receivedValue <= 300) {
        sineWave.begin(info, 140);
        config.pins()[0] = 27;
        pwm.begin(config);
        playTone = true;
      } else if (receivedValue <= 500) {
        config.pins()[0] = 27;
        pwm.begin(config);   
        playTone = true;
      }
    }
    // 0 to 100 for volume of noise on motor 1
    if (receivedValue >= 0 && receivedValue <= 100) {
      if (receivedValue == 0) {
        digitalWrite(motorPins[0], LOW);
        playNoise = false;
      } else {
        config.pins()[0] = 32;
        pwm.begin(config);
        playNoise = true; 
      }
    }
  }
  if (playNoise) {
    copierWav.copy();
  }
  if (playTone) {
    copierTone.copy();
  }
  if (isClicking && millis() - clickTimer >= 10) {
    digitalWrite(motorPins[motorClicking], LOW);
    isClicking = false;
  }
}