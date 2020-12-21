#define sanitizerDelay 0.25 //in seconds 

const int trigPin = 9;
const int echoPin = 10;
const byte motorpin = 8;
bool flag = true;
float duration, distance;
const int raspiPin = 5;
//const int buzzerPin = 6;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(motorpin, OUTPUT);
  //pinMode(raspiPin, INPUT);
  //pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  /*
  if(digitalRead(raspiPin)==HIGH)
  {
    digitalWrite(buzzerPin,HIGH);
  }
  else{
    digitalWrite(buzzerPin,LOW);
  }
  */
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = (duration * .0343) / 2;
  Serial.print("Distance: ");
  Serial.println(distance);
  
  if (distance <= 5) {
    digitalWrite(motorpin, HIGH);
    Serial.println("HIGH");
    delay(sanitizerDelay*1000);
    digitalWrite(motorpin, LOW);
  }
  delay(500);
}
