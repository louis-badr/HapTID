#include <Arduino.h>

const int adcResolution = 10;
const float adcRange = pow(2, adcResolution) - 1;

const int xPin = A12;
const int yPin = A11;
const int zPin = A10;

// Number of samples for readAxis
const int sampleSize = 100;

// Rest values for each axis
float xRest = 0, yRest = 0, zRest = 0;

bool streaming = false;
bool centered = false;

struct axesVal
{
  float x;
  float y;
  float z;
};

// Read the value of each axis at rest (average of sampleSize samples)
int readStableAxis(int axisPin)
{
  long reading = 0;
  for (int i = 0; i <= sampleSize; i++)
  {
    reading += analogRead(axisPin);
  }
  return reading/sampleSize;
}

// Calibrate all axes by reading the value at rest
axesVal calibrateAllAxes()
{
  // Serial.println("Calibration started");
  // for each axis read the value at rest
  xRest = readStableAxis(xPin);
  yRest = readStableAxis(yPin);
  zRest = readStableAxis(zPin);
  // convert raw values to G between -3 and 3 G (ADXL335)
  xRest = (xRest / adcRange) * 6.0 - 3.0;
  yRest = (yRest / adcRange) * 6.0 - 3.0;
  zRest = (zRest / adcRange) * 6.0 - 3.0;
  // Serial.println("Calibration Done");
  return {xRest, yRest, zRest};
}

// Read raw value of all axes
axesVal readAllAxesRaw()
{
  // read raw values
  float xRaw = analogRead(xPin);
  float yRaw = analogRead(yPin);
  float zRaw = analogRead(zPin);
  return {xRaw, yRaw, zRaw};
}

// Read the value of all axes in G
axesVal readAllAxesG()
{
  axesVal axesRaw = readAllAxesRaw();
  // convert raw values to G between -3 and 3 G (ADXL335)
  float xG = (axesRaw.x / adcRange) * 6.0 - 3.0;
  float yG = (axesRaw.y / adcRange) * 6.0 - 3.0;
  float zG = (axesRaw.z / adcRange) * 6.0 - 3.0;
  return {xG, yG, zG};
}

// Read the value of all axes centered on rest value
axesVal readAllAxesCentered()
{
  axesVal axesG = readAllAxesG();
  // center values
  float xCentered = axesG.x - xRest;
  float yCentered = axesG.y - yRest;
  float zCentered = axesG.z - zRest;
  return {xCentered, yCentered, zCentered};
}

// Print the value of all axes
void printAllAxes(axesVal axesVal)
{
  Serial.print(.25);
  Serial.print(",");
  Serial.print(-0.25);
  Serial.print(",");
  //Serial.print("xG:");
  Serial.print(axesVal.x, 4);
  Serial.print(",");
  //Serial.print("yG:");
  Serial.print(axesVal.y, 4);
  Serial.print(",");
  //Serial.print("zG:");
  Serial.println(axesVal.z, 4);
}

// Read acceleration on all axes
float readAcceleration(axesVal axesVal)
{
  return sqrt(pow(axesVal.x, 2) + pow(axesVal.y, 2) + pow(axesVal.z, 2));
}


void setup() 
{
  //Serial.begin(38400);
  analogReadResolution(adcResolution);
}

void loop() 
{
  if (Serial.available() > 0) 
  {
    char incomingByte = Serial.read();
    // Serial.print("Received : ");
    // Serial.println(incomingByte);

    // Calibration
    if((int)incomingByte == '1')
    {
      calibrateAllAxes();
    }
    // Start or stop streaming G value of all axis
    if((int)incomingByte == '2')
    {
      if(streaming)
      {
        streaming = false;
        centered = false;
        Serial.println("Streaming G values stopped\n");
      }
      else
      {
        streaming = true;
        Serial.println("Streaming G values started\n");
      }
    }
    // Start or stop streaming centered G value of all axis - please run the calibration first
    if((int)incomingByte == '3')
    {
      if(streaming)
      {
        streaming = false;
        centered = false;
        Serial.println("Streaming centered values stopped\n");
      }
      else
      {
        streaming = true;
        centered = true;
        Serial.println("Streaming centered values started\n");
      }
    }
    // Read acceleration
    if((int)incomingByte == '4')
    {
      // Serial.print("Acceleration:");
      Serial.print(readAcceleration(readAllAxesCentered()), 4);
    }
  }

  if (streaming)
  {
    if(centered)
    {
      printAllAxes(readAllAxesCentered());
    }
    else
    {
      printAllAxes(readAllAxesG());
    }
    delay(.1);
  }
}