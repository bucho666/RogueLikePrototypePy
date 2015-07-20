# -*- coding: utf-8 -*-
from app import Application
from app import Screen
from app import Color

class Scene(object):
  def finalize(self):
    pass

  def initialize(self):
    pass

  def update(self):
    pass

class ActiveScene(object):
  _current = Scene()
  def __init__(self):
    pass

  @classmethod
  def change(cls, new_scene):
    ActiveScene._current.finalize()
    ActiveScene._current = new_scene
    ActiveScene._current.initialize()

  @classmethod
  def update(cls):
    ActiveScene._current.update()

class TitleScene(Scene):
  def __init__(self):
    Scene.__init__(self)
    self._screen = Screen()

  def initialize(self):
    self._screen.clear()
    self._screen.write('タイトルシーン')
    self._screen.move(0, 0)

  def update(self):
    key = self._screen.read_key()
    if key == 'q':
      ActiveScene.change(EndingScene())

class EndingScene(Scene):
  def __init__(self):
    Scene.__init__(self)
    self._screen = Screen()

  def initialize(self):
    self._screen.clear()
    self._screen.set_color(Color.RED)
    self._screen.write('You Win!!')
    self._screen.move(0, 0)

  def update(self):
    key = self._screen.read_key()
    if key == 'q':
      Game.over()

class Game(Application):
  _is_over = False

  def __init__(self):
    Application.__init__(self)

  @classmethod
  def over(cls):
    cls._is_over = True

  @classmethod
  def is_over(cls):
    return cls._is_over

  def main(self, args):
    Screen().initialize()
    ActiveScene.change(TitleScene())
    Game._is_over = False
    while not self.is_over():
      ActiveScene.update()

if __name__ == '__main__':
  Game().run()
