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

  def __add__(self, other):
    x, y = other.xy()
    return Position(self._x + x, self._y + y)

class PlayerCharacter(object):
  def __init__(self):
    self._point = Position(1, 1)

  def draw(self, screen):
    screen.move(self._point.xy())
    screen.set_color(Color.WHITE)
    screen.write('@')
    screen.move(self._point.xy())

  def move(self, direction):
    self._point += direction
    return self

class Direction(object):
  EAST  = Position( 1,  0)
  WEST  = Position(-1,  0)
  NORTH = Position( 0, -1)
  SOUTH = Position( 0,  1)
  NORTH_EAST = NORTH + EAST
  NORTH_WEST = NORTH + WEST
  SOUTH_EAST = SOUTH + EAST
  SOUTH_WEST = SOUTH + WEST

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
    elif key == 'l': self._player.move(Direction.EAST)
    elif key == 'h': self._player.move(Direction.WEST)
    elif key == 'k': self._player.move(Direction.NORTH)
    elif key == 'j': self._player.move(Direction.SOUTH)
    elif key == 'y': self._player.move(Direction.NORTH_WEST)
    elif key == 'u': self._player.move(Direction.NORTH_EAST)
    elif key == 'b': self._player.move(Direction.SOUTH_WEST)
    elif key == 'n': self._player.move(Direction.SOUTH_EAST)
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
