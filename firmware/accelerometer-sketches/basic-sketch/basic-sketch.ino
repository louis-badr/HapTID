const int xpin = 34;                  // x-axis of the accelerometer
const int ypin = 39;                  // y-axis
const int zpin = 36;                  // z-axis (only on 3-axis models)
int xG = 0;
int yG = 0;
int zG = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  xG = analogRead(xpin);
  yG = analogRead(ypin);
  zG = analogRead(zpin);
  Serial.print(xG);
  Serial.print(",");
  Serial.print(yG);
  Serial.print(",");
  Serial.print(zG);
  Serial.println();
  delay(10);
}