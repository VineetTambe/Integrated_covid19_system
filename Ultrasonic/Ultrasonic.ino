const int trigPin = 9;
const int echoPin = 10;
const byte motorpin = 8;
bool flag = true;
float duration, distance;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(motorpin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
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
    delay(500);
    digitalWrite(motorpin, LOW);
  }
  delay(100);
}
