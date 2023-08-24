#include "AudioTools.h"
#include "whitenoise1s.h"
#include "click.h"

unsigned long starttime;
unsigned long endtime;

uint16_t sample_rate=44100;
uint8_t channels = 1;

I2SStream out1;
I2SStream out2;
MemoryStream noise(whitenoise1s_raw, whitenoise1s_raw_len);
MemoryStream click(click_raw, click_raw_len);
SineWaveGenerator<int16_t> sineWave(32000);
GeneratedSoundStream<int16_t> sine(sineWave);

void setup() {
  Serial.begin(115200);
  AudioLogger::instance().begin(Serial, AudioLogger::Info);

  auto config1 = out1.defaultConfig(TX_MODE);
  config1.i2s_format = I2S_LSB_FORMAT;
  config1.port_no = 0;
  config1.sample_rate = sample_rate;
  config1.channels = channels;
  config1.bits_per_sample = 16;
  config1.pin_bck = 33;
  config1.pin_ws = 32;
  config1.pin_data = 25;
  out1.begin(config1);

  auto config2 = out2.defaultConfig(TX_MODE);
  config2.i2s_format = I2S_LSB_FORMAT;
  config2.port_no = 1;
  config2.sample_rate = sample_rate;
  config2.channels = channels;
  config2.bits_per_sample = 16;
  config2.pin_bck = 22;
  config2.pin_ws = 23;
  config2.pin_data = 1;
  out2.begin(config2);

  noise.setLoop(true);
  click.setLoop(true);
}

void loop() {
  // Wait for incoming data
  while (!Serial.available()) {}

  // Read data into buffer
  uint8_t buf[20];
  int len = Serial.readBytes(buf, sizeof(buf));

  // Decode parameters
  int motor, type, freq, vol;
  float duration;
  if (len == sizeof(buf)) {
    struct {
      int32_t p1, p2, p3;
      float p4, p5;
    } *params = reinterpret_cast<decltype(params)>(buf);
    motor = params->p1;
    type = params->p2;
    freq = params->p3;
    vol = params->p4;
    duration = params->p5;
  }
  switch (type) {
    case 1:
      playTone(motor,freq,vol,duration);
      break;
    case 2:
      playNoise(motor,vol,duration);
      break;
    case 3:
      playClicks(motor,freq,vol,duration);
      break;
  }
}

// plays a tone (sine wave)
void playTone(int motor, int freq, float vol, float duration) {
  ConverterScaler<int16_t> volume(vol/100, 0, 32767);
  StreamCopy copier1(out1, sine);
  StreamCopy copier2(out2, sine);
  sineWave.begin(channels, sample_rate, freq);
  starttime = millis();
  endtime = starttime;
  while ((endtime - starttime) <= duration * 1000) {
    if (motor == 1) {
      copier1.copy(volume);
    }
    else {
      copier2.copy(volume);
    }
    endtime = millis();
  }
}

// plays recorded white noise (low-pass filtered at 500Hz)
void playNoise(int motor, float vol, float duration) {
  ConverterScaler<int16_t> volume(vol/100, 0, 32767);
  StreamCopy copier1(out1, noise);
  StreamCopy copier2(out2, noise);
  starttime = millis();
  endtime = starttime;
  while ((endtime - starttime) <= duration * 1000) {
    if (motor == 1) {
      copier1.copy(volume);
    }
    else {
      copier2.copy(volume);
    }
    endtime = millis();
  }
}

void playClicks(int motor, int nb, float vol, float spacing) {
  ConverterScaler<int16_t> volume(vol/100, 0, 32767);
  StreamCopy copier1(out1, click);
  StreamCopy copier2(out2, click);
  for (int i=0; i<nb; i++) {
    starttime = millis();
    endtime = starttime;
    while ((endtime - starttime) <= 0.1) {
      if (motor == 1) {
        copier1.copy(volume);
      }
      else {
        copier2.copy(volume);
      }
      endtime = millis();
    }
    delay(spacing*1000);
  }
}