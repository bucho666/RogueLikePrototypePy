# -*- coding: utf-8 -*-
from app import Screen
from app import Color
from game import Game
from scene import Scene

class EndingScene(Scene):
  def __init__(self):
    Scene.__init__(self)
    self._screen = Screen()

  def initialize(self):
    self._screen.clear()
    self._screen.set_color(Color.RED)
    self._screen.write('You Won!!')
    self._screen.move((0, 1))
    self._screen.set_color(Color.YELLOW)
    self._screen.write('-- Press Any Key --')

  def update(self):
    key = self._screen.read_key()
    Game.over()
