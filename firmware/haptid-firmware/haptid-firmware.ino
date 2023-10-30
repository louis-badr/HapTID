#include "AudioTools.h"
#include "audiofile.h"
#include "alice.h"

// keep pin on HIGH to run the amp - each amp controls two motors
int shdnPins[3] = {22, 19, 4};
// in order from left to right
int motorPins[6] = {32, 33, 25, 26, 27, 12};
// tracks if audio is playing on a motor
bool motorIsPlaying[6] = {0, 0, 0, 0, 0, 0};

//Data Flow: MemoryStream -> EncodedAudioStream  -> PWMAudioOutput
AudioInfo info(8000, 1, 16);

SineWaveGenerator<int16_t> sineWave(32000); // subclass of SoundGenerator with max amplitude of 32000
GeneratedSoundStream<int16_t> sound(sineWave);  // Stream generated from sine wave
//MemoryStream wav(alice_wav, alice_wav_len);
MemoryStream wav(audiofile_raw, audiofile_raw_len);
PWMAudioOutput pwm;          // PWM output 
EncodedAudioStream out(&pwm, new WAVDecoder()); // Decoder stream

// void startPlayAudioFile(int motor, float volume) {
//   Stream copier(out, wav);
//   out.begin();
//   wav.begin();
//   auto config = pwm.defaultConfig();
//   config.copyFrom(info);
//   config.resolution = 11;
//   config.start_pin = motor;
//   pwm.begin(config); 
//   while (millis() - starttime <= duration) {
//     copier.copy();
//   }
//   digitalWrite(motor, LOW);
// }

// plays audio file on the selected motor - volume 0-1 - duration in ms 0-30000
void playAudioFile(int motor, float volume, float duration) {
  unsigned long starttime = millis();
  StreamCopy copier(out, wav);    // copy in to out
  out.begin();   // indicate that we process the WAV header
  wav.begin();       // reset actual position to 0
  auto config = pwm.defaultConfig();
  config.copyFrom(info);
  config.resolution = 11;
  config.start_pin = motor;
  pwm.begin(config); 
  while (millis() - starttime <= duration) {
    copier.copy();
  }
  digitalWrite(motor, LOW);
}

// plays a click on the selected motor 1-6 with a volume value 0-1
void playClick(int motor, int volume) {
  unsigned long starttime = millis();
  volume *= 255;
  digitalWrite(motor, volume);
  while (millis() - starttime <= 10) {}
  digitalWrite(motor, LOW);
}

// plays a tone on the selected motor - frequency (Hz) 0-20k - volume 0-1 - duration in ms 0-30000
void playTone(int motor, float volume, float duration, int frequency) {
  unsigned long starttime = millis();
  StreamCopy copier(pwm, sound);
  sineWave.begin(info, frequency);
  auto config = pwm.defaultConfig();
  config.copyFrom(info);
  config.resolution = 11;
  config.start_pin = motor;
  pwm.begin(config);
  while (millis() - starttime <= duration) {
    copier.copy();
  }
  digitalWrite(motor, LOW);
}

void playStartingSequence() {
  for (int i = 0; i <= 5; i++) {
    playClick(motorPins[i], 1);
    delay(250);
  }
  delay(250);
  for (int i = 5; i >= 0; i--) {
    playClick(motorPins[i], 1);
    delay(250);
  }
  delay(750);
  for (int i = 0; i <= 5; i++) {
    playClick(motorPins[i], 1);
  }
}

void setup() {
  Serial.begin(115200);

  for (int i = 0; i <= 2; i++) {
    pinMode(shdnPins[i], OUTPUT);
    digitalWrite(shdnPins[i], HIGH);
  }
  for (int i = 0; i <= 5; i++) {
    pinMode(motorPins[i], OUTPUT);
    digitalWrite(motorPins[i], LOW);
  }

  AudioLogger::instance().begin(Serial, AudioLogger::Info);
  wav.setLoop(true);

  delay(5000);
  playStartingSequence();
  delay(1000);
  //playAudioFile(motor6, 1, 5000);
}

void loop() {

}