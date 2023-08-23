#include "AudioTools.h"
//#include "whitenoise1s.h"
//#include "alice.h"
//#include "la440.h"
#include "200hz.h"

// Amp shutdown pins (HIGH is ON)
// int shdn1 = 34; // input only pin - doesn't work
int shdn2 = 27;
int shdn3 = 10;

// Motor Pins
// int motor1 = 33;
// int motor2 = 32;
int motor3 = 25;
int motor4 = 26;
int motor5 = 9;
int motor6 = 12;

//Data Flow: MemoryStream -> EncodedAudioStream  -> PWMAudioOutput
//Use 8000 for alice_wav and 11025 for knghtsng_wav
AudioInfo info(44100, 1, 16);
//MemoryStream wav(knghtsng_wav, knghtsng_wav_len);
//MemoryStream wav(alice_wav, alice_wav_len);
MemoryStream wav(200hz_raw, 200hz_raw_len);
//MemoryStream wav(whitenoise1s_raw, whitenoise1s_raw_len);
PWMAudioOutput pwm;          // PWM output 
EncodedAudioStream out(&pwm, new WAVDecoder()); // Decoder stream
StreamCopy copier(out, wav);    // copy in to out

void setup(){
  Serial.begin(115200);

  // Turn the amps on
  // pinMode(shdn1, OUTPUT);
  pinMode(shdn2, OUTPUT);
  pinMode(shdn3, OUTPUT);
  // digitalWrite(shdn1, HIGH);
  digitalWrite(shdn2, HIGH);
  digitalWrite(shdn3, HIGH);

  AudioLogger::instance().begin(Serial, AudioLogger::Info);  

  wav.begin();
  out.begin();

  auto config = pwm.defaultConfig();
  config.copyFrom(info);
  config.start_pin = motor3;
  pwm.begin(config);
}

void loop(){
  if (wav) {
    copier.copy();
  } else {
    // after we are done we just print some info form the wav file
    auto info = out.audioInfo();
    LOGI("The audio rate from the wav file is %d", info.sample_rate);
    LOGI("The channels from the wav file is %d", info.channels);

    // restart from the beginning
    Serial.println("Restarting...");
    delay(5000);
    out.begin();   // indicate that we process the WAV header
    wav.begin();       // reset actual position to 0
    pwm.begin();       // reset counters 
  }
}