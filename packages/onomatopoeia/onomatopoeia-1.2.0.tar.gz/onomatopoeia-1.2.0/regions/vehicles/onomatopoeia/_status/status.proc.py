




def add_paths_to_system (paths):
	import pathlib
	from os.path import dirname, join, normpath
	import sys
	
	this_folder = pathlib.Path (__file__).parent.resolve ()	
	for path in paths:
		sys.path.insert (0, normpath (join (this_folder, path)))

add_paths_to_system ([
	'../../../vehicles'
])


import json
import pathlib
from os.path import dirname, join, normpath
import sys

this_structure_name = "onomatopoeia"

this_folder = pathlib.Path (__file__).parent.resolve ()
regions = str (normpath (join (this_folder, "../../../../regions")))


vehicle_path = str (normpath (join (this_folder, "..")))


if (len (sys.argv) >= 2):
	glob_string = vehicle_path + '/' + sys.argv [1]
	db_directory = False
else:
	glob_string = vehicle_path + '/**/status_*.py'
	db_directory = normpath (join (this_folder, "DB"))

print ("glob string:", glob_string)

import biotech
scan = biotech.start (
	glob_string = glob_string,
	simultaneous = True,
	module_paths = [
		normpath (join (regions, "vehicles"))
	],
	relative_path = vehicle_path
)
