#!/usr/bin/env python
import usb.core
import usb.util
import time

class NoMissilesError(Exception): pass
class MissileMoveError(Exception): pass

class missileCenter:
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
       return
      except NoMissilesError, e:
        raise NoMissilesError()

  def move(self, direction):
     try:
      #do the move
      self.dev.ctrl_transfer(0x21, 0x09,0x0300,0x00,[0x5f, direction, 0xe0, 0xff, 0xfe])
      #sleep while the missile is doing his move
      time.sleep(0.5)
      #then stop
      self.dev.ctrl_transfer(0x21, 0x09,0x0300,0x00,[0x5f, STOP, 0xe0, 0xff, 0xfe])
     except:
       raise MissileMoveError()
