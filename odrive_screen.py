from kivy.uix.screenmanager import ScreenManager, Screen

from dpea_odrive.odrive_helpers import *

ODRIVE_CONTROLLER_SERIAL_NUMBER = "207935A1524B"
od = find_odrive(serial_number=ODRIVE_CONTROLLER_SERIAL_NUMBER)
ax = ODriveAxis(od.axis1)

class OdriveScreen(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def on_enter(self):
        pass

    def on_leave(self):
        self.manager.current = 'main'

    def turn_forward_5_turns(self):
        pass

    def turn_backward_5_turns(self):
        pass

    def home(self):
        pass


