from dpeaDPi.DPiComputer import DPiComputer
from dpeaDPi.DPiStepper import *
from time import sleep

dpiStepper = DPiStepper()


dpiStepper.setBoardNumber(0)
if dpiStepper.initialize() != True:
    print("Communication with the DPiStepper board failed.")
dpiStepper.enableMotors(True)



microstepping = 8
dpiStepper.setMicrostepping(microstepping)



speed_steps_per_second = 200 * microstepping
accel_steps_per_second_per_second = speed_steps_per_second
dpiStepper.setSpeedInStepsPerSecond(0, speed_steps_per_second)
dpiStepper.setAccelerationInStepsPerSecondPerSecond(0, accel_steps_per_second_per_second)


stepperStatus = dpiStepper.getStepperStatus(0)
print(f"Pos = {stepperStatus}")


stepper_num = 0
steps = -1600
wait_to_finish_moving_flg = True
for i in range(3):
    dpiStepper.setSpeedInStepsPerSecond(0, speed_steps_per_second)
    dpiStepper.setAccelerationInStepsPerSecondPerSecond(0, accel_steps_per_second_per_second)
    dpiStepper.moveToRelativePositionInSteps(stepper_num, steps, wait_to_finish_moving_flg)
    speed_steps_per_second += 200 * microstepping
    accel_steps_per_second_per_second += speed_steps_per_second


dpiStepper.enableMotors(False)