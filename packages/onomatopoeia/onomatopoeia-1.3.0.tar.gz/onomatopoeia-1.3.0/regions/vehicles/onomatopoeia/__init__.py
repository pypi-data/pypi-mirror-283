

'''
	import onomatopoeia

	import pathlib
	from os.path import dirname, join, normpath
	this_dir = str (pathlib.Path (__file__).parent.resolve ())
	onomatopoeia_harbor.start ({
		"directory": this_dir,
		"relative path": this_dir
	});

	onomatopoeia_harbor.server.stop ()
'''

print ("__name__", __name__)

from onomatopoeia._clique import clique

from onomatopoeia.moves.start import start
