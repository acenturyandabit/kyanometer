import cv2
import asyncio
from aiohttp import web
import websockets

from tts import multiprocessing_text_outputter as mpto

videoSource=0
#videoSource="http://192.168.43.1:8083/video"



from Img2Barcode import Barcode_Func_file as BarcodeReader




if __name__=="__main__":
    # we are multithreading so be safe
    controlSocket=None
    commandQueue=[]
    async def handleWSClient(ws, path):
        global controlSocket
        global commandQueue
        if controlSocket is not None:
            await controlSocket.close()
        controlSocket=ws
        try:
            async for message in ws:
                #decode messages
                # message is in format (dx,dy)... unless its not
                commandQueue.append(message)
        except websockets.exceptions.ConnectionClosedError:
            print("disconnected")
            pass
    start_server= websockets.serve(handleWSClient, port=3943)
    asyncio.get_event_loop().run_until_complete(start_server)

    bufferFrame = None
    bufferFlip=False
    async def getFrames():
        global bufferFlip
        while True:
            while bufferFlip==False:
                #wait for buffer
                await asyncio.sleep(0.1)
            bufferFlip=False
            img = cv2.resize(bufferFrame, (480, 320))
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'+frame+b'\r\n'



    mpto.start_engine()
    async def main():
        throttle=0
        isOK=True
        global bufferFrame
        global bufferFlip
        sparklyFrame=None
        source = cv2.VideoCapture(videoSource)
        while isOK:
            isOK, frame = source.read()
            # do processing
            if isOK:
                if throttle==10:
                    bufferFrame=frame
                    bufferFlip=True
                    throttle=0
                throttle=throttle+1

                if len(commandQueue):
                    latestCommand= commandQueue.pop(0)
                    if latestCommand=="helloworld":
                        mpto.output_text("hello world")
                    elif latestCommand=="barcode":
                        (result, sparklyFrame) = Barcode.BarcodeDetect(frame)
                        mpto.output_text(result)
                    else:
                        mpto.output_text("unknown command")
                cv2.imshow("Video feed",frame)
                if sparklyFrame:
                    cv2.imshow("Kyanometer output",sparklyFrame)
                key=cv2.waitKey(1)
                await asyncio.sleep(0.1)
                pass
            else:
                break
        mpto.all_text_complete()
        source.release()
        cv2.destroyAllWindows()
        return


    asyncio.get_event_loop().create_task(main())
    async def videoSender(request):
        response = web.StreamResponse()
        response.content_type = 'multipart/x-mixed-replace; boundary=frame'
        await response.prepare(request)
        async for frame in getFrames():
            await response.write(frame)
        return response

    # also serve a static website that gives control.
    async def handle(request):
        indexFile=open("static/index.html")
        fileToSend = "\n".join(indexFile.readlines())
        indexFile.close()
        
        return web.Response(text=fileToSend, content_type="text/html")

    app = web.Application()
    app.add_routes([web.get('/', handle), web.get('/video', videoSender)])
    web.run_app(app,port=8045)


    asyncio.get_event_loop().run_forever()
