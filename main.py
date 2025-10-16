import math
import os

from kivy.properties import ColorProperty, NumericProperty

os.environ['DISPLAY'] = ":0.0"
import sys
sys.path.insert(0, '.venv/src/pidev')
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.config import Config
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy.AdminScreen import AdminScreen
from pidev.kivy.DPEAButton import DPEAButton
from joystick_screen import JoystickScreen
from odrive_screen import OdriveScreen


from dpeaDPi.DPiComputer import DPiComputer
from dpeaDPi.DPiStepper import *

dpiStepper = DPiStepper()
dpiStepper.setBoardNumber(0)
if not dpiStepper.initialize():
    print("Communication with the DPiStepper board failed.")

dpiStepper.setMicrostepping(8)

dpiComputer = DPiComputer()
if not dpiComputer.initialize():
    print("Communication with the DPiComputer board failed.")

from dpea_odrive.odrive_helpers import *

ODRIVE_CONTROLLER_SERIAL_NUMBER = "207935A1524B"
od = find_odrive(serial_number=ODRIVE_CONTROLLER_SERIAL_NUMBER)
assert od.config.enable_break_resistor is True, "Check for faulty break resistor."
ax = ODriveAxis(od.axis1)
ax.set_gains()
if not ax.is_calibrated():
    print("Calibrating odrive motors")
    ax.calibrate()

class MotorButtonsGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        Builder.load_file('main.kv')
        Builder.load_file('joystick_screen.kv')
        Builder.load_file('odrive_screen.kv')

        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(JoystickScreen(name='joystick'))
        sm.add_widget(PassCodeScreen(name='passCode'))
        sm.add_widget(AdminScreen(name='admin'))
        sm.add_widget(PauseScreen(name='pauseScene'))
        sm.add_widget(OdriveScreen(name='odrive'))
        PassCodeScreen.set_admin_events_screen('admin')

        return sm


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    # Properties
    button_shift = NumericProperty(0.075)
    # Global variables
    servo_scheduled = False
    stepper_scheduled = False

    max_stepper_speed = 1600*5


    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)




    def counter_action(self):
        """
            This function increases the displayed count for the counter button by one
            Variables used/altered:
                self.ids.counter_button.text
            Called by counter_button
        """

        print("Call to counter_action")

        self.ids.counter_button.text = str(int(self.ids.counter_button.text) + 1)

    def schedule_servo_motor(self):
        """
            This function should enable or disable the servo motor from listening to a switch event.
            When you press a button, it "wakes up" the servo and then moves according to a switch being pressed or not.
            Variables used/altered:
                self.servo_scheduled
                self.ids.servo_motor_script_button.text
            It results in a call being placed to servo_motor_action

        """

        print("Call to schedule_servo_motor")

        servo_btn = self.ids.servo_motor_button


        if not self.servo_scheduled:
            Clock.schedule_interval(self.servo_motor_action, timeout=0.05)
            servo_btn.fill_color = (1, 0, 0, 1)
            servo_btn.text = "Turn Servo OFF"

        else:
            Clock.unschedule(self.servo_motor_action)
            servo_btn.fill_color = (0, 1, 0, 1)
            servo_btn.text = "Turn Servo ON"
            dpiComputer.writeServo(0, 90)

        self.servo_scheduled = not self.servo_scheduled
    def servo_motor_action(self, dt=0):
        """
           This function reads a switch and activates the servo motor based on that input.
           Variables used/altered:
               dpiComputer
           It results in the servo motor being to either 180° or 0°.
           Called by schedule_servo_motor
        """

        print("Call to servo_motor_switch_action")

        value = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)

        if value:
            dpiComputer.writeServo(0, 0) # CW
        else:
            dpiComputer.writeServo(0, 180) # CCW

    def schedule_stepper_motor(self):
        """
            This function should behave similarly to the scheduling function for the servo.
            When activated the motor should start moving based off of the slider position.
            This function
        """

        print("Call to schedule_stepper_motor")

        stepper_btn = self.ids.stepper_motor_button


        if not self.stepper_scheduled:
            Clock.schedule_interval(self.stepper_motor_action, timeout=0.05)
            stepper_btn.fill_color = (1, 0, 0, 1)
            stepper_btn.text = "Turn Stepper OFF"
            dpiStepper.enableMotors(False) # prevent any weird shenanigains
            dpiStepper.enableMotors(True)


        else:
            Clock.unschedule(self.stepper_motor_action)
            stepper_btn.fill_color = (0, 1, 0, 1)
            stepper_btn.text = "Turn Stepper ON"
            dpiStepper.enableMotors(False)
            print("Hi!")
        print(self.ids.slider.value)

        self.stepper_scheduled = not self.stepper_scheduled



    def stepper_motor_action(self, dt=None):
        """
            This function is responsible for running the stepper motor based off of the slider.
            When the slider is in the middle, the stepper motor should be disabled.
            When the slider is moved to the right, the motor increases in speed in the clockwise direction.
            When the slider is moved left of the midpoint, the motor increases in speed in the counter-clockwise direction.
        """

        print("Call to stepper_motor_action")

        slider_pos : float = self.ids.slider.value

        steps_per_second: float = abs(slider_pos)/100.0 * self.max_stepper_speed
        dpiStepper.setSpeedInStepsPerSecond(0, steps_per_second)
        dpiStepper.setAccelerationInStepsPerSecondPerSecond(0, steps_per_second)

        dpiStepper.moveToRelativePositionInSteps(0, int(math.copysign(1, slider_pos) * steps_per_second*0.05), False)

    def set_motor_speed_by_revs_per_sec(self, revs_per_sec, stepper_num=0):
        """ This is a helper function that sets the speed of a stepper motor by a specified revolutions per second"""
        microstepping = 8
        dpiStepper.setMicrostepping(microstepping)
        speed_steps_per_second = (200 * microstepping) * revs_per_sec
        accel_steps_per_second_per_second = speed_steps_per_second
        dpiStepper.setSpeedInStepsPerSecond(stepper_num, speed_steps_per_second)
        dpiStepper.setAccelerationInStepsPerSecondPerSecond(stepper_num, accel_steps_per_second_per_second)

    def switch_screen(self):
        print("Triggered switch to Joystick Screen")
        self.manager.current = 'joystick'

    def switch_to_odrive_screen(self):
        print("Triggered switch to ODrive Screen")
        self.manager.current = 'odrive'

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        self.manager.current = 'passCode'

if __name__ == "__main__":
    # Makes the window auto full screen
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'window_state', 'maximized')
    Config.write()
    MotorButtonsGUI().run()
