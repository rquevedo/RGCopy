#! /usr/bin/python
# -*- coding: utf8 -*-

import os, sys
KEYS = ("NAUTILUS_SCRIPT_SELECTED_FILE_PATHS",
"NAUTILUS_SCRIPT_SELECTED_URIS", "NAUTILUS_SCRIPT_CURRENT_URI",
"NAUTILUS_SCRIPT_WINDOW_GEOMETRY")

ft = open("/home/reisy/some.txt", "w")
for key_value in [(key, os.environ.get(key, 'NOT FOUND')) for key in KEYS]:
	ft.write("env(%s): %s\n" % key_value)
# file_names=sys.argv[1:]
# for index, file_name in enumerate(file_names):
# ft.write("%s: [%s]\n" % (index, file_name))
# if os.path.isfile(file_name): os.rename(file_name, '%03d-%s' %
# (index+1, file_name))
ft.close()
