import asyncio
import json

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
import uuid
from aiohttp import web

webApp=None

class VideoEmitter(MediaStreamTrack):
    
    kind = "video"

    def __init__(self, track, localSender):
        super().__init__()  
        self.track = track
        self.localSender=localSender

    async def recv(self):
        frame = await self.track.recv()

        self.localSender.image = frame.to_ndarray(format="bgr24")
        self.localSender.newFrame=True
        return frame


class VideoCapture:
    def __init__(self):
        global webApp
        self.newFrame=False
        self.w=0
        self.h=0
        # Also setup a web page to send and receive from
        # also serve a static website that gives control.
        async def handle(request):
            indexFile=open("static/index2.html")
            fileToSend = "\n".join(indexFile.readlines())
            indexFile.close()
            return web.Response(text=fileToSend, content_type="text/html")
        app = web.Application()
        app.add_routes([web.get('/', handle)])
        app.router.add_post("/offer", self.offer)
        webApp=app

    async def offer(self,request):
        params = await request.json()
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

        pc = RTCPeerConnection()
        pc_id = "PeerConnection(%s)" % uuid.uuid4()


        @pc.on("datachannel")
        def on_datachannel(channel):
            @channel.on("message")
            def on_message(message):
                if isinstance(message, str) and message.startswith("ping"):
                    channel.send("pong" + message[4:])

        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            if pc.iceConnectionState == "failed":
                await pc.close()
                pcs.discard(pc)

        @pc.on("track")
        def on_track(track):

            if track.kind == "video":
                pc.addTrack(VideoEmitter(track,self))

        # handle offer
        await pc.setRemoteDescription(offer)

        # send answer
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        return web.Response(
            content_type="application/json",
            text=json.dumps(
                {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
            ),
        )


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