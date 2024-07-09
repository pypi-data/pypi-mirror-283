

'''
	import titaness.procedures.data_nodes.tiny as titaness_db
	records = titaness_db.records (
		db_directory = normpath (join (dynamics, f"status_db"))
	)
'''

'''
	import titaness.procedures.data_nodes.tiny as titaness_db
	last_record = titaness_db.last_record (
		db_directory = normpath (join (dynamics, f"status_db"))
	)
'''

from tinydb import TinyDB, Query
import pathlib
from os.path import dirname, join, normpath
	
def records (
	db_directory
):
	db_file = normpath (join (db_directory, f"records.json"))
	db = TinyDB (db_file)

	records = db.all ()
	db.close ()
	
	return list (records)
	
	
def last_record (
	db_directory
):
	db_file = normpath (join (db_directory, f"records.json"))
	db = TinyDB (db_file)

	records = db.all ()
	db.close ()
	
	records_list = list (records);
	
	return records_list [ len (records_list) - 1 ]