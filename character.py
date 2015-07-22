# -*- coding: utf-8 -*-
from app import Color
from floor import Position

class Character(object):
  def __init__(self):
    self._position = Position(1, 1)
    self._glyph = 'C'

  def draw(self, screen):
    screen.move(self._position.xy())
    screen.set_color(Color.WHITE)
    screen.write(self._glyph)

  def walk(self, direction):
    self._position += direction
    return self

  def position(self):
    return self._position

  def around_position(self):
    return self._position.around()

  def next_position(self, direction):
    return self._position + direction

class Monster(Character):
  def __init__(self):
    Character.__init__(self)
    self._glyph = 'g'

class PlayerCharacter(Character):
  def __init__(self):
    Character.__init__(self)
    self._glyph = '@'

  def draw(self, screen):
    Character.draw(self, screen)
    screen.move(self._position.xy())
