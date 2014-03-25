#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# main.py
import os
directory = os.path.dirname(os.path.realpath(__file__))

import imp
from gi.repository import Gtk ,Gdk ,GObject,Unity,Dbusmenu
copy = imp.load_source('copy',os.path.join(directory,'commons/copy.py'))
from copy import Copy,COPY_STATUS_CODE
gui = imp.load_source('gui',os.path.join(directory,'gui/gui.py'))
from gui import Interface as ui
import gettext ,locale
import urllib, urlparse
import datetime



STATUS_CODE = {0:'running',1:'paused'}
CONVERSION_RATE = {'b/s':1,'kB/s':1024,'MB/s':1048576,'GB/s':1073741824}


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
			self.main.copies[self.main.active_copy].status = 2
	 		self.main.ui.btn_pause_resume.set_label('Resume')
	 		self.main.update_ui(copy_paused=True)
			self.main.copies[self.main.active_copy].process.pause_resume(self.main.status)
			self.main.status = 1
		else:
			
			self.main.copies[self.main.active_copy].status = 1
			self.main.update_ui(copy_paused=True)
	 		self.main.ui.btn_pause_resume.set_label('Pause')
	 		GObject.idle_add(self.main.manage_copies)
	 		self.main.copies[self.main.active_copy].process.pause_resume(self.main.status)
			self.main.status = 0
		
	#TODO: Check event handler
	def on_windows_destroy(self, *args):
 		Gtk.main_quit(*args)

class RGCopy():

	def __init__(self):

		self.ui = ui()
		self.active_copy = None
		self.active_dir_copy = -1
		self.file_list = []
		self.ui.builder.connect_signals(Handler(self))
		self.copies_size = 0
		self.partial_copies_size = 0
		self.lines = self.get_lines_list()
		self.status = 0
		self.cont = 0
		self.show_state = False
		

	def initialize(self):
		self.ui.scrolledwindow1.set_visible(False)

	def get_copies_list(self):

		cps = []
		copy_path = self.get_copy_path()
		for line in self.lines:
			if not os.path.isdir(line):
				
				copy = Copy(line,copy_path,self)
				copy_size = copy.get_size()
				self.copies_size+= copy_size
				file_name = os.path.basename(line)
				parent_dir = os.path.dirname(line)
				self.file_list.append((parent_dir,file_name,copy_size))
			
			else:				
				copy = Copy(line,copy_path,self,True)
				paths = []
				files_dic = {}
				for path,dirs,files in os.walk(line):
					paths.append(path)
					files_dic[path]=files
				paths.sort()
				for path in paths:
					files = files_dic[path]
					if files:
						files.sort()
						for fl in files:
							full_path = os.path.join(path,fl)
							copy_size = os.path.getsize(full_path)#/1024.0
							self.copies_size+= copy_size
							self.file_list.append((path,fl,copy_size))
			cps.append(copy)
		self.set_treview_model()
		return cps

	def get_lines_list(self):
		lts = []
		cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
		content = cb.wait_for_text()
		for line in content.split('\n'):
			if os.path.exists(line):
				lts.append(line)
		return lts

	def convert_bytes(self,bytes):
		if bytes >= 1099511627776:
			terabytes = bytes / 1099511627776.0
			size = '%.2f TB' % terabytes
		elif bytes >= 1073741824:
			gigabytes = bytes / 1073741824.0
			size = '%.2f GB' % gigabytes
		elif bytes >= 1048576:
			megabytes = bytes / 1048576.0
			size = '%.2f MB' % megabytes
		elif bytes >= 1024:
			kilobytes = bytes / 1024.0
			size = '%.2f KB' % kilobytes
		else:
			size = '%.2f B' % bytes
		return size

	def set_treview_model(self):

		for fl in self.file_list:
			self.ui.listStore.append([fl[1],self.convert_bytes(fl[2]),COPY_STATUS_CODE[0],fl[0]])

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
			#return home_dir
			return '/media/reisy/5ff5704e-3efb-468b-b90f-4ec7a8e8369e/reisy/Documents/desarrollo_propio/RGCopy/test'
		return dir_to_open

	def show(self):

		def maximize(attr1,attr2):
			self.ui.rgcopy.present()
		#Setting nautilus launcher properties
		self.launcher = Unity.LauncherEntry.get_for_desktop_id ("nautilus.desktop")
		ql = Dbusmenu.Menuitem.new ()
		item1 = Dbusmenu.Menuitem.new ()
		item1.property_set (Dbusmenu.MENUITEM_PROP_LABEL, "Show copy dialog")
		item1.property_set_bool (Dbusmenu.MENUITEM_PROP_VISIBLE, True)
		item1.connect('item-activated',maximize)
		ql.child_append (item1)
		self.launcher.set_property("quicklist", ql)

		self.ui.rgcopy.set_title('RGCopy')
		self.ui.rgcopy.show_all()
		self.initialize()
		GObject.threads_init()
		Gtk.main()

	def run_process(self):
		self.copies = self.get_copies_list()
		GObject.idle_add(self.manage_copies)

	def manage_copies(self):

		if self.status == 1:
			return False
		if self.active_copy is not None:
			if self.copies[self.active_copy].process.process.poll() != None:
				print self.copies[self.active_copy].process.process.poll()
				self.copies[self.active_copy].process.update_copy({'percent':100,'copied_size':self.file_list[self.active_dir_copy][2]})
				self.update_ui()
				self.copies[self.active_copy].status = 3
				if len(self.copies) == (self.active_copy + 1):
					self.update_ui(True)
					self.launcher.set_property("urgent", True)
					#Gtk.main_quit()
				else:
					self.active_copy += 1
					self.copies[self.active_copy].status = 1
					self.copies[self.active_copy].process.start()
					return True
			else:
				return True
		else:
			self.active_copy = 0
			self.copies[self.active_copy].status = 1
			self.copies[self.active_copy].process.start()
			self.launcher.set_property("progress_visible", True)
			return True

	def update_ui(self,copy_done=None,file_list=None,copy_paused=False):

		def get_pb_all_files_values(updated_value):
			return int(((self.partial_copies_size + updated_value) * 100.0) / self.copies_size)

		def convert_to_bytes(rate):
			if rate:
				mu = rate[-4:]
				value = rate[:-4]
				return float(value)*CONVERSION_RATE[mu]
			return None



		def get_total_eta(rate):
			b_p_s = convert_to_bytes(rate)
			if b_p_s:
				left = self.copies_size - (self.partial_copies_size + copy.copied_size)
				seconds = left / b_p_s
				eta = str(datetime.timedelta(seconds=round(seconds)))
				return eta
			return '--:--:--'

		# def build_progress_bar_text(text1,percent,text2):

		# 	txt = text1
		# 	while len(txt) < 55:
		# 		txt+=' '
		# 	p = str(percent)
		# 	while len(p) != 3:
		# 		p = ' ' + p
		# 	txt+= p + '%'
		# 	while len(txt) < 120-len(text2):
		# 		txt+=' '
		# 	txt+=text2
		# 	return txt

		copy = self.copies[self.active_copy]
		
		if file_list:
			try:
				for fl in file_list:

					self.active_dir_copy += 1
					if self.active_dir_copy > 0:
						
						#Adding file size to partial list
						self.partial_copies_size+= self.file_list[self.active_dir_copy-1][2]
						
						#Set to copied last file and set to running current
						self.ui.listStore[self.active_dir_copy-1][2] = COPY_STATUS_CODE[3]
						self.ui.listStore[self.active_dir_copy][2] = COPY_STATUS_CODE[1]
						#Set file name and dest
						self.ui.lbl_file_name.set_text(self.format_string(fl))
						self.ui.lbl_target.set_text(self.format_string(copy.dest))
					else:
						#Set file name and dest
						self.ui.lbl_file_name.set_text(self.format_string(fl))
						self.ui.lbl_target.set_text(self.format_string(copy.dest))
						#Set to running current
						self.ui.listStore[self.active_dir_copy][2] = COPY_STATUS_CODE[1]
			except Exception,e:
				print e
		if copy_done:
			self.ui.listStore[self.active_dir_copy][2] = COPY_STATUS_CODE[3]
		if copy_paused:
			self.ui.listStore[self.active_dir_copy][2] = COPY_STATUS_CODE[copy.status]
		#pb_single_file
		self.ui.pb_single_file.set_fraction(float(copy.percent)/100)
		#pb_all_files
		fraction = get_pb_all_files_values(copy.copied_size)
		self.ui.pb_all_files.set_fraction(float(fraction)/100)
		#Windows Title
		self.ui.rgcopy.set_title('Copy: %s (%s)-RGCopy' % (str(fraction)+'%',copy.speed_rate))
		#Progress Bar Labels
		self.ui.lbl_file_size.set_text('%s of %s' % (self.convert_bytes(self.partial_copies_size + copy.copied_size),
			self.convert_bytes(self.copies_size)))
		self.ui.lbl_single_file_eta.set_text(copy.ETA)
		self.ui.lbl_total_file_count.set_text('%s of %s' % (self.active_dir_copy+1,len(self.file_list)))
		self.ui.lbl_total_files_eta.set_text(get_total_eta(copy.speed_rate))
		#Launcher
		self.launcher.set_property("progress", float(fraction)/100)

		# file_size = '%s of %s' % (self.convert_bytes(self.partial_copies_size + copy.copied_size),
		#  	self.convert_bytes(self.copies_size))
		# self.ui.pb_single_file.set_text(build_progress_bar_text(file_size,copy.percent,copy.ETA))
		# file_count = '%s of %s' % (self.active_dir_copy+1,len(self.file_list))
		# self.ui.pb_all_files.set_text(build_progress_bar_text(file_count,fraction,get_total_eta(copy.speed_rate)))


	def format_string(self,string):
		return string if len(string) <= 55 else '...%s' % string[len(string)-55:]



