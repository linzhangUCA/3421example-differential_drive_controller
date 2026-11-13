# Make sure you've uploaded `diff_drive` directory to the Pico board


from time import sleep

from machine import Pin

from diff_drive.motor import Motor
from diff_drive.sentient_wheel import SentientWheel

# SETUP
m = Motor(9, 11, 10)  # right
sw = SentientWheel(16, 17)  # right
STBY = Pin(12, Pin.OUT)
STBY.off()
# Constants
TARGET_REVS = 2
CPR = 28
GEAR_RATIO = 100
TARGET_COUNTS = CPR * GEAR_RATIO * TARGET_REVS

# LOOP
STBY.on()  # enable motor driver
m.forward(0.4)
while sw.counts < TARGET_COUNTS:
    print(f"Encoder counts: {sw.counts}")
    sleep(0.01)
m.short_brake()
print("motor stopped.")
sleep(1)
STBY.off()  # disable motor driver
