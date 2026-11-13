from machine import Pin
from diff_drive.regulated_wheel import RegulatedWheel


class DiffDriveController:
    def __init__(
        self,
        left_wheel_configs: dict,
        right_wheel_configs: dict,
        enable_pin_id: int,
    ):
        self.left_wheel = RegulatedWheel(
            motor_pin_ids=left_wheel_configs["motor_pin_ids"],
            encoder_pin_ids=left_wheel_configs["encoder_pin_ids"],
        )
        self.right_wheel = RegulatedWheel(
            motor_pin_ids=right_wheel_configs["motor_pin_ids"],
            encoder_pin_ids=right_wheel_configs["encoder_pin_ids"],
        )
        self.enable_pin = Pin(enable_pin_id, Pin.OUT)
        self.disable()
        # Constants
        self.wheel_sep = 0.116
        # Variables
        self.ang_vel = 0.0
        self.lin_vel = 0.0

    def enable(self):
        self.enable_pin.value(1)

    def disable(self):
        self.enable_pin.value(0)

    def get_vels(self):
        self.ang_vel = (
            self.right_wheel.lin_vel - self.left_wheel.lin_vel
        ) / self.wheel_sep
        self.lin_vel = (self.left_wheel.lin_vel + self.right_wheel.lin_vel) * 0.5

        return self.ang_vel, self.lin_vel

    def set_vels(self, ref_ang_vel, ref_lin_vel):
        ref_vel_left = ref_lin_vel - ref_ang_vel * self.wheel_sep * 0.5
        ref_vel_right = ref_lin_vel + ref_ang_vel * self.wheel_sep * 0.5
        self.left_wheel.set_vel(ref_vel_left)
        self.right_wheel.set_vel(ref_vel_right)


if __name__ == "__main__":
    # SETUP
    right_wheel_configs = {
        "motor_pin_ids": (9, 11, 10),
        "encoder_pin_ids": (16, 17),
    }
    left_wheel_configs = {
        "motor_pin_ids": (15, 13, 14),
        "encoder_pin_ids": (18, 19),
    }

    ddc = DiffDriveController(
        left_wheel_configs=left_wheel_configs,
        right_wheel_configs=right_wheel_configs,
        enable_pin_id=12,
    )
    ddc.enable()
    print(
        "Set desired angular and linear velocity by calling ddc.set_vels(<ang_vel>, <lin_vel>)"
    )
