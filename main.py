import cv2
import asyncio
import phonesource

class awaitableVideoCapture:
    def __init__(self,sourceArg):
        self.source=cv2.VideoCapture(sourceArg)
    async def read(self):
        return self.source.read()

source = awaitableVideoCapture(0)
#source = phonesource.VideoCapture()
#source = awaitableVideoCapture("videosample.mp4")

def localDisplay(frame, result):
    cv2.imshow("frame",frame)
    key=cv2.waitKey(1)
    pass

displayResult = localDisplay
#displayResult = phonesource.output


async def main():
    print ("hi")
    isOK=True
    while isOK:
        isOK, frame = await source.read()
        # do processing
        if isOK:
            displayResult(frame, result={})

asyncio.get_event_loop().create_task(main())
phonesource.start()
asyncio.get_event_loop().run_forever()