import random

from message import (
    Direction,
    Motor,
    RedisMessage
)
from redisclient import Redis


class Rover:
    def __init__(self):
        self.redis = Redis()
        self.forward_prev = False
        self.backward_prev = False
        self.left_prev = False
        self.right_prev = False

        self._pos = (0, 0)

    def _nonce(self) -> int:
        return random.randint(100, 10000)

    def handle_input(self, mapping: dict):
        forward = mapping['w']
        left = mapping['a']
        right = mapping['d']
        backward = mapping['s']
        
        if forward:
            # handle forward and backward first
            f_message = RedisMessage(
                direction=Direction.Forward,
                motor=Motor.Both,
                speed=forward,
                nonce=self._nonce()
            )
            self.redis.send(f_message)
            self.forward_prev = True

        elif backward:
            b_message = RedisMessage(
                direction=Direction.Backward,
                motor=Motor.Both,
                speed=backward,
                nonce=self._nonce()
            )
            self.redis.send(b_message)
            self.backward_prev = True

        # handle left
        if left:
            motor_right = RedisMessage(
                direction=Direction.Forward,
                motor=Motor.Right,
                speed=1.0,
                nonce=self._nonce()
            )
            motor_left = RedisMessage(
                direction=Direction.Backward,
                motor=Motor.Left,
                speed=1.0,
                nonce=self._nonce()
            )
            self.redis.send(motor_right, motor_left)
            self.left_prev = True

        elif right:
            motor_right = RedisMessage(
                direction=Direction.Backward,
                motor=Motor.Right,
                speed=1.0,
                nonce=self._nonce()
            )
            motor_left = RedisMessage(
                direction=Direction.Forward,
                motor=Motor.Left,
                speed=1.0,
                nonce=self._nonce()
            )
            self.redis.send(motor_right, motor_left)
            self.right_prev = True


        stop_msg = RedisMessage(
            direction=Direction.Forward, # redundant here doesn't matter
            motor=Motor.Both,
            speed=0.0,
            nonce=self._nonce()
        )

        if self.forward_prev:
            if not forward:
                self.redis.send(stop_msg)
                self.forward_prev = False

        if self.backward_prev:
            if not backward:
                self.redis.send(stop_msg)
                self.backward_prev = False

        if self.right_prev:
            if not right:
                self.redis.send(stop_msg)
                self.right_prev = False

        if self.left_prev:
            if not left:
                self.redis.send(stop_msg)
                self.left_prev = False