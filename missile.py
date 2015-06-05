#!/usr/bin/env python
import usb.core
import usb.util

class NoMissilesError(Exception): pass

class centerMissileDevice:
  dev       = None
  handle    = None
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

  def __init__(self,usbdevice):
      try:
        self.handle = usbdevice.open()
        self.handle.reset()
        return
      except NoMissilesError, e:
        raise NoMissilesError()

  def move(self, direction):
     self.handle.controlMsg(0x21, 0x09, [0x5f, direction, 0xe0, 0xff, 0xfe], 0x0300, 0x00)

class UsbDevice:
  def __init__(self):
    self.handle = None
    self.launcher = None
    self.dev = None
    self.busses = usb.busses()

  def probe(self):
    dev = usb.core.find(idVendor=0x0416,idProduct=0x9391)
    self.dev = dev
    self.conf = self.dev.configurations[0]
    self.intf = self.conf.interfaces[0][0]
    self.endpoints = []
    for endpoint in self.intf.endpoints:
      self.endpoints.append(endpoint)
    self.launcher = legacyMissileDevice
    return self.launcher

    raise NoMissilesError()

  def open(self):
    if self.handle:
      self.handle = None
    self.handle = self.dev.open()
    try:
      self.handle.detachKernelDriver(0)
      self.handle.detachKernelDriver(1)
    except usb.USBError, err:
      print >> sys.stderr, err

    self.handle.setConfiguration(self.conf)
    self.handle.claimInterface(self.intf)
    self.handle.setAltInterface(self.intf)
