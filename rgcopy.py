#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# main.py
import os
directory = os.path.dirname(os.path.realpath(__file__))

import imp
from gi.repository import Gtk ,Gdk ,GObject, Notify
#from commons.copy import Copy,COPY_STATUS_CODE
copy = imp.load_source('copy',os.path.join(directory,'commons/copy.py'))
from copy import Copy,COPY_STATUS_CODE
#from gui.gui import Interface as ui
gui = imp.load_source('gui',os.path.join(directory,'gui/gui.py'))
from gui import Interface as ui
import gettext ,locale, time
import urllib, urlparse
import time


STATUS_CODE = {0:'running',1:'paused'}


class Handler():

	def __init__(self,main):
		self.main = main


 	def on_btn_more_clicked(self, *args):
 		self.main.ui.scrolledwindow1.set_visible(not self.main.ui.scrolledwindow1.get_visible())

 	def on_btn_close_clicked(self,button):
 		self.main.copies[self.main.active_copy].process.kill()
		Gtk.main_quit()

	def on_btn_pause_clicked(self,button):
		if self.main.status == 0:
			self.main.copies[self.main.active_copy].process.pause_resume(self.main.status)
			self.main.status = 1
			self.main.copies[self.main.active_copy].status = 2
	 		self.main.ui.btn_pause_resume.set_label('Resume')
	 		self.main.update_ui()
		else:
			self.main.copies[self.main.active_copy].process.pause_resume(self.main.status)
			self.main.status = 0
			self.main.copies[self.main.active_copy].status = 1
	 		self.main.ui.btn_pause_resume.set_label('Pause')
	 		# GObject.idle_add(self.manage_copies)
	 		GObject.timeout_add(1000,self.main.manage_copies)
		
	#TODO: Check event handler
	def on_windows_destroy(self, *args):
 		Gtk.main_quit(*args)

class RGCopy():

	def __init__(self):

		self.ui = ui()
		self.active_copy = None
		self.ui.builder.connect_signals(Handler(self))
		self.copies_size = 0
		self.partial_copies_size = 0
		self.lines = self.get_lines_list()
		self.status = 0
		self.show_state = False
		

	def initialize(self):
		self.ui.scrolledwindow1.set_visible(False)

	def get_copies_list(self):

		cps = []
		copy_path = self.get_copy_path()
		for line in self.lines:
			if os.path.isdir(line):
				for path,dirs,files in os.walk(line,topdown=False):
					#for dr in dirs:
					relative_path = path.split(os.path.dirname(line)+os.sep)[1]#os.path.join(path,dr)
					create_path = os.path.join(copy_path,relative_path)
					if not os.path.exists(create_path):
						os.makedirs(create_path)
					for fl in files:
						relative_path = path.split(os.path.dirname(line)+os.sep)[1]
						create_path = os.path.join(copy_path,relative_path)
						copy = Copy(os.path.join(path,fl),create_path+os.sep)
						copy.file_name = os.sep.join([relative_path,fl])
						self.copies_size+= copy.size
						cps.append(copy)
						self.set_treview_model(copy)
						#self.update_process_ui(len(cps))
			else:
				copy = Copy(line,copy_path)
				self.copies_size+= copy.size
				copy.file_name = os.path.basename(line)
				cps.append(copy)
				self.set_treview_model(copy)
				#self.update_process_ui(len(cps))
		return cps

	def update_process_ui(self,cps_len):

		if cps_len > 1000:
			self.ui.rgcopy.set_title('Process: %s files-RGCopy' % str(cps_len))
			#self.ui.lbl_file_name.set_text(self.format_string(str(copy.file_name)))
			#self.ui.lbl_file_name.set_text('asdfsdf')

	def get_lines_list(self):
		lts = []
		cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
		content = cb.wait_for_text()
		for line in content.split('\n'):
			if os.path.exists(line):
				lts.append(line)
		return lts

	def convert_bytes(self,bytes):
		bytes = float(bytes * 1024)
		if bytes >= 1099511627776:
			terabytes = bytes / 1099511627776
			size = '%.2f TB' % terabytes
		elif bytes >= 1073741824:
			gigabytes = bytes / 1073741824
			size = '%.2f GB' % gigabytes
		elif bytes >= 1048576:
			megabytes = bytes / 1048576
			size = '%.2f MB' % megabytes
		elif bytes >= 1024:
			kilobytes = bytes / 1024
			size = '%.2f KB' % kilobytes
		else:
			size = '%.2f B' % bytes
		return size

	def set_treview_model(self,copy):
		self.ui.listStore.append([copy.dir,self.convert_bytes(copy.size),COPY_STATUS_CODE[copy.status]])

	def get_copy_path(self):

		try:
			dir_to_open=""
			selected=os.environ["NAUTILUS_SCRIPT_SELECTED_URIS"].split("\n")[:-1]
			#Note getting SELECTED_URIS rather than SELECTED_FILE_PATHS as later
			#is not set when ~/Desktop and ~/.Trash selected??
			if len(selected) == 1:
			    uri_bits=urlparse.urlparse(urllib.unquote(selected[0]))
			    if uri_bits[0] == "file":
			        dir_to_open=uri_bits[2]
			    elif uri_bits[0] == "x-nautilus-desktop":
			        if uri_bits[2] == "///trash":
			            dir_to_open=home_dir+'/.Trash'
			        elif uri_bits[2] == "///home":
			            dir_to_open=home_dir+'/Desktop'
			    if not os.path.isdir(dir_to_open):
			        dir_to_open=""
			if not dir_to_open: #we didn't select 1 directory so open current dir
			    current_uri=os.environ["NAUTILUS_SCRIPT_CURRENT_URI"]
			    uri_bits=urlparse.urlparse(urllib.unquote(current_uri))
			    if uri_bits[0] == "file":
			        dir_to_open=uri_bits[2]
			    elif uri_bits[0] == "x-nautilus-desktop":
			        dir_to_open=home_dir+'/Desktop'
			    elif uri_bits[0] == "trash":
			        dir_to_open=home_dir+'/.Trash'
		except Exception,e:
			#return str(e)
			return '/home/reisy/Documents/desarrollo_propio/RGCopy/test'
		return dir_to_open

	def show(self):
		self.ui.rgcopy.set_title('RGCopy')
		self.ui.rgcopy.show_all()
		self.initialize()
		GObject.threads_init()
		Gtk.main()

	def run_process(self):
		# GObject.timeout_add(1000,main.manage_copies)
		self.copies = self.get_copies_list()
		GObject.idle_add(self.manage_copies)

	def manage_copies(self):

		if self.status == 1:
			return False
		if self.active_copy is not None:
			if self.copies[self.active_copy].done:
				self.copies[self.active_copy].status = 3
				if len(self.copies) == (self.active_copy + 1):
					#Gtk.main_quit()
					self.update_ui()
					return False
				else:
					self.partial_copies_size+= self.copies[self.active_copy].size
					self.active_copy += 1
					self.copies[self.active_copy].status = 1
					self.copies[self.active_copy].process.start()
					self.update_ui(True)
					return True
			else:
				self.update_ui()
				return True
		else:
			self.active_copy = 0
			self.copies[self.active_copy].status = 1
			self.copies[self.active_copy].process.start()
			self.update_ui()
			return True


	# def manage_copies(self):
	# 	self.active_copy = 0
	# 	self.copies[self.active_copy].process.start()
	# 	#GObject.idle_add(self.update_ui)

	def update_ui(self,update_tree_view=None):

		def get_pb_all_files_values(updated_value):
			return int(((self.partial_copies_size + updated_value) * 100.0) / self.copies_size)

		copy = self.copies[self.active_copy]
		#TreeView
		self.ui.listStore[self.active_copy][2] = COPY_STATUS_CODE[self.copies[self.active_copy].status]
		if update_tree_view:
			self.ui.listStore[self.active_copy-1][2] = COPY_STATUS_CODE[3]
			#self.ui.pb_single_file.set_fraction(0)
		#pb_single_file
		# if self.ui.pb_single_file.get_fraction() < copy.percent/100.0:
		# 	self.ui.pb_single_file.set_fraction(self.ui.pb_single_file.get_fraction()+0.0003)
		self.ui.pb_single_file.set_fraction(float(copy.percent)/100)
		#pb_all_files
		fraction = get_pb_all_files_values(copy.copied_size)
		self.ui.pb_all_files.set_fraction(float(fraction)/100)
		#print str(fraction)+'%'
		#Windows Title
		self.ui.rgcopy.set_title('Copiar: %s (%s)-RGCopy' % (str(fraction)+'%',copy.speed_rate))
		if copy.file_name:
			self.ui.lbl_file_name.set_text(self.format_string(str(copy.file_name)))
		self.ui.lbl_target.set_text(self.format_string(copy.dest))


	def format_string(self,string):
		return string if len(string) <= 55 else '...%s' % string[len(string)-55:]



