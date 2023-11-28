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

struct axesG
{
  float x;
  float y;
  float z;
};

// Read an accurate value of an axis at rest (average of sampleSize samples)
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
void calibrateAllAxes()
{
  Serial.println("Calibration started");
  // for each axis read the value at rest
  xRest = readStableAxis(xPin);
  yRest = readStableAxis(yPin);
  zRest = readStableAxis(zPin);
  Serial.println("Calibration Done");
  // print the values
  Serial.print("Values at rest > x: ");
  Serial.print(xRest);
  Serial.print(" y: ");
  Serial.print(yRest);
  Serial.print(" z: ");
  Serial.print(zRest);
  Serial.println("\n");
}

// Read the value of all axes in G
axesG readAllAxesG()
{
  // read raw values
  float xRaw = analogRead(xPin);
  float yRaw = analogRead(yPin);
  float zRaw = analogRead(zPin);
  // center values around rest values and convert to G (+- 3G for ADXL335)
  float xG = ((xRaw - xRest) / adcRange) * 6.0;
  float yG = ((yRaw - yRest) / adcRange) * 6.0;
  float zG = ((zRaw - zRest) / adcRange) * 6.0;
  return {xG, yG, zG};
}

// Print the value of all axes in G
void printAllAxesG(axesG axesG)
{
  Serial.print("xG:");
  Serial.print(axesG.x);
  Serial.print(",");
  Serial.print("yG:");
  Serial.print(axesG.y);
  Serial.print(",");
  Serial.print("zG:");
  Serial.println(axesG.z);
}

// Measure the vibration intensity during duration milliseconds
float measureVibrationIntensity(uint32_t duration)
{
  float sumX = 0, sumY = 0, sumZ = 0;
  unsigned long startTime = millis();
  int count = 0;
  // during 3 seconds
  while (millis() - startTime <= duration)
  {
    // read the value of all axes
    axesG axesG = readAllAxesG();
    // sum the absolute value of each axis
    sumX += abs(axesG.x);
    sumY += abs(axesG.y);
    sumZ += abs(axesG.z);
    count++;
  }
  // average the sum of each axis
  float avgX = sumX / count;
  float avgY = sumY / count;
  float avgZ = sumZ / count;
  float avgAll = (avgX + avgY + avgZ) / 3; 
  return avgAll;
}

void setup() 
{
  //Serial.begin(38400);
  analogReadResolution(adcResolution);
}

void loop() 
{
  char startByte = '0';
  if (Serial.available() > 0) 
  {
    startByte = Serial.read();
    Serial.print("Received : ");
    Serial.println(startByte);
  }
  
  // Calibration
  if((int)startByte == '1')
  {
    calibrateAllAxes();
  }

  // Start or stop streaming value of all axis
  if((int)startByte == '2')
  {
    if(streaming)
    {
      streaming = false;
      Serial.println("Streaming stopped\n");
    }
    else
    {
      streaming = true;
      Serial.println("Streaming started\n");
    }
  }

  // Measure vibration intensity
  if((int)startByte == '3')
  {
    Serial.print("Vibration intensity: ");
    Serial.println(measureVibrationIntensity(3000));
  }

  if (streaming)
  {
    printAllAxesG(readAllAxesG());
  }
}