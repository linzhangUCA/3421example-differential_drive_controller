from machine import Timer

from diff_drive.motor import Motor
from diff_drive.sentient_wheel import SentientWheel


def clamp(x, min_val=-1.0, max_val=1.0):
    return max(min_val, min(x, max_val))


class RegulatedWheel(Motor, SentientWheel):
    def __init__(self, motor_pin_ids, encoder_pin_ids):
        Motor.__init__(self, *motor_pin_ids)
        SentientWheel.__init__(self, *encoder_pin_ids)
        # Constants
        self.K_P = 1.5
        self.K_I = 0.8
        self.K_D = 0.25
        self.reg_freq = 100  # Hz
        # Variables
        self.prev_err = 0.0
        self.sum_err = 0.0
        self.reg_counter = 0
        self.ref_vel = 0.0  # reference linear velocity
        # Controller timer
        self.vel_reg_timer = Timer(
            freq=self.reg_freq,
            mode=Timer.PERIODIC,
            callback=self.regulate_velocity,
        )

    def regulate_velocity(self, timer):
        if self.ref_vel == 0.0 or self.reg_counter > self.reg_freq:
            self.short_brake()
        else:
            err = self.ref_vel - self.lin_vel
            self.sum_err += err
            d_err = err - self.prev_err  # ignored rescaling by dt
            self.prev_err = err  # NOTE: error now is the past
            u = clamp(self.K_P * err + self.K_I * self.sum_err + self.K_D * d_err)
            if u > 0.0:
                self.forward(u)
            elif u < 0.0:
                self.backward(-u)
            else:
                self.short_brake()
            self.reg_counter += 1

    def set_vel(self, reference_value=0.0):
        """Set reference/target linear velocity
        Args:
            reference_value
        """
        if reference_value != self.ref_vel:
            self.prev_err = 0.0
            self.sum_err = 0.0
        self.ref_vel = reference_value
        self.reg_counter = 0


if __name__ == "__main__":
    from time import sleep

    from machine import Pin

    # SETUP
    regw = RegulatedWheel(motor_pin_ids=(9, 11, 10), encoder_pin_ids=(16, 17))  # right
    # regw = RegulatedWheel(motor_pin_ids=(15, 13, 14), encoder_pin_ids=(18, 19))  # right
    STBY = Pin(12, Pin.OUT)
    STBY.value(1)  # enable motor driver

    # LOOP
    for refv in (0.1, 0.2, 0.3, 0.4, 0.0):
        regw.set_vel(refv)
        for _ in range(200):  # 2 sec for each ref vel
            print(f"Reference velocity: {refv}, measured velocity: {regw.lin_vel}")
            sleep(0.01)

    STBY.value(0)  # disable motor driver
