#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# main.py

import os
directory = os.path.dirname(os.path.realpath(__file__))

import imp
import gi
#gi.require_version('Gtk', '3.0')
#gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk , Gdk , GObject, AppIndicator3, Unity
from commons.copy import Copy, COPY_STATUS_CODE
from gui.gui import Interface as ui
import gettext , locale
import urllib, urlparse
import datetime



STATUS_CODE = {0:'running', 1:'paused'}
SHOW_HIDE_TEXT = {True:'Less', False:'More'}
CONVERSION_RATE = {'b/s':1, 'kB/s':1024, 'MB/s':1048576, 'GB/s':1073741824}


class Handler():

	def __init__(self, main):
		self.main = main


 	def on_btn_more_clicked(self, *args):
 		self.main.ui.scrolledwindow1.set_visible(not self.main.ui.scrolledwindow1.get_visible())
 		self.main.ui.btn_more.set_label(SHOW_HIDE_TEXT[self.main.ui.scrolledwindow1.get_visible()])

 	def on_btn_close_clicked(self, button):
 		self.main.copies[self.main.active_copy].process.kill()
		Gtk.main_quit()

	def on_btn_pause_clicked(self, button):
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
		self.lines, self.action = [], 'not_set'#self.get_lines_list()
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
				
				copy = Copy(line, copy_path, self, self.action)
				copy_size = copy.get_size()
				self.copies_size += copy_size
				file_name = os.path.basename(line)
				parent_dir = os.path.dirname(line)
				self.file_list.append((parent_dir, file_name, copy_size))
			
			else:				
				copy = Copy(line, copy_path, self, self.action, True)
				paths = []
				files_dic = {}
				for path, dirs, files in os.walk(line):
					paths.append(path)
					files_dic[path] = files
				paths.sort()
				for path in paths:
					files = files_dic[path]
					if files:
						files.sort()
						for fl in files:
							full_path = os.path.join(path, fl)
							copy_size = os.path.getsize(full_path)#/1024.0
							self.copies_size += copy_size
							self.file_list.append((path, fl, copy_size))
			cps.append(copy)
		self.set_treview_model()
		return cps

# 		import os
# statvfs = os.statvfs('/home/foo/bar/baz')

# statvfs.frsize * statvfs.f_blocks     # Size of filesystem in bytes
# statvfs.frsize * statvfs.f_bfree      # Actual number of free bytes
# statvfs.frsize * statvfs.f_bavail 
	def get_clipboard_content(self):

		cb = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
		atom = Gdk.Atom.intern('x-special/gnome-copied-files', False)
		content = cb.wait_for_contents(atom)
		content_data = content.get_data()
		content_data = str(content_data)
		if content_data:
			split_data = content_data.split('\n')
			value1 = split_data[0]
			value2 = split_data[1:]
			return value1, value2
		else:
			return None, []

	def get_lines_list(self):
		lts = []
		action, lines = self.get_clipboard_content()
		for line in lines:
			if line.startswith('file://'):
				url = line.split('file://')[1]
				line = urllib.url2pathname(url)
			elif line.startswith('smb://'):
				url = line.split('smb://')[1]
				path_array = url.split('/')
				server_name = path_array[0]
				share_name = path_array[1]
				file_path = '/'.join(path_array[2:])
				user = get_login_user()
				line = urllib.url2pathname('/run/user/%s/gvfs/smb-share:server=%s,share=%s/%s' % (user,server_name,share_name,file_path))
			elif line.startswith('sftp://'):
				url = line.split('sftp://')[1]
				path_array = url.split('/')
				server_name = path_array[0]
				file_path = '/'.join(path_array[1:])
				user = get_login_user()
				split_server_name = server_name.split('@')
				if len(split_server_name) != 1:
					user_name = split_server_name[0]
					server_name = split_server_name[1]
					line = urllib.url2pathname('/run/user/%s/gvfs/sftp:host=%s,user=%s/%s' % (user,server_name,user_name,file_path))
				else:
					line = urllib.url2pathname('/run/user/%s/gvfs/sftp:host=%s/%s' % (user,server_name,file_path))


			if os.path.exists(line):
				lts.append(line)
		return lts, action

	def convert_bytes(self, bytes):
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
			self.ui.listStore.append([fl[1], self.convert_bytes(fl[2]), COPY_STATUS_CODE[0], fl[0]])

	def get_copy_path(self):

		try:
			dir_to_open = ""
			selected = os.environ["NAUTILUS_SCRIPT_SELECTED_URIS"].split("\n")[:-1]
			#Note getting SELECTED_URIS rather than SELECTED_FILE_PATHS as later
			#is not set when ~/Desktop and ~/.Trash selected??
			if len(selected) == 1:
			    uri_bits = urlparse.urlparse(urllib.unquote(selected[0]))
			    if uri_bits[0] == "file":
			        dir_to_open = uri_bits[2]
			    elif uri_bits[0] == "x-nautilus-desktop":
			        if uri_bits[2] == "///trash":
			            dir_to_open = home_dir + '/.Trash'
			        elif uri_bits[2] == "///home":
			            dir_to_open = home_dir + '/Desktop'
			    if not os.path.isdir(dir_to_open):
			        dir_to_open = ""
			if not dir_to_open: #we didn't select 1 directory so open current dir
			    current_uri = os.environ["NAUTILUS_SCRIPT_CURRENT_URI"]
			    uri_bits = urlparse.urlparse(urllib.unquote(current_uri))
			    if uri_bits[0] == "file":
			        dir_to_open = uri_bits[2]
			    elif uri_bits[0] == "x-nautilus-desktop":
			        dir_to_open = home_dir + '/Desktop'
			    elif uri_bits[0] == "trash":
			        dir_to_open = home_dir + '/.Trash'
		except Exception, e:
			return home_dir
		#return '/home/reisy/Escritorio/RGCopy_prueba'
		return dir_to_open
        

	def show(self):

		def maximize(attr1, attr2):
			self.ui.rgcopy.present()

		APPNAME = "RGCopy"
		ICON = '/opt/RGCopy/icons/32x32/stallion.png'
		
		self.ai = AppIndicator3.Indicator.new(APPNAME, ICON, AppIndicator3.IndicatorCategory.APPLICATION_STATUS)		
		self.ai.set_menu(self.ui.tray_menu)

		#self.ai.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
		self.launcher = Unity.LauncherEntry.get_for_desktop_id ("RGCopy.desktop")

		self.ui.rgcopy.set_title('RGCopy')
		self.ui.rgcopy.show_all()
		self.initialize()
		#GObject.threads_init()
		Gtk.main()

	def on_show_copy_activate(self):
		self.ui.rgcopy.set_visible(True)
		self.ui.rgcopy.show_all()

	def run_process(self):
		self.copies = self.get_copies_list()
		GObject.idle_add(self.manage_copies)

	def manage_copies(self):
		if self.status == 1:
			return False
		if self.active_copy is not None:
			if self.copies[self.active_copy].process.done():
				self.copies[self.active_copy].process.update_copy({'percent':100, 'copied_size':self.file_list[self.active_dir_copy][2]})
				self.update_ui()
				self.copies[self.active_copy].status = 3
				if len(self.copies) == (self.active_copy + 1):
					self.update_ui(True)
					Gtk.main_quit()
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
			return True

	def update_ui(self, copy_done=None, file_list=None, copy_paused=False):

		def get_pb_all_files_values(updated_value):
			if self.copies_size != 0:
				return int(((self.partial_copies_size + updated_value) * 100.0) / self.copies_size)
			return 1

		def convert_to_bytes(rate):
			if rate:
				mu = rate[-4:]
				value = rate[:-4]
				return float(value) * CONVERSION_RATE[mu]
			return None



		def get_total_eta(rate):
			b_p_s = convert_to_bytes(rate)
			if b_p_s:
				left = self.copies_size - (self.partial_copies_size + copy.copied_size)
				seconds = left / b_p_s
				eta = str(datetime.timedelta(seconds=round(seconds)))
				return eta
			return '--:--:--'

		copy = self.copies[self.active_copy]
		
		if file_list:
			try:
				for fl in file_list:

					self.active_dir_copy += 1
					if self.active_dir_copy > 0:
						
						#Adding file size to partial list
						self.partial_copies_size += self.file_list[self.active_dir_copy - 1][2]
						
						#Set to copied last file and set to running current
						self.ui.listStore[self.active_dir_copy - 1][2] = COPY_STATUS_CODE[3]
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
			except Exception, e:
				pass
		if copy_done:
			self.ui.listStore[self.active_dir_copy][2] = COPY_STATUS_CODE[3]
		if copy_paused:
			self.ui.listStore[self.active_dir_copy][2] = COPY_STATUS_CODE[copy.status]
		#pb_single_file
		self.ui.pb_single_file.set_fraction(float(copy.percent) / 100)
		#pb_all_files
		fraction = get_pb_all_files_values(copy.copied_size)
		self.ui.pb_all_files.set_fraction(float(fraction) / 100)
		#Windows Title
		self.ui.rgcopy.set_title('Copy: %s (%s)-RGCopy' % (str(fraction) + '%', copy.speed_rate))
		#Progress Bar Labels
		self.ui.lbl_file_size.set_text('%s of %s' % (self.convert_bytes(self.partial_copies_size + copy.copied_size),
			self.convert_bytes(self.copies_size)))
		self.ui.lbl_single_file_eta.set_text(copy.ETA)
		self.ui.lbl_total_file_count.set_text('%s of %s' % (self.active_dir_copy + 1, len(self.file_list)))
		self.ui.lbl_total_files_eta.set_text(get_total_eta(copy.speed_rate))



	def format_string(self, string):
		return string if len(string) <= 55 else '...%s' % string[len(string) - 55:]



if __name__ == '__main__': 
	main = RGCopy()
	main.show()