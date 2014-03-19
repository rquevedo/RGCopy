import os
directory = os.path.dirname(os.path.realpath(__file__))
from gi.repository import Gtk


class Interface():

	def __init__(self):

		self.builder = Gtk.Builder()
		self.builder.add_from_file(os.path.join(directory,'rgcopy.glade'))
		self.build_treeview()

	def __getattr__(self, name):
		return self.builder.get_object(name)


	def build_treeview(self):


		def column(name,cell,attribute,value,width):		
			column = Gtk.TreeViewColumn(name)
			column.pack_start(cell, False)
			column.add_attribute(cell, attribute, value)
			
			#column.set_fixed_width(width)
			column.set_sizing(Gtk.TreeViewColumnSizing.FIXED)
			column.set_min_width(width)
			column.set_resizable(True)
			return column

		listStore = Gtk.ListStore(str,str,str)
		self.listStore = listStore		
		self.file_list.set_model(self.listStore)

		self.file_list.append_column(column('File',Gtk.CellRendererText(),"text",0,335))
		self.file_list.append_column(column('Size',Gtk.CellRendererText(),"text",1,75))
		self.file_list.append_column(column('Status',Gtk.CellRendererText(),"text",2,60))
