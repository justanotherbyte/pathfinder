import time

import RPi.GPIO as GPIO
from gpiozero import Motor, LED


class Rover:
    ENABLE_PIN = 26
    MOTOR_RN = 9
    MOTOR_RP = 10
    MOTOR_LN = 11
    MOTOR_LP = 8

    TRIGGER_PIN = 13
    ECHO_PIN = 25

    SPEED_OF_SOUND_CM_NS = 343 * 100 / 1E9  # 0.0000343 cm / ns

    LED_PINS = [17, 27, 22, 23]

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)

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

    def read_distance(self, timeout: int = 50) -> float:
        offset = 190000
        GPIO.output(self.TRIGGER_PIN, 1)
        time.sleep(.00001)  # 10 microseconds
        GPIO.output(self.ECHO_PIN, 0)


        # Wait for the ECHO pin to go high
        # wait for the pulse rise
        GPIO.wait_for_edge(self.ECHO_PIN, GPIO.RISING, timeout=timeout)
        pulse_start = time.perf_counter_ns()

        # And wait for it to fall
        GPIO.wait_for_edge(self.ECHO_PIN, GPIO.FALLING, timeout=timeout)
        pulse_end = time.perf_counter_ns()

        pulse_duration = pulse_end - pulse_start - offset
        distance = (pulse_duration * self.SPEED_OF_SOUND_CM_NS) / 2
        return max(distance, 0.0)