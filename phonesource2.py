import numpy as np
import asyncio
import json

try:
    import websockets
except ImportError:
    print("Please `pip install websockets` to continue.")
    exit(0)
try:
    from aiohttp import web
except ImportError:
    print("Please `pip install aiohttp` to continue.")
    exit(0)

webApp=None

class VideoCapture:
    def __init__(self):
        global webApp
        self.websocket=None
        self.newFrame=False
        self.w=0
        self.h=0
        # start listening for websocket
        start_server= websockets.serve(self.acceptWSClient, port=3988, max_size=None)
        asyncio.get_event_loop().run_until_complete(start_server)
        # Also setup a web page to send and receive from
        # also serve a static website that gives control.
        indexFile=open("static/index.html")
        fileToSend = "\n".join(indexFile.readlines())
        indexFile.close()
        async def handle(request):
            return web.Response(text=fileToSend, content_type="text/html")
        app = web.Application()
        app.add_routes([web.get('/', handle)])
        webApp=app


    async def read(self):
        while not self.newFrame:
            # wait until the frame has arrived
            await asyncio.sleep(0.1)
        self.newFrame=False
        return (True, self.image)

    async def acceptWSClient(self, ws,path):
        if self.websocket is not None:
            self.websocket.close()
        self.websocket = ws
        try: 
            async for message in ws:
                if type(message) is bytes:
                    #try:
                    buffer=np.frombuffer(message,dtype=np.uint8)
                    self.image = buffer.reshape((self.h, self.w, 4))
                    self.image=self.image[:,:,:3] # ditch the alpha channel
                    self.newFrame=True
                    #except IO:
                elif type(message) is str:
                    print ("i am a message")
                    # this is a config message
                    settingsDict=json.loads(message)
                    self.w=settingsDict['w']
                    self.h=settingsDict['h']
                    print (settingsDict)
                    # set config as appropriate
        except websockets.exceptions.ConnectionClosedError:
            print ("disconnected")
            self.websocket=None

def start():
    if webApp:
        web.run_app(webApp,port=8011)

def output():
    # convert the frame into binary
    # send over websocket
    pass