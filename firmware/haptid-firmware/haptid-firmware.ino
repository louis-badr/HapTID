#include "AudioTools.h"
#include "audiofile.h"
//#include "alice.h"

unsigned long starttime;

// keep shdn on HIGH to run the amp - each amp controls two motors
int shdn1 = 22;
int motor1 = 32;
int motor2 = 33;

int shdn2 = 19;
int motor3 = 25;
int motor4 = 26;

int shdn3 = 4;
int motor5 = 27;
int motor6 = 12;

//Data Flow: MemoryStream -> EncodedAudioStream  -> PWMAudioOutput

AudioInfo info(8000, 1, 8);

SineWaveGenerator<int16_t> sineWave(32000); // subclass of SoundGenerator with max amplitude of 32000
GeneratedSoundStream<int16_t> sound(sineWave);  // Stream generated from sine wave
//MemoryStream wav(alice_wav, alice_wav_len);
MemoryStream wav(audiofile_raw, audiofile_raw_len);
PWMAudioOutput pwm;          // PWM output 
EncodedAudioStream out(&pwm, new WAVDecoder()); // Decoder stream

void setup(){
  Serial.begin(115200);

  pinMode(shdn1, OUTPUT);
  pinMode(motor1, OUTPUT);
  pinMode(motor2, OUTPUT);

  pinMode(shdn2, OUTPUT);
  pinMode(motor3, OUTPUT);
  pinMode(motor4, OUTPUT);

  pinMode(shdn3, OUTPUT);
  pinMode(motor5, OUTPUT);
  pinMode(motor6, OUTPUT);

  digitalWrite(shdn1, HIGH);
  digitalWrite(motor1, LOW);
  digitalWrite(motor2, LOW);

  digitalWrite(shdn2, HIGH);
  digitalWrite(motor3, LOW);
  digitalWrite(motor4, LOW);

  digitalWrite(shdn3, HIGH);
  digitalWrite(motor5, LOW);
  digitalWrite(motor6, LOW);

  AudioLogger::instance().begin(Serial, AudioLogger::Info);
  wav.setLoop(true);
  //playTone(motor6, 1, 5000, 440);
  playAudioFile(motor6, 1, 5000);
}

void loop(){

}

// plays audio file on the selected motor - volume 0-1 - duration in ms 0-30000
void playAudioFile(int motor, float volume, float duration){
  StreamCopy copier(out, wav);    // copy in to out
  out.begin();   // indicate that we process the WAV header
  wav.begin();       // reset actual position to 0
  auto config = pwm.defaultConfig();
  config.copyFrom(info);
  config.resolution = 11;
  config.start_pin = motor;
  pwm.begin(config); 
  starttime = millis();
  while (millis() - starttime <= duration) {
    copier.copy();
  }
  digitalWrite(motor, LOW);
}

// plays a click on the selected motor 1-6 with a volume value 0-1
void playClick(int motor, float volume){
  volume *= 255;
  digitalWrite(motor, volume);
  delay(8);
  digitalWrite(motor, LOW);
}

// plays a tone on the selected motor - frequency (Hz) 0-20k - volume 0-1 - duration in ms 0-30000
void playTone(int motor, float volume, float duration, int frequency){
  StreamCopy copier(pwm, sound);
  sineWave.begin(info, frequency);
  auto config = pwm.defaultConfig();
  config.copyFrom(info);
  config.resolution = 11;
  config.start_pin = motor;
  pwm.begin(config);
  starttime = millis();
  while (millis() - starttime <= duration) {
    copier.copy();
  }
  digitalWrite(motor, LOW);
}