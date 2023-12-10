#include "AudioTools.h"
//#include "caresseamp8000.h"
#include "caresseamp16000.h"
//#include "tremblement2amp16000.h"
//#include "frottement1amp16000.h"
//#include "tapotement1amp16000.h"
//#include "alice.h"

// keep pin on HIGH to run the amp - each amp controls two motors
int shdnPins[3] = {22, 19, 4};
// in order from left to right
int motorPins[6] = {32, 33, 25, 26, 27, 12};

//Data Flow: MemoryStream -> EncodedAudioStream  -> PWMAudioOutput
AudioInfo info(16000, 1, 16);

SineWaveGenerator<int16_t> sineWave(32000); // subclass of SoundGenerator with max amplitude of 32000
GeneratedSoundStream<int16_t> sound(sineWave);  // Stream generated from sine wave
MemoryStream wav(wav_data, wav_data_len);
PWMAudioOutput pwm;          // PWM output 
EncodedAudioStream out(&pwm, new WAVDecoder()); // Decoder stream

// plays audio file on the selected motor (1 to 6) - volume (0 to 1) - duration in ms (0 to 30000)
void playAudioFile(int motorNo, float volume, float duration) {
  unsigned long starttime = millis();
  StreamCopy copier(out, wav);
  out.begin();   // indicate that we process the WAV header
  wav.begin();       // reset actual position to 0
  auto config = pwm.defaultConfig();
  config.copyFrom(info);
  config.resolution = 11;
  config.start_pin = motorPins[motorNo - 1];
  pwm.begin(config); 
  while (millis() - starttime <= duration) {
    copier.copy();
  }
  digitalWrite(motorPins[motorNo - 1], LOW);
}

// plays a tone on the selected motor (1 to 6) - frequency (Hz) (0 to 20k) - volume (0 to 1) - duration in ms (0 to 30000)
void playTone(int motorNo, float volume, float duration, int frequency) {
  unsigned long starttime = millis();
  StreamCopy copier(pwm, sound);
  sineWave.begin(info, frequency);
  auto config = pwm.defaultConfig();
  config.copyFrom(info);
  config.resolution = 11;
  config.start_pin = motorPins[motorNo - 1];
  pwm.begin(config);
  if (duration > 30000) { duration = 30000;}
  while (millis() - starttime <= duration) {
    copier.copy();
  }
  digitalWrite(motorPins[motorNo - 1], LOW);
}

// plays a click on the selected motor (1 to 6) at volume (0 to 1)
void playClick(int motorNo, int volume) {
  unsigned long starttime = millis();
  volume *= 255;
  digitalWrite(motorPins[motorNo - 1], volume);
  while (millis() - starttime <= 10) {}
  digitalWrite(motorPins[motorNo - 1], LOW);
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

void setup() {
  Serial.begin(115200);
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

  delay(5000);
  playStartingSequence();
  delay(1000);
  playAudioFile(1, 1, 30000);
}

void loop() {}