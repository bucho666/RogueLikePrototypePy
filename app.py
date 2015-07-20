# -*- coding: utf-8 -*-
import curses
import random
import locale

class Screen(object):
  _color_table = []
  _screen = None
  def __init__(self):
    self._current_color = 0

  def initialize(self):
    Screen._screen = ScreenBuilder.build()
    Screen._color_table = Color.table()
    return self

  def read_key(self):
      return chr(self._screen.getch())

  def move(self, x, y):
      self._screen.move(x, y)

  def set_color(self, color_id):
    self._current_color = self._color_table[color_id]

  def write(self, string):
    self._screen.addstr(string, self._current_color)

  def clear(self):
    self._screen.clear()

class ScreenBuilder(object):
  @classmethod
  def build(cls):
    Color.initialize()
    return cls.initialize_screen()

  @classmethod
  def initialize_screen(cls):
    curses.noecho()
    curses.cbreak()
    screen = curses.initscr()
    screen.keypad(1)
    return screen

class Color(object):
  NUMBER = 17
  (DEFAULT,
  RED,
  GREEN,
  YELLOW,
  BLUE,
  MAGENTA,
  CYAN,
  WHITE,
  BLACK,
  RIGHT_RED,
  RIGHT_GREEN,
  RIGHT_YELLOW,
  RIGHT_BLUE,
  RIGHT_MAGENTA,
  RIGHT_CYAN,
  RIGHT_WHITE,
  RIGHT_BLACK) = range(NUMBER)

  @classmethod
  def initialize(cls):
    curses.start_color()
    color_pairs = (
      (cls.RED, curses.COLOR_RED), (cls.GREEN, curses.COLOR_GREEN),
      (cls.YELLOW, curses.COLOR_YELLOW), (cls.BLUE, curses.COLOR_BLUE),
      (cls.MAGENTA, curses.COLOR_MAGENTA), (cls.CYAN, curses.COLOR_CYAN),
      (cls.WHITE, curses.COLOR_WHITE), (cls.BLACK, curses.COLOR_BLACK))
    for (num, color) in color_pairs:
      curses.init_pair(num, color, curses.COLOR_BLACK)

  @classmethod
  def table(cls):
    table = []
    for color_num in range(17):
      color = curses.color_pair(color_num) if color_num <= 8\
        else curses.color_pair(color_num - 8) | curses.A_BOLD
      table.append(color)
    return table

class Application(object):
  def run(self):
    locale.setlocale(locale.LC_ALL, '')
    curses.wrapper(self._main)

  def _main(self, args):
    Screen().initialize()
    while True:
      self.process()

if __name__ == '__main__':
  class Demo(Application):
    import sys
    def __init__(self):
      Application.__init__(self)
      self._screen = Screen()

    def process(self):
      key = self._screen.read_key()
      if key == 'q': sys.exit(1)
      self._screen.clear()
      self._screen.move(1, 2)
      self._screen.set_color(Color.DEFAULT)
      self._screen.write('入力キー: %s' % key)
      for color_id in range(Color.NUMBER):
        self._screen.move(3 + color_id, 2)
        self._screen.set_color(color_id)
        self._screen.write('color: %d' % color_id)

  Demo().run()
