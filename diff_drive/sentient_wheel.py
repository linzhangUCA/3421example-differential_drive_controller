from math import pi

from machine import Timer

from diff_drive.encoder import Encoder


class SentientWheel(Encoder):
    def __init__(self, ch_a_id: int, ch_b_id: int):
        super().__init__(ch_a_id, ch_b_id)
        # Contants
        self.cpr = 28
        self.gear_ratio = 100  # 100:1
        self.wheel_radius = 0.022  # m
        self.meas_freq = 200  # Hz
        # Variables
        self.prev_counts = 0
        self.ang_vel = 0.0
        self.lin_vel = 0.0
        # Velocity measurement timer
        self.vel_meas_timer = Timer(
            freq=self.meas_freq,  # Hz
            mode=Timer.PERIODIC,
            callback=self.measure_velocity,
        )

    def measure_velocity(self, timer):
        curr_counts = self.counts
        delta_counts = curr_counts - self.prev_counts
        self.prev_counts = curr_counts  # NOTE: counts now is the past
        cps = delta_counts * self.meas_freq  # encoder counts per second
        rps_og = cps / self.cpr  # original shaft's revs per second
        ang_vel_og = rps_og * 2 * pi  # original shaft's ang. vel., rad/s
        self.ang_vel = ang_vel_og / self.gear_ratio  # rad/s
        self.lin_vel = self.ang_vel * self.wheel_radius  # m/s


# TEST
if __name__ == "__main__":
    from time import sleep

    # from machine import Pin
    #
    # from diff_drive.motor import Motor

    # SETUP
    sw = SentientWheel(16, 17)  # right
    # m = Motor(9, 11, 10)
    # sw = SentientWheel(18, 19)  # left
    # m = Motor(15, 13, 14)
    # STBY = Pin(12, Pin.OUT)
    # STBY.value(1)

    # LOOP
    while True:
        print(f"Measured angular velocity: {sw.ang_vel}, linear velocity: {sw.lin_vel}")
        sleep(0.1)

    # efforts = (0, 0.25, 0.5, 0.75, 1.0)
    # for ef in efforts:
    #     m.forward(ef)
    #     for _ in range(20):
    #         print(f"Measured linear velocity: {sw.lin_vel}")
    #         sleep(0.1)
    # for ef in reversed(efforts):
    #     m.forward(ef)
    #     for _ in range(20):
    #         print(f"Measured linear velocity: {sw.lin_vel}")
    #         sleep(0.1)
    #
    # STBY.value(0)
