const int xpin = 34;                  // x-axis of the accelerometer
const int ypin = 39;                  // y-axis
const int zpin = 36;                  // z-axis (only on 3-axis models)
int xVal = 0;
int yVal = 0;
int zVal = 0;
float xG = 0;
float yG = 0;
float zG = 0;
float meanG = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  // read values - 12-bit so between 0 and 4095
  xVal = analogRead(xpin);
  yVal = analogRead(ypin);
  zVal = analogRead(zpin);

  // to G values
  xG = map(xVal, 0, 4095, -3000, 3000);
  xG  = xG / 1000;
  yG = map(yVal, 0, 4095, -3000, 3000);
  yG = yG / 1000;
  zG = map(zVal, 0, 4095, -3000, 3000);
  zG = zG / 1000;

  // mean of G values - should = to -1G at rest
  meanG = (xG+yG+zG)/3;

  Serial.print(xG);
  Serial.print(",");
  Serial.print(yG);
  Serial.print(",");
  Serial.print(zG);
  Serial.print(",");
  Serial.print(meanG);
  Serial.println();
  delay(10);
}