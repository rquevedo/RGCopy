import os
directory = os.path.dirname(os.path.realpath(__file__))
import imp
process = imp.load_source('process', os.path.join(directory, 'process.py'))
from process import Process
import subprocess

COPY_STATUS_CODE = {0:'waiting', 1:'running', 2:'paused', 3:'copied'}

class Copy():

	def __init__(self, direction, dest, main, action, is_dir=False):
		self.values = {}
		self.values['dir'] = direction
		self.values['dest'] = dest
		self.values['percent'] = 0
		self.values['copied_size'] = 0
		self.values['ETA'] = ''
		self.values['speed_rate'] = ''
		self.values['main'] = main
		self.values['action'] = action
		self.values['status'] = 0
		self.values['is_dir'] = is_dir
		self.values['process'] = Process(self)
		
		
	
	def get_size(self):
		
		if self.values['is_dir']:
			return None
		else:
			return os.path.getsize(self.values['dir'])

	def __setitem__(self, key, value):

		self.values[key] = value

	def __getattr__(self, key):
		return self.values[key]
