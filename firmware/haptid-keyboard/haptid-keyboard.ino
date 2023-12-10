int framerate = 144;
float delayFsr = 1000/framerate;

int randomFinger;
int pressedFinger;

unsigned long startTime;
unsigned long elapsedTime;

int pressThreshold = 300; // FSR reading value over which it is counted as a press
int fsrReading;      // analog reading from the FSR resistor divider
unsigned long fsrVoltage; // analog reading converted to voltage
unsigned long fsrResistance; // voltage converted to resistance
double force;

char receivedChar;

void setup(void) {
  Serial.begin(115200);   // We'll send debugging information via the Serial monitor
}

void loop(void) {
  if (Serial.available() > 0) {
    receivedChar = Serial.read();
    if (receivedChar == 'C') {
      readInputCRT();
    }
    else if (receivedChar == 'F') {
      startStreamFSR(10);
    }
  }
}

// Choice Reaction Time (CRT)
// fonction on attend qu'un FSR soit pressé - on retourne quel FSR a été pressé et le temps entre le début de la lecture et l'appui
void readInputCRT() {
  bool keepReading = true;
  randomFinger = random(5);
  // on démarre le timer
  startTime = micros();
  // on lit en boucle chaque FSR
  while(keepReading) {
    for (int i = 0; i <= 4; i++) {
      fsrReading = analogRead(i);
      //Serial.println(fsrReading);
      if (fsrReading >= pressThreshold) {
        elapsedTime = micros() - startTime;
        pressedFinger = i;
        keepReading = false;
        break;
      }
    }
  }
  // on print le résultat
  Serial.print(pressedFinger);
  Serial.print(";");
  Serial.println(elapsedTime/1000);
}

// Force Control
// fonction pour streamer la valeur de l'index convertie en force pendant X secondes
void startStreamFSR(float sec) {
  // start the timer
  startTime = micros();
  // for the next X seconds
  while(micros() - startTime <= sec * 1000000) {
    // read the analog pin
    fsrReading = analogRead(0);
    // analog voltage reading ranges from 0 to 1023 which is mapped from 0 to 5V (= 5000mV)
    fsrVoltage = map(fsrReading, 0, 1023, 0, 5000);
    if (fsrVoltage != 0) {
      fsrResistance = 5000 - fsrVoltage;
      fsrResistance *= 10000; // 10k resistor
      fsrResistance /= fsrVoltage;
      force = 6570*pow(fsrResistance,-0.738);
    }
    else {
      force = 0;
    }
    Serial.println(force);
    delay(delayFsr);
  }
}