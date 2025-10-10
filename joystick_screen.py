from __future__ import annotations

from kivy.animation import Animation
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock

from pidev.kivy.ImageButton import ImageButton
from pidev.Joystick import Joystick

import pygame

import os.path

joy:Joystick|None = None

try:
    joy = Joystick(0, False)
except pygame.error as e:
    print("No joystick connected, please connect and try again.")


class JoystickScreen(Screen):
    anim = Animation(size_hint=(1, 1), duration=1.5, t="in_bounce")
    picture_size = NumericProperty(0.2)
    picture_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Hachune_Miku_infobox_size.png")

    def on_enter(self):
        print("Call to on_enter from JoystickScreen")
        Clock.schedule_interval(self.joy_update, 1.0/60)
        self.ids.hatsune_btn.source = self.picture_path
        self.ids.hatsune_btn.size_hint = (self.picture_size, self.picture_size)


    def on_leave(self, dt = None):
        print("Call to on_leave from JoystickScreen")
        Clock.unschedule(self.joy_update)
        self.anim.stop(self.ids.hatsune_btn)
        self.ids.hatsune_btn.size_hint = (self.picture_size, self.picture_size)
        self.manager.current = 'main'
        self.ids.hatsune_btn.pos[1] = self.height / 2 * (1 - self.picture_size)
        self.ids.hatsune_btn.pos[0] = self.width / 2 * (1 - self.picture_size)

    def joy_axes(self) -> tuple[float, float]:
        return joy.get_both_axes()
    def joy_update(self, dt=None):
        # TODO: Find the Joystick source code in your pidev folder or below
        #  Joystick source code: https://github.com/dpengineering/RaspberryPiCommon/blob/master/pidev/Joystick.py
        # TODO: Get joystick x and y values
        # TODO: Update x and y labels with joystick values
        # TODO: Move ImageButton based on joystick input

        self.update_buttons_clicked()

        if not joy:
            return

        joystick_x, joystick_y = self.joy_axes()

        self.ids.joy_x.text = f"x speed: {joystick_x}"
        self.ids.joy_y.text = f"y speed: {joystick_y}"

        const = 15

        picture = self.ids.hatsune_btn

        picture.pos[0] += joystick_x * const
        picture.pos[1] +=- joystick_y * const

        print("Call to joy_update from JoystickScreen")

    def update_buttons_clicked(self):

        if not joy:
            return

        pressed_btns: str = ""

        for i in range(0, 11):
            if joy.get_button_state(i):
                pressed_btns += str(i)

        self.ids.pressed_btns_btn.text = "No Buttons Pressed" if pressed_btns == "" else pressed_btns

        print("Call to check_buttons_clicked from JoystickScreen")

    def switch_screen_main(self):
        self.anim.start(self.ids.hatsune_btn)
        Clock.schedule_once(self.on_leave, 1.75)

        print("Call to switch_screen_main from JoystickScreen")
