# -*- coding: utf-8 -*-
from app import Application
from app import Screen

class GameScene(object):
  _current = None

  @classmethod
  def change(cls, new_scene):
    if GameScene._current: GameScene._current.finalize()
    GameScene._current = new_scene
    GameScene._current.initialize()

  @classmethod
  def update(cls):
    GameScene._current.update()

class Game(Application):
  _is_over = False

  def __init__(self, first_scene):
    Application.__init__(self)
    self._first_scene = first_scene

  @classmethod
  def over(cls):
    cls._is_over = True

  @classmethod
  def is_over(cls):
    return cls._is_over

  def main(self, args):
    Screen().initialize()
    GameScene.change(self._first_scene)
    Game._is_over = False
    while not self.is_over():
      GameScene.update()
