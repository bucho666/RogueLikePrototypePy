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

  def __add__(self, other):
    x, y = other.xy()
    return Position(self._x + x, self._y + y)

  def xy(self):
    return (self._x, self._y)

  def around_xy(self):
    x, y = self._x, self._y
    return ((x-1, y-1), (x,   y-1), (x+1, y-1),
            (x-1, y  ),             (x+1, y  ),
            (x-1, y+1), (x  , y+1), (x+1, y+1))

class Direction(object):
  EAST  = Position( 1,  0)
  WEST  = Position(-1,  0)
  NORTH = Position( 0, -1)
  SOUTH = Position( 0,  1)
  NORTH_EAST = NORTH + EAST
  NORTH_WEST = NORTH + WEST
  SOUTH_EAST = SOUTH + EAST
  SOUTH_WEST = SOUTH + WEST

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

  def around_xy(self):
    return self._position.around_xy()

  def moved_position(self, direction):
    return self._position + direction

MAP = [
      list('##########################'),
      list('#....######.........######'),
      list('#....####.+.#.....#.######'),
      list('##+####...#.###.###.+...##'),
      list('##......###.#.....#.###.##'),
      list('###########.........+...##'),
      list('##########################'),
      ]

class DungeonScene(Scene):
  def __init__(self):
    Scene.__init__(self)
    self._screen = Screen()
    self._player = PlayerCharacter()

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
    elif key == 'q':
      GameScene.change(EndingScene())
      return

  def move_character(self, direction):
    x, y = self._player.moved_position(direction).xy()
    if MAP[y][x] != '#':
      self._player.move(direction)

  def draw(self):
    self._screen.set_color(Color.DEFAULT)
    for x, y in self._player.around_xy():
        self._screen.move((x, y))
        self._screen.write(MAP[y][x])
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
