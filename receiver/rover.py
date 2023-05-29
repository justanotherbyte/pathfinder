import threading
import time

from gpiozero import Motor, LED


class Rover:
    ENABLE_PIN = 26
    MOTOR_RN = 9
    MOTOR_RP = 10
    MOTOR_LN = 11
    MOTOR_LP = 8

    LED_PINS = [17, 27, 22, 23]

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

        self.leds = []
        for pin_num in self.LED_PINS:
            self.leds.append(LED(pin_num))

        print(self.leds)
        threading.Thread(target=self.rotate_lights, daemon=True).start()
    

    def rotate_lights(self):
        while True:
            for led in self.leds:
                led.on()
                time.sleep(0.1)
                led.off()