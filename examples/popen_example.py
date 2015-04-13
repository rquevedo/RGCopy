

import sys
from subprocess import PIPE, Popen
from threading  import Thread

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()#rsync -Pha /media/Datos/Entretenimiento/Peliculas/Unknown.wmv  /home/reisy/Desktop/  1>&2

p = Popen(['/usr/bin/rsync', '-Pha', '/home/reisy/Videos/nuevos/El Club de la Comedia 1x01.avi', '/home/reisy/Desktop/', '1>&2'], bufsize=0, stdout=PIPE)
q = Queue()
t = Thread(target=enqueue_output, args=(p.stdout, q))
t.daemon = True # thread dies with the program
t.start()

# ... do other things here

# read line without blocking
line = None
while not line :
	
	try:  
		line = q.get_nowait() # or q.get(timeout=.1)
		print line	
	except Empty:
		pass
		
