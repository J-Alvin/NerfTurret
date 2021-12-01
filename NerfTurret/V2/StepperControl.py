'''
Stepper motor Object
'''

#from gpiozero import OutputDevice as stepper
from DebugStepper import stepper
import time

class StepperMotor():
    seq = [[1,0,0,1], # Define step sequence as shown in manufacturers datasheet
             [1,0,0,0], 
             [1,1,0,0],
             [0,1,0,0],
             [0,1,1,0],
             [0,0,1,0],
             [0,0,1,1],
             [0,0,0,1]]
    
    stepCount = len(seq)
    in_1 = None
    in_2 = None
    in_3 = None
    in_4 = None
    stepPins = None
    stepCounter = 0
    waitTime = 0.004
    stepDir = 1

    def __init__(self, pin_1, pin_2, pin_3, pin_4):
        self.in_1 = stepper(pin_1)
        self.in_2 = stepper(pin_2)
        self.in_3 = stepper(pin_3)
        self.in_4 = stepper(pin_4)
        self.stepPins = [self.in_1, self.in_2, self.in_3, self.in_4]

    def reverseDirection(self):
        self.stepDir = self.stepDir *-1

    def forward(self, steps):
        for _ in range(steps):
            for pin in range(0,4):
                xPin= self.stepPins[pin]          # Get GPIO
                if self.seq[self.stepCounter][pin]!=0:
                    xPin.on()
                else:
                    xPin.off()

            self.stepCounter += self.stepDir
            if (self.stepCounter >= self.stepCount):
                self.stepCounter = 0
            if (self.stepCounter < 0):
                self.stepCounter = self.stepCount + self.stepDir
            time.sleep(self.waitTime)     # Wait before moving on

