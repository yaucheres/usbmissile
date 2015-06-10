import logging
import asyncio

import api_hour
import aiohttp.web
from aiohttp.web import Response
from api_hour.plugins.aiohttp import JSON
logging.basicConfig(level=logging.INFO)  # enable logging for api_hour
import center_missile 

class Container(api_hour.Container):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Declare HTTP server
        self.servers['http'] = aiohttp.web.Application(loop=kwargs['loop'])
        self.servers['http'].ah_container = self  # keep a reference in HTTP server to Container

        # Define HTTP routes
        self.servers['http'].router.add_route('GET','/',self.index)
        self.servers['http'].router.add_route('GET',"/{name}",self.variable_handler)
        #self.servers['http'].router.add_route('GET','/left',self.left)
        #self.servers['http'].router.add_route('GET','/right',self.right)
        #self.servers['http'].router.add_route('GET','/up',self.up)
        #self.servers['http'].router.add_route('GET','/down',self.down)
        #self.servers['http'].router.add_route('GET','/leftup',self.leftup)
        #self.servers['http'].router.add_route('GET','/rightup',self.rightup)
        #self.servers['http'].router.add_route('GET','/leftdown',self.leftdown)
        #self.servers['http'].router.add_route('GET','/rightdown',self.rightdown)
        #self.servers['http'].router.add_route('GET','/pause',self.pause)
        #self.servers['http'].router.add_route('GET','/fire',self.fire)

    # A HTTP handler example
    # More documentation: http://aiohttp.readthedocs.org/en/latest/web.html#handler
    @asyncio.coroutine
    def index(self, request):
        self.missile_
        message = 'Hello World !'
        return Response(text=message)



    
    @asyncio.coroutine
    def variable_handler(self, request):
        try:
            {'left':self.missile.move(centerMissile.LEFT),
            'right':self.missile.move(centerMissile.RIGHT),
            'up':self.missile.move(centerMissile.UP),
            'down':self.missile.move(centerMissile.DOWN),
            'leftup':self.missile.move(centerMissile.LEFTUP),
            'rightup':self.missile.move(centerMissile.RIGHTUP),
            'leftdown':self.missile.move(centerMissile.LEFTDOWN),
            'rightdown':self.missile.move(centerMissile.RIGHTDOWN),
            'pause':self.missile.move(centerMissile.STOP),
            'fire':self.missile.move(centerMissile.FIRE)}["{}"]()
        except KeyError:
          return JSON({"command":"{}","status":"error", "message":"unknown command"})
        except NoMissileError:
          return JSON({"command":"{}","status":"error", "message":"problem initialising the missile"})
        except MissileMoveError:
          return JSON({"command":"{}","status":"error", "message":"failed to make the {} action"})
            
                    

#     asyncio.coroutine
#     def left(self, request):
#         message = 'On the left !'
#         return JSON({"command":"left","status":"success", "message":message})
# 
#     @asyncio.coroutine
#     def right(self, request):
#         message = 'On the right !'
#         return JSON({"command":"right","status":"success", "message":message})
# 
#     @asyncio.coroutine
#     def up(self, request):
#         message = 'Uptown  funky you up !'
#         return JSON({"command":"up","status":"success", "message":message})
# 
#     @asyncio.coroutine
#     def down(self, request):
#         message = 'Down !'
#         return JSON({"command":"down","status":"success", "message":message})
# 
#     @asyncio.coroutine
#     def leftdown(self, request):
#         message = 'Left Down !'
#         return JSON({"command":"leftdown","status":"success", "message":message})
# 
#     @asyncio.coroutine
#     def pause(self, request):
#         message = 'Stop !'
#         return JSON({"command":"pause","status":"success", "message":message})
# 
#     @asyncio.coroutine
#     def rightdown(self, request):
#         message = 'Right Down !'
#         return JSON({"command":"rightdown","status":"success", "message":message})
# 
#     @asyncio.coroutine
#     def fire(self, request):
#         message = 'Fire in the hole !'
#         return JSON({"command":"fire","status":"success", "message":message})

    # Container methods
    @asyncio.coroutine
    def start(self):
        # A coroutine called when the Container is started
        yield from super().start()
        self.missile = missileCenter() 


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
