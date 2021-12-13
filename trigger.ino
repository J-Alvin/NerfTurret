#include <AccelStepper.h>
#define motorPin1  11      // IN1
#define motorPin2  10      // IN2
#define motorPin3  9     // IN3
#define motorPin4  8     // IN4
int yes = LOW;
#define inPin 4
#define MotorInterfaceType 8

AccelStepper stepper = AccelStepper(MotorInterfaceType, motorPin1, motorPin3, motorPin2, motorPin4);

void setup()
{stepper.setMaxSpeed(500);
Serial.begin(9600);
pinMode(inPin, INPUT);
}

void loop() {
  yes = !digitalRead(inPin);
  if(yes == LOW)
  {
    stepper.setSpeed(1000);
    stepper.runSpeed();
    }
    Serial.println(yes);
}
