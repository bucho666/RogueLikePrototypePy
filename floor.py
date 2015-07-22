# -*- coding: utf-8 -*-

class Position(object):
  def __init__(self, x, y):
    self._x, self._y = (x, y)

  def __add__(self, other):
    x, y = other.xy()
    return Position(self._x + x, self._y + y)

  def __eq__(self, other):
    return self.xy() == other.xy()

  def xy(self):
    return (self._x, self._y)

  def around(self):
    x, y = self._x, self._y
    return (Position(x-1, y-1), Position(x,   y-1), Position(x+1, y-1),
            Position(x-1, y  ),                     Position(x+1, y  ),
            Position(x-1, y+1), Position(x  , y+1), Position(x+1, y+1))

class Direction(object):
  EAST  = Position( 1,  0)
  WEST  = Position(-1,  0)
  NORTH = Position( 0, -1)
  SOUTH = Position( 0,  1)
  NORTH_EAST = NORTH + EAST
  NORTH_WEST = NORTH + WEST
  SOUTH_EAST = SOUTH + EAST
  SOUTH_WEST = SOUTH + WEST
  LIST = (
    EAST, WEST, NORTH, SOUTH,
    NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST
  )

MAP = ( [
      list('##########################'),
      list('#....######.........######'),
      list('#....####.+.#.....#.######'),
      list('##+####...#.###.###.+...##'),
      list('##...>..###.#.....#.###.##'),
      list('###########.........#>..##'),
      list('##########################'),
      ],
      [
      list('##########################'),
      list('###########...#.#...+..###'),
      list('#########.+.#.#...#.##.###'),
      list('#######...#.#.#..##.#...##'),
      list('###.....###.#.....#.#...##'),
      list('#>..#######.###.....#<..##'),
      list('##########################'),
      ])

class CurrentFloor(object):
  _floor = 0
  _terrain = MAP[_floor]

  def terrain_at(self, position):
    x, y = position.xy()
    return CurrentFloor._terrain[y][x]

  def draw_at(self, position, screen):
    screen.move(position.xy())
    screen.write(self.terrain_at(position))

  def is_last_floor(self):
    return CurrentFloor._floor == len(MAP) - 1

  def can_walk(self, position):
    return self.terrain_at(position) != '#'

  def is_down_stairs_at(self, position):
    return self.terrain_at(position) == '>'

  def next(self):
    CurrentFloor._floor += 1
    CurrentFloor._terrain = MAP[CurrentFloor._floor]
