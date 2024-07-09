
'''
	python3 /titaness/venues/stages/titaness/_status/status.proc.py "_status/monitors/10_time_limits/status_1.py"
'''

import pathlib
from os.path import dirname, join, normpath
import titaness

import time

def check_1 ():

	
	this_directory = pathlib.Path (__file__).parent.resolve ()
	this_module = str (this_directory)
	the_guarantees = str (normpath (join (this_directory, f"guarantees")))
	

	
	bio = titaness.on ({
		"glob_string": this_module + "/**/guarantee_*.py",
		
		"time_limit": 5,
		
		"simultaneous": True,
		"simultaneous_capacity": 10,

		"module_paths": [
			normpath (join (this_module, "modules")),
			normpath (join (this_module, "modules_pip"))
		],

		"relative_path": this_module,
		
		"aggregation_format": 2
	})
	
	bio ["off"] ()
	scan = bio ["proceeds"]
	
	assert (scan ["paths"] [0] ["alarm"] == "time limit exceeded"), scan ["paths"]

	assert (scan ["stats"] ["paths"] ["alarms"] == 1), scan ["stats"]
	assert (scan ["stats"] ["paths"] ["empty"] == 0), scan ["stats"]

	assert (scan ["stats"] ["checks"] ["passes"] == 0), scan ["stats"]
	assert (scan ["stats"] ["checks"] ["alarms"] == 0), scan ["stats"]
	
checks = {
	'aggregation format and exit': check_1
}
