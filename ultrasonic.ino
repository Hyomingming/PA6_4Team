int ECHO = 7;
int TRIG = 6;
  
void setup() {
  Serial.begin(9600); // 시리얼 통신 시작, 9600bps의 속도로 시리얼 통신 시작
  pinMode(ECHO, INPUT);
  pinMode(TRIG, OUTPUT);
}

void loop() {
  float duration, distance;
  
  digitalWrite(TRIG, LOW);
  delay(2);
  digitalWrite(TRIG, HIGH);
  delay(20);
  digitalWrite(TRIG, LOW);

  if(digitalRead(ECHO) == LOW) {
    duration = pulseIn(ECHO, HIGH); // ECHO가 HIGH를 유지한 시간을 저장 한다.
    distance = ((float)(340*duration)/10000)/2;
  }
  
  Serial.println(distance);
  delay(100);
}
