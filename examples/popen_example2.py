import os
from asyncproc import Process
myProc = Process("rsync -Pha /home/reisy/Videos/nuevos/El Club de la Comedia 1x01.avi /home/reisy/Desktop/")

while True:
    # check to see if process has ended
    poll = myProc.wait(os.WNOHANG)
    if poll != None:
        break
    # print any new output
    out = myProc.read()
    if out != "":
        print out
