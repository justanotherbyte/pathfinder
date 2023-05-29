from gpiozero import Motor


class Rover:
    ENABLE_PIN = 26
    MOTOR_RN = 9
    MOTOR_RP = 10
    MOTOR_LN = 11
    MOTOR_LP = 8

    def __init__(self):
        self.right_motor = Motor(
            forward=self.MOTOR_RP,
            backward=self.MOTOR_RN,
            enable=self.ENABLE_PIN
        )
        self.left_motor = Motor(
            forward=self.MOTOR_LN,
            backward=self.MOTOR_LP,
            enable=None # gpiozero errors if we set both motors
            # to have the same enable pin. this is fine since both motors
            # will always be enabled and disabled at the same time
        )

    

