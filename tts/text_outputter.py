import pyttsx3
import threading
import time
import functools


engine = pyttsx3.init()
engine.setProperty('rate', 500)
sayQueue=[]
sayDict={}
endRequireds=0
ended=True
def onEnd(name, completed):
    print ("i is finished")
    print (name)
    global ended
    ended=True
engine.connect('finished-utterance',onEnd)

def speech_digester_loop():
    engine.startLoop(False)
    global sayQueue
    global ended
    global endRequireds
    while threading.main_thread().is_alive() or (not ended) or (endRequireds>0):
        if len(sayQueue) and ended:
            ended=not sayDict[sayQueue[0]][1] # if we must wait for end then set ended to false
            if sayDict[sayQueue[0]][1]:
                endRequireds=endRequireds-1
            engine.say(sayDict[sayQueue[0]][0],sayQueue[0])
            sayQueue.pop()
        engine.iterate()
        print (ended)
        print (threading.main_thread().is_alive())
        print (endRequireds)
    print ("ended was {}".format(ended))
    engine.endLoop()

speechThread = threading.Thread(target=speech_digester_loop)
speechThread.start()

counter=0
def output_text(text,waitFinish=False):
    global sayQueue
    global sayDict
    global counter
    global endRequireds
    name=str(time.time()+counter)
    counter=counter+1
    sayDict[name]=(text,waitFinish)
    if (waitFinish):
        endRequireds=endRequireds+1
    sayQueue.append(name)

#    sayqueue.append(text)
if __name__=="__main__":
    output_text("hello world",True)
    exit(0)
    # output_text("goodbye world",True)
    # output_text("you should not hear this")
    # output_text("you should only hear part of this")
    # time.sleep(3)
    # output_text("you should hear all of this",True)
#engine.runAndWait()

