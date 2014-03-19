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
		self.process = None
		self.error = ''
		self.start_time = 0
		self.running = True
		self.cont = 0

	def get_pid(self):
		return self.process.pid

	def readoutlineeeee(self):
	 	fcntl.fcntl(self.process.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
	 	if self.running:
	 		while True:
	 			output = ''
	 			try:
	 				output += self.process.stdout.read()
	 				break
	 			except Exception, e:
	 				pass

	 		self.update_copy(self.get_split_values(output))

	 	if self.process.poll() != None:
	 		self.update_copy({'done':True,'percent':100,'copied_size':self.copy.size})
	 		return False
	 	return True

	def readoutline(self,source, condition):
		fcntl.fcntl(source, fcntl.F_SETFL, os.O_NONBLOCK)
		#if self.running:
		output = ''
		try:
			output += self.process.stdout.read()
		except Exception, e:
			pass
		self.update_copy(self.get_split_values(output))
		#print 'Pid: '+ str(self.process.pid) + ' Process: ' + str(self.process.poll())
		if self.process.poll() != None:
			self.update_copy({'done':True,'percent':100,'copied_size':self.copy.size})
			self.process.stdout.close()
			return False
		if output.find('speedup is') != -1:
			self.cont += 1
			print self.cont
			self.process.stdout.close()
			self.kill()
			self.update_copy({'done':True,'percent':100,'copied_size':self.copy.size})
			return False
		return True

	def get_split_values(self,output):
		update_ui_values = {}
		values = [i for i in output.split(' ') if i != '\r' and i != '']
		if len(values) == 4 and values[1].endswith('%'):
			update_ui_values['percent'] = int(values[1][0:-1])
			update_ui_values['copied_size'] = int(values[0])/1024.0
			update_ui_values['speed_rate'] = values[2]
			update_ui_values['ETA'] = values[3]
		return update_ui_values

	def update_copy(self,values):
		for key in values.keys():
			self.copy[key] = values[key]

	def pause_resume(self,status):
		os.kill(self.get_pid(), SIGNALS[status])
		#self.running = not self.running
		#if self.running:
		#	GObject.io_add_watch(self.process.stdout, GObject.IO_IN, self.readoutline)

	def kill(self):
		os.kill(self.get_pid(), signal.SIGKILL)

	def start(self):

		cmd = ['rsync','-Pa']
		cmd.append(self.copy.dir)
		cmd.append(self.copy.dest)
		self.process = subprocess.Popen(cmd, bufsize=-1, stdout=subprocess.PIPE)#, stderr=subprocess.PIPE
		#GObject.timeout_add(1000,self.readoutline)
		GObject.io_add_watch(self.process.stdout, GObject.IO_IN, self.readoutline)

	# def start(self):
	# 	thread = Thread(target=self.run_process)
	# 	thread.start()

