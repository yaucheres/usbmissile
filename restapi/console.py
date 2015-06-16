#!/usr/bin/env python
import missile_center
from missile_center import NoMissilesError
from missile_center import missileCenter
from missile_center import MissileMoveError

class MissileNoDisplay:
  def run(self):
    try:
        m = missileCenter()
    except NoMissilesError, e:
        raise NoMissilesError
    while 1:
      keys = None
      while not keys:
        keys = raw_input("Enter something: ")
      for k in keys:
        if k == 'window resize':
          size = self.ui.get_cols_rows()
        elif k in ('w', 'up'):
            m.move(m.UP)
        elif k in ('x', 'down'):
            m.move(m.DOWN)
        elif k in ('a', 'left'):
            m.move(m.LEFT)
        elif k in ('d', 'right'):
            m.move(m.RIGHT)
        elif k in ('f', 'space'):
            m.move(m.FIRE)
        elif k in ('s'):
            m.move(m.STOP)
        elif k in ('q'):
            m.move(m.LEFTUP)
        elif k in ('e'):
            m.move(m.RIGHTUP)
        elif k in ('z'):
            m.move(m.LEFTDOWN)
        elif k in ('c'):
            m.move(m.RIGHTDOWN)
        elif k in ('r'):
          for n in range(3):
              sleep(0.5)
        elif k in ('v'):
            if  random.random() > 0.8:
              m.move(m.FIRE)
        elif k in ('esc'):
          return

try:
  MissileNoDisplay().run()
except NoMissilesError, e:
  print "No WMDs found."
