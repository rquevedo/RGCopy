#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# copy_with_rgcopy.py
import imp
from threading import Thread

#rgcopy = imp.load_source('rgcopy', '/opt/rgcopy/rgcopy.py')
rgcopy = imp.load_source('rgcopy', '/media/reisy/5ff5704e-3efb-468b-b90f-4ec7a8e8369e/reisy/Documents/desarrollo_propio/RGCopy/rgcopy.py')


main = rgcopy.RGCopy()
if main.lines:
	thread = Thread(target=main.run_process)
	thread.start()
	main.show()
