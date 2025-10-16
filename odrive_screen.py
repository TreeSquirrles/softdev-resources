from kivy.properties import NumericProperty, Clock
from kivy.uix.screenmanager import ScreenManager, Screen

from dpea_odrive.odrive_helpers import *

ODRIVE_CONTROLLER_SERIAL_NUMBER = "207935A1524B"
od = find_odrive(serial_number=ODRIVE_CONTROLLER_SERIAL_NUMBER)
ax = ODriveAxis(od.axis1)
ax.set_vel_limit(5) #turns/s



class OdriveScreen(Screen):
    button_shift = NumericProperty(0)
    debounce = False
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def on_enter(self):
        Clock.schedule_interval(self.waitForNextCommand, 0.05)

    def on_leave(self):
        self.manager.current = 'main'

    def turn_forward_5_turns(self):
        print("sent call to turn forward 5")
        if(not self.debounce):
            self.debounce = True
            ax.set_relative_pos(5)

    def turn_backward_5_turns(self):
        print("sent call to turn backward 5")
        ax.set_relative_pos(-5)

    def waitForNextCommand(self, time=None):
        if not ax.is_busy():
           self.debounce = False

    def home(self):
        pass


