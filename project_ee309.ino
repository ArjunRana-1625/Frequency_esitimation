const int signalPin = 2;  
volatile unsigned long lastTime = 0;
volatile unsigned long period = 0;
unsigned long lastUpdate = 0;
int readingsIgnored = 0;  // Counter to ignore first few unstable readings

void signalISR() {
  unsigned long currentTime = micros();
  period = currentTime - lastTime;
  lastTime = currentTime;
}

void setup() {
  Serial.begin(115200);
  pinMode(signalPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(signalPin), signalISR, RISING);
}

void loop() {
  if (millis() - lastUpdate >= 20) {  
    lastUpdate = millis();
    if (period > 0) {
      float frequency = 1000000.0 / period;
         unsigned long timestamp = millis();  

        if(timestamp>10000){
          Serial.print(timestamp);
          Serial.print(" ms, Frequency: ");
          Serial.print(frequency, 2);
          Serial.println(" Hz");
      }
    }
  }
}
