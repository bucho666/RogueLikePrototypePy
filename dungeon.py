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
import random

class DungeonScene(Scene):
  def __init__(self):
    Scene.__init__(self)
    self._screen = Screen()
    self._player = PlayerCharacter()
    self._floor = CurrentFloor()
    self._monster = Monster()
    self._sight = Sight(self._player, self._monster)

  def initialize(self):
    self._screen.clear()

  def update(self):
    self.walk_monster()
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

  def walk_monster(self):
    direction = random.choice(Direction.LIST)
    self.walk_character(direction, self._monster)

  def walk_player(self, direction):
    self.walk_character(direction, self._player)

  def walk_character(self, direction, ch):
    next_position = ch.next_position(direction)
    if self._floor.can_walk(next_position):
      ch.walk(direction)

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
  def __init__(self, character, monster):
    self._character = character
    self._last_position = character.position()
    self._floor = CurrentFloor()
    self._monster = monster

  def draw(self, screen):
    self.draw_last_position(screen)
    self.draw_current_position(screen)
    self.update_last_position()

  def draw_last_position(self, screen):
    for p in self._last_position.around():
      self._floor.draw_at(p, screen)

  def draw_current_position(self, screen):
    screen.set_color(Color.DEFAULT)
    for p in self._character.around_position():
      if self._monster.position() == p:
        self._monster.draw(screen)
      else:
        self._floor.draw_at(p, screen)

  def update_last_position(self):
    self._last_position = self._character.position()

if __name__ == '__main__':
  from title import TitleScene
  from game import Game 
  Game(TitleScene()).run()
