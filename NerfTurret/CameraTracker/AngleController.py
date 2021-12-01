import StepperControl as sp

NUM_STEPS = 50

def motor_control(pins, v_turn, v_run):
    motor = sp.StepperMotor(pins[0], pins[1], pins[2], pins[3])
    old_value = 0

    # Run until MP is shut down.
    while(v_run.value):
        # Retrieve Turn Value
        value = v_turn.value
        if (value != 0):
            if ( old_value == value ):        
                pass
                #print("FORWARD")
                motor.forward(NUM_STEPS)
            else:
                motor.reverseDirection()   
                motor.forward(NUM_STEPS)
        old_value = value
        
