# -*- coding: utf-8 -*-
from app import Color
from app import Screen
from scene import Scene
from game import GameScene
from floor import CurrentFloor
from floor import Direction
from character import Monster
from character import PlayerCharacter
from ending import EndingScene

class DungeonScene(Scene):
  def __init__(self):
    Scene.__init__(self)
    self._screen = Screen()
    self._player = PlayerCharacter()
    self._floor = CurrentFloor()
    self._sight = Sight(self._player)
    self._floor.put_monster(Monster())

  def initialize(self):
    self._screen.clear()

  def update(self):
    self._floor.update_monsters()
    self.draw()
    self.control(self._screen.read_key())

  def control(self, key):
    if   key == 'l': self.walk_player(Direction.EAST)
    elif key == 'h': self.walk_player(Direction.WEST)
    elif key == 'k': self.walk_player(Direction.NORTH)
    elif key == 'j': self.walk_player(Direction.SOUTH)
    elif key == 'y': self.walk_player(Direction.NORTH_WEST)
    elif key == 'u': self.walk_player(Direction.NORTH_EAST)
    elif key == 'b': self.walk_player(Direction.SOUTH_WEST)
    elif key == 'n': self.walk_player(Direction.SOUTH_EAST)
    elif key == '>': self.down_stairs()

  def walk_player(self, direction):
    self._floor.walk_character(direction, self._player)

  def down_stairs(self):
    if not self._floor.is_down_stairs_at(self._player.position()):
      return
    if not self._floor.is_last_floor():
      self._floor.next()
      self._screen.clear()
    else:
      GameScene.change(EndingScene())

  def draw(self):
    self._sight.draw(self._screen)
    self._player.draw(self._screen)

class Sight(object):
  def __init__(self, character):
    self._character = character
    self._last_position = character.position()
    self._floor = CurrentFloor()

  def draw(self, screen):
    self.draw_last_position(screen)
    self.draw_current_position(screen)
    self.update_last_position()

  def draw_last_position(self, screen):
    for p in self._last_position.around():
      self._floor.draw_unsight_at(p, screen)

  def draw_current_position(self, screen):
    screen.set_color(Color.DEFAULT)
    for p in self._character.around_position():
      self._floor.draw_sight_at(p, screen)

  def update_last_position(self):
    self._last_position = self._character.position()

if __name__ == '__main__':
  from title import TitleScene
  from game import Game
  Game(TitleScene()).run()
