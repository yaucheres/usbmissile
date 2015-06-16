import logging
import asyncio

import api_hour
import aiohttp.web
from aiohttp.web import Response
from api_hour.plugins.aiohttp import JSON
import missile_center 
from missile_center import NoMissilesError
from missile_center import missileCenter
from missile_center import MissileMoveError

logging.basicConfig(level=logging.INFO)  # enable logging for api_hour

class Container(api_hour.Container):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Declare HTTP server
        self.servers['http'] = aiohttp.web.Application(loop=kwargs['loop'])
        self.servers['http'].ah_container = self  # keep a reference in HTTP server to Container

        # Define HTTP routes
        self.servers['http'].router.add_route('GET','/left',self.left)
        self.servers['http'].router.add_route('GET','/right',self.right)
        self.servers['http'].router.add_route('GET','/up',self.up)
        self.servers['http'].router.add_route('GET','/down',self.down)
        self.servers['http'].router.add_route('GET','/leftup',self.leftup)
        self.servers['http'].router.add_route('GET','/rightup',self.rightup)
        self.servers['http'].router.add_route('GET','/leftdown',self.leftdown)
        self.servers['http'].router.add_route('GET','/rightdown',self.rightdown)
        self.servers['http'].router.add_route('GET','/pause',self.pause)
        self.servers['http'].router.add_route('GET','/fire',self.fire)
        self.servers['http'].router.add_route('GET','/fireall',self.fireall)

    def sendCommandToMissileCenter(self,command, commandName):
        self.missile = missileCenter() 
        try:
            self.missile = missileCenter() 
            self.missile.move(command)
            return JSON({"command":commandName,"status":"success", "message":"moved to the " + commandName})
        except NoMissilesError:
            return JSON({"command":init,"status":"error", "message":"problem initialising the missile"})
        except MissileMoveError:
            return JSON({"command":commandName,"status":"error", "message":"failed to make the " + commandName + " action"})
                

    # A HTTP handler example
    # More documentation: http://aiohttp.readthedocs.org/en/latest/web.html#handler
    @asyncio.coroutine
    def left(self, request):
         return self.sendCommandToMissileCenter(missileCenter.LEFT,"left")
 
    @asyncio.coroutine
    def right(self, request):
        return self.sendCommandToMissileCenter(missileCenter.RIGHT,"right")
 
    @asyncio.coroutine
    def up(self, request):
        return self.sendCommandToMissileCenter(missileCenter.UP,"up")
 
    @asyncio.coroutine
    def down(self, request):
        return self.sendCommandToMissileCenter(missileCenter.DOWN,"down")
 
    @asyncio.coroutine
    def leftdown(self, request):
        return self.sendCommandToMissileCenter(missileCenter.LEFTDOWN,"leftdown")

    @asyncio.coroutine
    def rightdown(self, request):
        return self.sendCommandToMissileCenter(missileCenter.RIGHTDOWN,"rightdown")

    @asyncio.coroutine
    def leftup(self, request):
        return self.sendCommandToMissileCenter(missileCenter.LEFTUP,"leftup")

    @asyncio.coroutine
    def rightup(self, request):
        return self.sendCommandToMissileCenter(missileCenter.RIGHTUP,"rightup")
 
    @asyncio.coroutine
    def pause(self, request):
        return self.sendCommandToMissileCenter(missileCenter.STOP,"stop")
 
    @asyncio.coroutine
    def fire(self, request):
        self.missile = missileCenter() 
        try:
            self.missile = missileCenter() 
            self.missile.fire()
            return JSON({"command":"fire","status":"success", "message":"fired missile"})
        except NoMissilesError:
            return JSON({"command":init,"status":"error", "message":"problem initialising the missile"})
        except MissileMoveError:
            return JSON({"command":"fire","status":"error", "message":"failed to fire"})
                


    @asyncio.coroutine
    def fireall(self, request):
        self.missile = missileCenter() 
        try:
            self.missile = missileCenter() 
            self.missile.fireall()
            return JSON({"command":"fireall","status":"success", "message":"fired all missile"})
        except NoMissilesError:
            return JSON({"command":init,"status":"error", "message":"problem initialising the missile"})
        except MissileMoveError:
            return JSON({"command":"fire","status":"error", "message":"failed to fire all missiles"})



    # Container methods
    @asyncio.coroutine
    def start(self):
        # A coroutine called when the Container is started
        yield from super().start()


    @asyncio.coroutine
    def stop(self):
        # A coroutine called when the Container is stopped
        yield from super().stop()


    def make_servers(self):
        # This method is used by api_hour command line to bind your HTTP server on socket
        return [self.servers['http'].make_handler(logger=self.worker.log,
                                                  keep_alive=self.worker.cfg.keepalive,
                                                  access_log=self.worker.log.access_log,
                                                  access_log_format=self.worker.cfg.access_log_format)]
