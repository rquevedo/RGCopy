#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# process.py


import fcntl, os , time , subprocess
from threading import Thread
from gi.repository import GObject
import signal

SIGNALS = {0:signal.SIGSTOP,1:signal.SIGCONT}
class Process:

	def __init__(self,copy):
		self.copy = copy
		self.main = self.copy.main
		self.process = None
		self.error = ''
		self.start_time = 0

	def get_pid(self):
		return self.process.pid

	def readoutline(self,source, condition):
		fcntl.fcntl(source, fcntl.F_SETFL, os.O_NONBLOCK)
		output = ''
		try:
			output += self.process.stdout.read()
		except Exception, e:
			pass
		split_values,file_list = self.get_split_values(output)
		self.update_copy(split_values)
		self.main.update_ui(file_list=file_list)
		return True

	def get_split_values(self,output):
		update_ui_values = {}
		file_list = []
		values = [i for i in output.split(' ') if i != '\r' and i != '']
		name_values = [i.split('\n') for i in output.split('\r')]
		for n in name_values:
			file_list.extend(n)
		file_list = [i for i in file_list if not i.startswith(' ') and i != '' and not i.startswith('sending incremental file list') and i.find('speedup is') == -1 and i.find('bytes/sec') == -1 and not i.endswith('/')]
		if len(values) == 4 and values[1].endswith('%'):
			update_ui_values['percent'] = int(values[1][0:-1])
			update_ui_values['copied_size'] = int(values[0])
			update_ui_values['speed_rate'] = values[2]
			update_ui_values['ETA'] = values[3]
		return update_ui_values,file_list

	def update_copy(self,values):
		for key in values.keys():
			self.copy[key] = values[key]

	def pause_resume(self,status):
		os.kill(self.get_pid(), SIGNALS[status])

	def kill(self):
		if not self.process.poll():
			os.kill(self.get_pid(), signal.SIGKILL)

	def start(self):

		cmd = ['rsync','-Pa']
		cmd.append(self.copy.dir)
		cmd.append(self.copy.dest)
		self.process = subprocess.Popen(cmd, bufsize=-1, stdout=subprocess.PIPE)#, stderr=subprocess.PIPE
		GObject.io_add_watch(self.process.stdout, GObject.IO_IN, self.readoutline)


