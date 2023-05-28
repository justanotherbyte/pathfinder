from gpiozero import Motor


class Rover:
    ENABLE_PIN = 26
    MOTOR_RN = 9
    MOTOR_RP = 10

    def __init__(self):
        self.right_motor = Motor(
            forward=self.MOTOR_RN,
            backward=self.MOTOR_RP,
            enable=self.ENABLE_PIN
        )

    def forward(self):
        self.right_motor.forward()