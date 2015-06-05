#!/usr/bin/env python
import usb.core
import usb.util

class NoMissilesError(Exception): pass

class centerMissileDevice:
  dev       = None
  ep        = None
  STOP      = 0x0
  LEFT      = 0x8
  RIGHT     = 0x4
  UP        = 0x2
  DOWN      = 0x1
  LEFTUP    = LEFT + UP
  RIGHTUP   = RIGHT + UP
  LEFTDOWN  = LEFT + DOWN
  RIGHTDOWN = RIGHT + DOWN
  FIRE      = 0x10

  def __init__(self):
      try:
       self.dev = usb.core.find(idVendor=0x0416,idProduct=0x9391)
       if self.dev is None:
         raise ValueError('Device not found')
       self.dev.set_configuration()
       self.conf = self.dev.get_active_configuration()
       self.intf = self.conf[(0,0)]
       self.ep = usb.util.find_descriptor(
        self.intf,
        # match the first IN endpoint
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_IN)
       return
      except NoMissilesError, e:
        raise NoMissilesError()

  def move(self, direction):
     #self.ep.write(0x21, 0x09, [0x5f, direction, 0xe0, 0xff, 0xfe], 0x0300, 0x00)
     #self.ep.write(0x21, [0x5f, direction, 0xe0, 0xff, 0xfe])
     self.dev.ctrl_transfer(0x21, 0x09,0x0300,0x00,[0x5f, direction, 0xe0, 0xff, 0xfe])


class MissileNoDisplay:
  def run(self):
    try:
        m = centerMissileDevice()
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
