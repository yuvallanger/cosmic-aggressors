#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from builtins import object
from kivy.app import App
#from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty  #, ObjectProperty  #, ReferenceListProperty
from kivy.uix.widget import Widget
from kivy.metrics import Metrics
from kivy.logger import Logger


class PlayerShip(Widget):
    velocity = NumericProperty(0)

    def move(self):
        self.x += self.velocity

        if self.x < 0:
            self.x = 0

        if self.right > self.parent.right:
            self.right = self.parent.right


class AlienShip(Widget):
    pass


class PlayerMissile(Widget):
    velocity = NumericProperty(2)

    def move(self):
        self.y += self.velocity

        if self.y > self.parent.parent.height:
            self.parent.remove_widget(self)


class PlayerMissiles(Widget):
    pass


class AggressorsGame(Widget):
    def init_ship(self):
        self.ids.player_ship.size = 20, 15
        self.ids.player_ship.center_x = self.center_x
        self.ids.player_ship.y = 10

    def fire_player_missile(self, *args):
        if len(self.ids.player_missiles.children) <= params.max_missile_num:
            player_missile = PlayerMissile()
            player_missile.center_x = self.ids.player_ship.center_x
            player_missile.y = self.ids.player_ship.top

            self.ids.player_missiles.add_widget(player_missile)

    def init_aliens(self):
        pass

    def move_missiles(self):
        for missile in self.ids.player_missiles.children[:]:
            missile.move()

    def update(self, dt):
        self.ids.player_ship.move()
        self.move_missiles()
        Logger.debug("{}".format([(i, m.pos, m.size) for (i, m) in enumerate(self.ids.player_missiles.children)]))

    def on_size(self, *args):
        Logger.debug(
            "size={Window.size}; "
            "dpi={Metrics.dpi}; "
            "density={Metrics.dpi}; "
            "SCALE={self.scale}".format(
                Window=Window,
                Metrics=Metrics,
                self=params,
            ))

    def _on_keyboard_down(self, window, b, keycode, text, modifiers):
        Logger.debug("{}".format(type(b)))
        if text == u" ":
            self.fire_player_missile()
        Logger.debug("{}".format([window, b, keycode, text, modifiers]))


class GameApp(App):
    def build(self):
        params.init()

        game = AggressorsGame()

        game.size = 600, 400

        game.init_ship()
        game.init_aliens()

        Window.bind(on_key_down=game._on_keyboard_down)

        Clock.schedule_interval(game.update, 1.0 / 60.)

        return game


class Params(object):
    def init(self):
        self.bg_width, self.bg_height = 600, 400
        self.width, self.height = Window.size
        self.center = Window.center
        ws = float(self.width) / self.bg_width
        hs = float(self.height) / self.bg_height
        self.scale = min(ws, hs)
        self.max_missile_num = 3
        Logger.debug(
            "size={Window.size}; "
            "dpi={Metrics.dpi}; "
            "density={Metrics.dpi}; "
            "SCALE={self.scale}".format(
                Window=Window,
                Metrics=Metrics,
                self=self,
            )
        )


params = Params()

if __name__ == "__main__":
    GameApp().run()
