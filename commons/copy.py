import os
directory = os.path.dirname(os.path.realpath(__file__))
#from process import Process
import imp
#from commons.copy import Copy,COPY_STATUS_CODE
process = imp.load_source('process',os.path.join(directory,'process.py'))
from process import Process
import subprocess

COPY_STATUS_CODE = {0:'waiting',1:'running',2:'paused',3:'copied'}

class Copy():

	def __init__(self,direction,dest):
		self.values = {}
		self.values['dir'] = direction
		self.values['dest'] = dest
		self.values['percent'] = 0
		self.values['copied_size'] = 0
		self.values['ETA'] = ''
		self.values['speed_rate'] = ''
		self.values['file_name'] = None
		self.values['process'] = Process(self)
		self.values['status'] = 0
		self.values['done'] = False
		self.values['size'] = os.path.getsize(direction)/1024.0
		#self.get_size()
	
	def get_size(self):
		cmd = ['/usr/bin/du','-s']
		cmd.append(self.dir)
		process = subprocess.Popen(cmd, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		string_value = process.stdout.readline().split('\t')[0]
		self.values['size'] = int(string_value)

	# def __getitem__(self, key):
	# 	return self.values[key]

	def __setitem__(self, key,value):
		self.values[key] = value
	# def __setattr__(self,key,value):
	# 	self.values[key] = value

	def __getattr__(self,key):
		return self.values[key]
