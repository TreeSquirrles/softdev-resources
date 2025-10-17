from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

from dpea_odrive.odrive_helpers import *

ODRIVE_CONTROLLER_SERIAL_NUMBER = "207935A1524B"
od = find_odrive(serial_number=ODRIVE_CONTROLLER_SERIAL_NUMBER)
ax = ODriveAxis(od.axis1)
ax.set_vel_limit(5) #turns/s
# ax.home_without_endstop(1, 0.5)

#4 butt 3 pot


class OdriveScreen(Screen):
    button_shift = NumericProperty(0)

    BUTTON_PIN = 4
    POT_PIN = 3
    MAX_DIST = 13 #rotations
    debounce = False
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def on_enter(self):
        Clock.schedule_interval(self.step, 0.05)

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

    def waitForNextCommand(self, dt=None):
        print(round(ax.get_pos(), 2))
        if not ax.is_busy():
           self.debounce = False

    def btnPress(self, dt=None):
        self.ids.btn_indicator_label.text = ("IM HAPPY YAY THE BUTTON IS PRESSED" if not digital_read(4)
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


