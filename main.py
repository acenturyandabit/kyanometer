import cv2
import asyncio
import phonesource2

class awaitableVideoCapture:
    def __init__(self,sourceArg):
        self.source=cv2.VideoCapture(sourceArg)
    async def read(self):
        return self.source.read()

source = awaitableVideoCapture("http://192.168.43.1:8083/video")

def localDisplay(frame, result):
    cv2.imshow("frame",frame)
    key=cv2.waitKey(1)
    pass

displayResult = localDisplay
#displayResult = CustomWebserver.output


async def main():
    print ("hi")
    isOK=True
    while isOK:
        isOK, frame = await source.read()
        # do processing
        if isOK:
            displayResult(frame, result={})

asyncio.get_event_loop().create_task(main())
#phonesource2.start()
asyncio.get_event_loop().run_forever()