# -*- coding: utf-8 -*-
from app import Screen
from app import Color
from game import Game
from game import GameScene

class Scene(object):
  def finalize(self):
    pass

  def initialize(self):
    pass

  def update(self):
    pass

class TitleScene(Scene):
  def __init__(self):
    Scene.__init__(self)
    self._screen = Screen()

  def initialize(self):
    self._screen.clear()
    self._screen.write('*** Rogue Rebuild ***')
    self._screen.move((0, 0))

  def update(self):
    key = self._screen.read_key()
    GameScene.change(DungeonScene())

class Position(object):
  def __init__(self, x, y):
    self._x, self._y = (x, y)

  def xy(self):
    return (self._x, self._y)

class PlayerCharacter(object):
  def __init__(self):
    self._point = Position(1, 1)

  def draw(self, screen):
    screen.move(self._point.xy())
    screen.set_color(Color.WHITE)
    screen.write('@')
    screen.move(self._point.xy())

class DungeonScene(Scene):
  def __init__(self):
    Scene.__init__(self)
    self._screen = Screen()
    self._player = PlayerCharacter()

  def initialize(self):
    self._screen.clear()
    self._screen.set_color(Color.GREEN)
    self._screen.write('Now Playng...')

  def update(self):
    key = self._screen.read_key()
    if key == 'q':
      GameScene.change(EndingScene())
      return
    self._screen.clear()
    self._player.draw(self._screen)

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

if __name__ == '__main__':
  from scene import TitleScene
  Game(TitleScene()).run()
