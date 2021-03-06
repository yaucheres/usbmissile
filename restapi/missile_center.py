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
          
          #get usb
          self.dev = usb.core.find(idVendor=0x0416,idProduct=0x9391)
          if self.dev is None:
              raise ValueError('Device not found')
          #set config if not already set
          if self.dev.get_active_configuration() is None :
              self.dev.set_configuration()
              print('initailised usb')
          return
      except Exception as e:
          print(e)
          raise NoMissilesError(e)

  def move(self, direction):
     try:
         #do the move
         self.dev.ctrl_transfer(0x21, 0x09,0x0300,0x00,[0x5f, direction, 0xe0, 0xff, 0xfe])
         #sleep while the missile is doing his move
         time.sleep(0.5)
         #then stop
         self.dev.ctrl_transfer(0x21, 0x09,0x0300,0x00,[0x5f, self.STOP, 0xe0, 0xff, 0xfe])
     except Exception as e:
         raise MissileMoveError(e)

  def fire(self):
     try:
         #send fire command
         self.dev.ctrl_transfer(0x21, 0x09,0x0300,0x00,[0x5f, self.FIRE, 0xe0, 0xff, 0xfe])
         #sleep while the missile is firing
         time.sleep(2)
         #then stop
         self.dev.ctrl_transfer(0x21, 0x09,0x0300,0x00,[0x5f, self.STOP, 0xe0, 0xff, 0xfe])
     except Exception as e:
         raise MissileMoveError(e)



  def fireall(self):
     try:
         #send fire command
         self.dev.ctrl_transfer(0x21, 0x09,0x0300,0x00,[0x5f, self.FIRE, 0xe0, 0xff, 0xfe])
         #sleep while the missile is firing
         time.sleep(30)
         #then stop
         self.dev.ctrl_transfer(0x21, 0x09,0x0300,0x00,[0x5f, self.STOP, 0xe0, 0xff, 0xfe])
     except Exception as e:
         raise MissileMoveError(e)

