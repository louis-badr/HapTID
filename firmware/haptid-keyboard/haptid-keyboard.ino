const int numFSRs = 5;
const int fsrPins[numFSRs] = {A0, A1, A2, A3, A4}; // Arduino Mega analog pins
const int pressThreshold = 250;                    // FSR value difference from baseline to consider a key press
bool isRunning = false;
unsigned long startTime;
unsigned long elapsedTime;
int baseline[numFSRs];

// Calculates the average value of the FSRs to use as a baseline with numSamples samples and delayTime ms between each sample
void calcBaselines(int numSamples, int delayTime)
{
  // Reads each FSR each loop and not one by one to maximize the time between reads
  for (int i = 0; i < numSamples; i++)
  {
    for (int j = 0; j < numFSRs; j++)
    {
      baseline[j] += analogRead(fsrPins[j]);
    }
    delay(delayTime);
  }
  for (int i = 0; i < numFSRs; i++)
  {
    baseline[i] /= numSamples;
  }
}

void setup(void)
{
  Serial.begin(115200);
  // Initialize FSR pins
  for (int i = 0; i < numFSRs; i++)
  {
    pinMode(fsrPins[i], INPUT);
  }
  delay(3000);
  // Takes 5 * 100 * 10 ms = 5 seconds
  calcBaselines(100, 10);
}

void loop()
{
  if (Serial.available() > 0)
  {
    char receivedChar = Serial.read();
    // Start the timer when we receive a 'R' character
    if (receivedChar == 'R')
    {
      startTime = micros();
      // Takes 5 * 3 * 5 ms = 75 ms
      calcBaselines(3, 5);
      isRunning = true;
    }
    // Stop the timer if we receive a 'S' character
    else if (receivedChar == 'S')
    {
      // Stop reading
      isRunning = false;
    }
  }
  // If the timer is running
  if (isRunning)
  {
    // Check if any FSR is pressed
    for (int i = 0; i < numFSRs; i++)
    {
      int fsrValue = analogRead(fsrPins[i]);
      if (fsrValue > pressThreshold + baseline[i])
      {
        // Stop the timer and print the key number and elapsed time
        elapsedTime = micros() - startTime;
        Serial.print("[");
        Serial.print(i);
        Serial.print(";");
        Serial.print(elapsedTime);
        Serial.println("]");
        // Stop reading
        isRunning = false;
        // Debounce
        delay(50);
        break;
      }
    }
    // If 3 seconds have passed, stop reading
    if (micros() - startTime > 3000000)
    {
      isRunning = false;
    }
  }
}