import os

os.environ['DISPLAY'] = ":0.0"
import sys
sys.path.insert(0, 'pidev')

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.config import Config
from pidev.pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.pidev.kivy.PauseScreen import PauseScreen
from pidev.pidev.kivy.AdminScreen import AdminScreen
from pidev.pidev.kivy.DPEAButton import DPEAButton
from joystick_screen import JoystickScreen


# TODO Lesson 5: Uncomment lines below
from dpeaDPi.DPiComputer import DPiComputer
from dpeaDPi.DPiStepper import *

dpiStepper = DPiStepper()
dpiStepper.setBoardNumber(0)
if not dpiStepper.initialize():
    print("Communication with the DPiStepper board failed.")

dpiComputer = DPiComputer()
if not dpiComputer.initialize():
    print("Communication with the DPiComputer board failed.")
# -------------------------------------------------------------


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
        # TODO: Load the joystick_screen.kv file here when ready

        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        # TODO: add a JoystickScreen widget here
        sm.add_widget(PassCodeScreen(name='passCode'))
        sm.add_widget(AdminScreen(name='admin'))
        sm.add_widget(PauseScreen(name='pauseScene'))
        PassCodeScreen.set_admin_events_screen('admin')

        return sm


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    # Variables for the Main Screen
    # TODO: Add more variables here as you see fit.
    servo_scheduled = False

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
        # TODO: increase the text in the counter button by 1

    def schedule_servo_motor(self):
        """
            This function should enable or disable the servo motor from listening to a switch event.
            When you press a button, it "wakes up" the servo and then moves according to a switch being pressed or not.
            Variables used/altered:
                self.servo_scheduled
                self.ids.servo_motor_script_button.text
            It results in a call being placed to servo_motor_listener
            Called by a Kivy button
        """
        #TODO: Test the functionality of this button on your GUI. 
        #   You should be able to toggle the servo motor action on and off
        #TODO: Find the bug in this code
        print("Call to schedule_servo_motor")

        if not self.servo_scheduled:
            Clock.schedule_interval(self.servo_motor_listener, 0.05)
            self.ids.servo_motor_button.fill_color = 'green'
            self.ids.servo_motor_button.text = 'Servo ON'
            print("Scheduled servo motor")

        else:
            Clock.unschedule(self.servo_motor_listener)
            self.ids.servo_motor_button.fill_color = 'red'
            self.ids.servo_motor_button.text = 'Servo OFF'
            print("Unscheduled servo motor")

    def servo_motor_listener(self, dt=0):
        """
           This function reads a switch and activates the servo motor based on that input.
           Variables used/altered:
               dpiComputer
           It results in the servo motor being to either 180° or 0°.
           Called by schedule_servo_motor
        """

        print("Call to servo_motor_listener")

        # if switch is pressed:
        # TODO Lesson 5: Move servo one direction
        # else:
        # TODO Lesson 5: Move servo the other direction

    def schedule_stepper_motor(self):
        """
            This function should behave similarly to the scheduling function for the servo.
            When activated the motor should start moving based off of the slider position.
            This function
        """

        print("Call to schedule_stepper_motor")

        # TODO: Schedule/unschedule the Kivy Clock to run stepper_motor_listener
        # TODO: Change the color and text of the stepper power button to indicate the status of the motor

    def stepper_motor_listener(self, dt=None):
        """
            This function is responsible for running the stepper motor based off of the slider.
            When the slider is in the middle, the stepper motor should be disabled.
            When the slider is moved to the right, the motor increases in speed in the clockwise direction.
            When the slider is moved left of the midpoint, the motor increases in speed in the counter-clockwise direction.
        """

        print("Call to stepper_motor_listener")

        # TODO: Get the value (-100 to 100) from a slider named "position"
        # TODO: Check if the slider is zero
        # TODO Lesson 5: If zero, decelerate, stop, and disable
        # TODO Lesson 5: If positive, spin stepper CW. Speed should increase with slider.
        # TODO Lesson 5: If negative, spin stepper CCW. Speed should increase with slider.
        # TODO Lesson 5: Utilize the helper function below to clean up your motor control code

    def set_motor_speed_by_revs_per_sec(self, revs_per_sec, stepper_num=0):
        """ This is a helper function that sets the speed of a stepper motor by a specified revolutions per second"""
        microstepping = 8
        dpiStepper.setMicrostepping(microstepping)
        speed_steps_per_second = (200 * microstepping) * revs_per_sec
        accel_steps_per_second_per_second = speed_steps_per_second
        dpiStepper.setSpeedInStepsPerSecond(stepper_num, speed_steps_per_second)
        dpiStepper.setAccelerationInStepsPerSecondPerSecond(stepper_num, accel_steps_per_second_per_second)

    def switch_screen(self):
        # TODO: set the screen manager's current screen to be the joystick screen
        print("Triggered switch to Joystick Screen")

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
