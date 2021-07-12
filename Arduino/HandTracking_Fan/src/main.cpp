#include <Arduino.h>
#include <string.h>

void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  // put your setup code here, to run once:
}

void loop() {
  // digitalWrite(2, HIGH);
  if(Serial.available())
  {
    String s = Serial.readStringUntil(':');
    // int str = Serial.read();
    if(s.equals("aa"))
    {
      digitalWrite(2, HIGH);
    }
    analogWrite(3, s.toInt());
  }
  // put your main code here, to run repeatedly:
}