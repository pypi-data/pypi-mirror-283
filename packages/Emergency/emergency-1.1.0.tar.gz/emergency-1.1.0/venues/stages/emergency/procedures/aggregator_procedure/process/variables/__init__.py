

'''
	from emergency.procedures.aggregator_procedure.process.variables import retrieve_aggregator_variables
'''

'''
	from emergency.procedures.aggregator_procedure.process.variables import add_anomaly
	from emergency.topics.exceptions import parse_exception
	add_anomaly ({
		"anomaly": "",
		"exception": parse_exception (E)
	})
'''

from emergency.procedures.aggregator_procedure.process.moves.format_path import format_path
from emergency.topics.show.variable import show_variable

import json

'''
	paths_statuses = [{
		"path": path,
		** scan_status
	}]
'''

'''
	the_internal_statuses = {
		"status_2.py": {
			"status": {
				"scan": "pending",
				"process": "pending",
			},
			
			
			#
			#	"pending"
			#
			"scan status": "done",
						
			"records": [],
			"venture": process_on
		}
	}
'''
aggregator_variables = {
	"intro_harbor": {
		"host": "0.0.0.0",
		"port": ""
	},
	
	"records_level": 3,
	
	"intro_variables": {},
	
	#
	#	This is the list of statuses
	#
	#"paths_statuses": [],
	
	"details": 2,
	
	#
	#
	#
	"internal_statuses": {},
	"internal_statuses_built": "no",
	
	"proceeds": {},
	"proceeds_built": "no",
	
	"anomalies": []
}

def add_anomaly (anomaly):
	try:
		is_JSON = json.dumps (anomaly)
	
		aggregator_variables ["anomalies"].append (anomaly)
		
		show_variable ({
			"anomaly": anomaly
		})
		
	except Exception as E:
		show_variable ("An anomaly couldn't be added.")
		aggregator_variables ["anomalies"].append ("An anomaly couldn't be added.")
		
		print ("exception:", E)


def setup_internal_statuses (
	status_check_paths,
	relative_path
):
	for status_check_path in status_check_paths:		
		aggregator_variables ["internal_statuses"] [ 
			format_path (status_check_path, relative_path) 
		] = {
			"occurrences": {	
				#
				#	This indicates if the aggregator started the health scan process venture.
				#	The venture is the function that the process is started in.
				#
				#	
				#		options: [ "yes", "no" ]
				#
				"scan process venture started": "no",
				
				#
				#	This indicates if the aggregator started the health scan process.
				#	
				#		options: [ "yes", "no" ]
				#
				"scan process started": "no",
				
				#
				#	This indicates if the scan process notified the
				#	aggregator that it is on.
				#	
				#		options: [ "yes", "no" ]
				#
				"scan process notified aggregator": "no",
				
				#
				#	This indicates if the aggregator stopped the health scan process.
				#
				#		options: [ "yes", "no" ]
				#
				"scan process was stopped": "no",
				
				#
				#	This indicates if the aggregator stopped the health scan process.
				#
				#		options: [ "yes", "no", "unknown" ]
				#
				"scan process is alive": "unknown",
				
				#
				#	This indicates if the aggregator received 
				#	proceeds from the health scan process (by HTTP).
				#
				#		options: [ "yes", "no" ]
				#
				"scan proceeds were retrieved": "no",
				
				#
				#	This indicates if the aggregator 
				#	retrieved the "records" from the
				#	health scan process (by pexpect).
				#
				"scan records were retrieved": "no",
				
				
				#
				#	This is the reason why the process
				#	was indicated as "done"
				#
				"done reason give": ""
			},

			

			"status": {
				"process": "pending",
				
			},
			
			"times": {
				"started": "",
				"ended": "",
				"elapsed": "",
				"records retrieval": ""
			},
			
			"records": [],
			
			"process": None,
			"results_of_scan": None
		}
			
			
	return;

def change ():
	return;
	
def retrieve_variables ():
	return aggregator_variables;	

def retrieve_aggregator_variables ():
	return aggregator_variables;	
	
def retrieve ():
	return aggregator_variables;