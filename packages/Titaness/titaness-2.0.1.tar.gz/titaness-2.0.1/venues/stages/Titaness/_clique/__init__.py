

#print ('Titaness')

#
#
import Titaness
import Titaness.topics.help_documentation as help_documentation
import Titaness._status.establish as establish_status
#
#
import click	
#
#
import pathlib
import time
from os.path import dirname, join, normpath
import os
#
#

def the_help_procedure (
	port = ""
):
	this_directory = pathlib.Path (__file__).parent.resolve ()
	this_module = str (normpath (join (this_directory, "..")))

	print ("port:", port)

	help_documentation.start ({
		"directory": this_module,
		"extension": ".s.HTML",
		"relative path": this_module,
		
		"port": int (port)
	})
	
	while True:
		time.sleep (1)

def clique ():
	@click.group ()
	def group ():
		pass
		
	@click.command ("help")
	@click.option ('--port', default = "20000")
	def command_help (port):
		the_help_procedure (port)
	group.add_command (command_help)
		
	@click.command ("internal-health")
	@click.option ('--glob-string', default = "")
	def command_internal_health (glob_string):
		if (len (glob_string) >= 1):
			this_folder = pathlib.Path (__file__).parent.resolve ()

			structures = normpath (join (this_folder, "../../.."))
			monitors = str (normpath (join (this_folder, "..")))
	
			glob_string = monitors + "/" + glob_string
	
		establish_status.start (
			glob_string = glob_string
		)
	group.add_command (command_internal_health)
	

	@click.command ("health")
	@click.option ('--simultaneous', default = "yes")
	@click.option ('--glob-string', default = "/**/status_*.py")
	def command_health (simultaneous, glob_string):
		this_directory = pathlib.Path (__file__).parent.resolve ()
		this_module = str (normpath (join (this_directory, "..")))

		CWD = os.getcwd ()
		
		if (simultaneous == "yes"):
			simultaneous_bool = True
		elif (simultaneous == "no"):
			simultaneous_bool = False
		else:
			print ("'--simultaneous yes' or '--simultaneous no'")
			exit ()
			
		Titaness.start (
			glob_string = CWD + glob_string,
			simultaneous = simultaneous
		)
	group.add_command (command_health)

	group ()




#
