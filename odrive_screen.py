from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen

from dpea_odrive.odrive_helpers import *

ODRIVE_CONTROLLER_SERIAL_NUMBER = "207935A1524B"
od = find_odrive(serial_number=ODRIVE_CONTROLLER_SERIAL_NUMBER)
ax = ODriveAxis(od.axis1)
ax.set_vel_limit(5) #turns/s


class OdriveScreen(Screen):
    button_shift = NumericProperty(0)
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def on_enter(self):
        pass

    def on_leave(self):
        self.manager.current = 'main'

    def turn_forward_5_turns(self):
        ax.set_pos(5)
        ax.wait_for_motor_to_stop()

    def turn_backward_5_turns(self):
        ax.set_relative_pos(-5)
        ax.wait_for_motor_to_stop()

    def home(self):
        pass


