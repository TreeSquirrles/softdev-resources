from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

from dpea_odrive.odrive_helpers import *

ODRIVE_CONTROLLER_SERIAL_NUMBER = "207935A1524B"
od = find_odrive(serial_number=ODRIVE_CONTROLLER_SERIAL_NUMBER)
ax = ODriveAxis(od.axis1)
ax.set_vel_limit(5) #turns/s
ax.home_without_endstop(1, 0.5)

#4 butt 3 pot


class OdriveScreen(Screen):
    button_shift = NumericProperty(0)
    BUTTON_PIN = 4
    POT_PIN = 3
    MAX_DIST = -13 #rotations
    debounce = False

    followPot = False
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def on_enter(self):
        Clock.schedule_interval(self.waitForNextCommand, 0.05)

    def on_leave(self):
        Clock.unschedule(self.waitForNextCommand)
        self.manager.current = 'main'

    def turn_forward_5_turns(self):
        print("sent call to turn forward 5")
        if self.debounce:
            return

        self.debounce = True
        ax.set_relative_pos(5)

    def turn_backward_5_turns(self):

        if self.debounce:
            return
        self.debounce = True

        print("sent call to turn backward 5")
        ax.set_relative_pos(-5)

    def schedule_follow_potentiometer(self):

        if self.followPot:
            self.debounce = True
            Clock.schedule_interval(self.set_position_on_potentiometer, 0.05)
            self.ids.follow_pot_toggle.text = "Following Potentiometer"
        else:
            Clock.unschedule(self.set_position_on_potentiometer)
            self.ids.follow_pot_toggle.text = "Tap to follow Potentiometer"

        self.followPot = not self.followPot

    def set_position_on_potentiometer(self, dt=None):
        print("hi")
        print(round(analog_read(od, 3), 4))
        ax.set_pos(self.MAX_DIST * analog_read(od, 3) / 3.3)


    def waitForNextCommand(self, dt=None):
        if not self.followPot and not ax.is_busy():
           self.debounce = False

    def btnPress(self, dt=None):
        self.ids.btn_indicator_label.text = ("IM HAPPY YAY THE BUTTON IS PRESSED" if not digital_read(od, 4)
        else "I'M NOT HAPPY BOO THE BUTTON IS NOT PRESSED")

    def step(self, dt=None):
        self.waitForNextCommand()
        self.btnPress()

    def home(self):
        if self.debounce:
            return
        print("homing")
        self.debounce = True
        # ax.home_with_endstop(1, .5, 2)
        ax.home_without_endstop(1, .5)


