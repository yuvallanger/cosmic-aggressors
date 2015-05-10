#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
from builtins import range
from builtins import object
from kivy.app import App
#from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty  #, ObjectProperty  #, ReferenceListProperty
from kivy.uix.widget import Widget
from kivy.metrics import Metrics, sp
from kivy.logger import Logger
from kivy.uix.floatlayout import FloatLayout


class Aggressors(Widget):
    pass


class Aggressor(Widget):
    offset = NumericProperty('10sp')

    def move(self):
        new_x = self.x + self.offset

        is_beyond_rim = (
            new_x < self.parent.right + sp(50) or
            new_x > self.parent.left - sp(50))
        if is_beyond_rim:
            self.y -= self.offset
        else:
            self.x = new_x


class PlayerShip(Widget):
    velocity = NumericProperty(0)

    def move(self):
        self.x += self.velocity

        if self.x < 0:
            self.x = 0

        if self.right > self.parent.right:
            self.right = self.parent.right

    def fire_missile(self):
        if len(self.missiles.children) < params.max_missile_num:
            player_missile = PlayerMissile()
            player_missile.center_x = self.center_x
            player_missile.y = self.top

            self.missiles.add_widget(player_missile)



class AlienShip(Widget):
    pass


class PlayerMissile(Widget):
    velocity = NumericProperty('2sp')

    def move(self):
        self.y += self.velocity

        if self.y > self.ids.game.height:
            self.parent.remove_widget(self)


class PlayerMissiles(Widget):
    pass


class CosmicAggressorsGame(FloatLayout):
    def init_ship(self):
        self.ids.player_ship.center_x = self.center_x
        self.ids.player_ship.missiles = PlayerMissiles()

    def init_aggressors(self):
        for col in range(params.aggressors_col_num):
            for row in range(params.aggressors_row_num):
                relative_x = float(col)
                relative_y = float(row)

                aggressor = Aggressor()
                aggressor.x = sp(50) + sp(50) * relative_x
                aggressor.y = sp(150) + sp(50) * relative_y

                self.ids.aggressors.add_widget(aggressor)
        Logger.debug("{}", self.ids.aggressors.children[:])

    def move_missiles(self):
        for missile in self.ids.player_ship.missiles.children[:]:
            missile.move()

    def move_aggressors(self):
        for aggressor in self.ids.aggressors.children[:]:
            pass # aggressor.move()


    def update(self, dt):
        self.ids.player_ship.move()
        self.move_missiles()
        self.move_aggressors()
        #Logger.debug("{}".format([(i, m.pos, m.size) for (i, m) in enumerate(self.ids.player_ship.missiles.children)]))

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

    def _on_keyboard_down(self, window, key, scancode, unicode_key, modifiers):
        Logger.debug("{}".format([window, key, scancode, unicode_key, modifiers]))
        if unicode_key == u" ":
            self.ids.player_ship.fire_missile()
        if unicode_key == u"h":
            self.ids.player_ship.move_left()
        if unicode_key == u"l":
            self.ids.player_ship.move_right()

    def _on_keyboard_up(self, window, key, scancode, unicode_key, modifiers):
        Logger.debug("{} {} {} {} {}".format(window, key, scancode, unicode_key, modifiers))


class GameApp(App):
    def build(self):
        params.init()

        game = CosmicAggressorsGame()

        game.root = game

        game.init_ship()
        game.init_aggressors()

        Window.bind(on_key_down=game._on_keyboard_down)

        Clock.schedule_interval(game.update, 1.0 / 60.)

        return game


class Params(object):
    def init(self):
        self.bg_size = self.bg_width, self.bg_height = 600, 400
        self.width, self.height = Window.size
        self.center = Window.center
        ws = float(self.width) / self.bg_width
        hs = float(self.height) / self.bg_height
        self.scale = min(ws, hs)
        self.max_missile_num = 3
        self.aggressors_col_num = 0
        self.aggressors_row_num = 0
        Logger.debug(
            "size={Window.size}; "
            "dpi={Metrics.dpi}; "
            "density={Metrics.density}; "
            "SCALE={self.scale}".format(
                Window=Window,
                Metrics=Metrics,
                self=self,
            )
        )


params = Params()

if __name__ == "__main__":
    GameApp().run()
