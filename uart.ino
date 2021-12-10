/* Handles input over USB from the camera and rotates a stepper motor to match the new angle.
 * 
 */
#include <Stepper.h>
float cur_angle = 0;
float target_angle = 40;
int steps_per_rev = 2048;
int steps_per_degree = steps_per_rev / 360;
Stepper yawMotor(steps_per_rev, 8, 10, 9, 11);
int incoming = 0;

void setup() {
  yawMotor.setSpeed(10);
  yawMotor.step(1024);
  yawMotor.step(-1024);
  Serial.begin(115200);     
  Serial.setTimeout(1);
}

void loop() {
  // Listen for input.
  while( !Serial.available());
  // Get our new desired angle.
  incoming = Serial.readString().toInt();
  Serial.print(incoming);

  // Do some data filtering when the serial misbehaves.
  if (incoming > 10 && incoming < 180)
  {
    target_angle = incoming;
    // calulate how much to step to reach new angle.
    int steps = (target_angle - cur_angle) * steps_per_degree;
    yawMotor.step(steps);
    cur_angle = target_angle;
    delay(250);
  }
}
