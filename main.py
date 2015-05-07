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


class PlayerShip(Widget):
    velocity = NumericProperty(2)

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
        print([(i, m.pos, m.size) for (i, m) in enumerate(self.ids.player_missiles.children)])


class GameApp(App):
    def build(self):
        params.init()

        game = AggressorsGame()

        game.size = 600, 400

        game.init_ship()
        game.init_aliens()

        Clock.schedule_interval(game.update, 1.0 / 60.)
        Clock.schedule_interval(game.fire_player_missile, 1)

        return game


class Params(object):
    def init(self):
        pass


params = Params()

if __name__ == "__main__":
    GameApp().run()
