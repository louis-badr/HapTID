const int numFSRs = 5;
const int fsrPins[numFSRs] = {A0, A1, A2, A3, A4}; // Arduino Mega analog pins
const int pressThreshold = 400;                    // FSR value above which we consider the key pressed
bool isRunning = false;
unsigned long startTime;
unsigned long elapsedTime;

void setup(void)
{
  Serial.begin(115200);
  // Initialize FSR pins
  for (int i = 0; i < numFSRs; i++)
  {
    pinMode(fsrPins[i], INPUT);
  }
}

void loop()
{
  if (Serial.available() > 0)
  {
    char receivedChar = Serial.read();
    // Start the timer when we receive a 'C' character
    if (receivedChar == 'C')
    {
      startTime = micros();
      isRunning = true;
    }
  }
  // If the timer is running
  if (isRunning)
  {
    // Check if any FSR is pressed
    for (int i = 0; i < numFSRs; i++)
    {
      int fsrValue = analogRead(fsrPins[i]);
      if (fsrValue > pressThreshold)
      {
        // Stop the timer and print the key number and elapsed time
        elapsedTime = micros() - startTime;
        Serial.print(i);
        Serial.print(";");
        Serial.println(elapsedTime);
        // Stop reading
        isRunning = false;
        break;
      }
    }
    // If 4 seconds have passed, stop reading
    if (micros() - startTime > 4000000)
    {
      isRunning = false;
    }
  }
}