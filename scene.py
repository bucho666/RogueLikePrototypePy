# -*- coding: utf-8 -*-
from app import Screen
from app import Color
from game import Game
from game import GameScene
from floor import CurrentFloor 
from floor import Position
from floor import Direction

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

class PlayerCharacter(object):
  def __init__(self):
    self._position = Position(1, 1)

  def draw(self, screen):
    screen.move(self._position.xy())
    screen.set_color(Color.WHITE)
    screen.write('@')
    screen.move(self._position.xy())

  def move(self, direction):
    self._position += direction
    return self

  def position(self):
    return self._position

  def around_position(self):
    return self._position.around()

  def moved_position(self, direction):
    return self._position + direction
   
class DungeonScene(Scene):
  def __init__(self):
    Scene.__init__(self)
    self._screen = Screen()
    self._player = PlayerCharacter()
    self._floor = CurrentFloor()

  def initialize(self):
    self._screen.clear()
    self._screen.set_color(Color.GREEN)

  def update(self):
   self.draw()
   self.control(self._screen.read_key())

  def control(self, key):
    if   key == 'l': self.move_character(Direction.EAST)
    elif key == 'h': self.move_character(Direction.WEST)
    elif key == 'k': self.move_character(Direction.NORTH)
    elif key == 'j': self.move_character(Direction.SOUTH)
    elif key == 'y': self.move_character(Direction.NORTH_WEST)
    elif key == 'u': self.move_character(Direction.NORTH_EAST)
    elif key == 'b': self.move_character(Direction.SOUTH_WEST)
    elif key == 'n': self.move_character(Direction.SOUTH_EAST)
    elif key == '>': self.down_stairs()

  def down_stairs(self):
    if not self._floor.is_down_stairs_at(self._player.position()):
      return
    if not self._floor.is_last_floor():
      self._floor.next()
      self._screen.clear()
    else:
      GameScene.change(EndingScene())

  def move_character(self, direction):
    next_position = self._player.moved_position(direction)
    if self._floor.can_walk(next_position):
      self._player.move(direction)

  def draw(self):
    self._screen.set_color(Color.DEFAULT)
    for p in self._player.around_position():
      self._floor.draw_at(p, self._screen)
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
