#include "AudioTools.h"
#include "whitenoise8000.h"

// keep pin on HIGH to run the amp - each amp controls two motors
int shdnPins[3] = {22, 19, 4};
// in order from left to right
int motorPins[6] = {32, 33, 25, 26, 27, 12};

//Data Flow: MemoryStream -> EncodedAudioStream  -> PWMAudioOutput
AudioInfo info(8000, 1, 16);
SineWaveGenerator<int16_t> sineWave(32000); // subclass of SoundGenerator with max amplitude of 32000
//GeneratedSoundStream<int16_t> tone(sineWave);  // Stream generated from sine wave
MemoryStream wav(wav_data, wav_data_len);
PWMAudioOutput pwm;          // PWM output 
EncodedAudioStream out(&pwm, new WAVDecoder()); // Decoder stream

// on crée un copier pour chaque type de son - un pour le bruit, un pour les sinusoïdes
StreamCopy copierWav(out, wav);
PWMConfig config = pwm.defaultConfig();
//StreamCopy copierTone(pwm, tone);

int receivedValue = 0;
unsigned long clickTimer;
bool playNoise = false;
bool playLowTone = false;
bool playHighTone = false;
bool isClicking = false;

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
  wav.setLoop(true);
  out.begin();   // indicate that we process the WAV header
  wav.begin();       // reset actual position to 0
  delay(3000);
}

void loop() {
  if (Serial.available() > 0) {
    receivedValue = Serial.parseInt();
    Serial.println(receivedValue);
    // 501 to 506 are clicks - left to right
    if (receivedValue >= 501 && receivedValue <= 506) {
      digitalWrite(motorPins[receivedValue - 500], HIGH);
      clickTimer = millis();
      isClicking = true;
    }
    // 200 to 300 for volume of low frequency tone on index finger
    if (receivedValue >= 200 && receivedValue <= 300) {}
    // 0 to 100 for volume of noise on motor 1
    if (receivedValue > 0 && receivedValue <= 100) {
      config.sample_rate = 8000;
      config.channels = 1;
      config.bits_per_sample = 16;
      config.resolution = 11;
      playNoise = true;
      config.start_pin = motorPins[0];
      pwm.begin(config); 
    }

    // stop noise on motor 1
    if (receivedValue == 0) {
      Serial.println("Stop noise");
      playNoise = false;
      digitalWrite(motorPins[0], LOW);
    }
  }
  // if noise is activated, play noise on motor 1
  if (playNoise) {
    copierWav.copy();
  }
  if (isClicking && millis() - clickTimer >= 8) {
    digitalWrite(motorPins[1], LOW);
    isClicking = false;
  }
}