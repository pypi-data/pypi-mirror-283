

from emergency.procedures.aggregator_procedure.process.variables import retrieve_variables
from emergency.procedures.aggregator_procedure.process.variables import add_anomaly
from ...done_with_scan import done_with_scan_move

from emergency.topics.exceptions import parse_exception

import time

def learn_if_global_time_limit_was_exceeded (status_path):
	try:
		aggregator_variables = retrieve_variables ()
		time_limit = aggregator_variables ["intro_variables"] ["time_limit"]
		internal_statuses = aggregator_variables ["internal_statuses"]
		
		status_of_path = internal_statuses [ status_path ]
		occurrences = status_of_path ["occurrences"]
	
		'''
		if (
			occurrences ["scan process started"] == "yes" and
			occurrences ["scan process is alive"] == "yes" and
			occurrences ["scan process notified aggregator"] == "yes" and
			occurrences ["scan process was stopped"] == "no" and
			len (internal_statuses [ status_path ] ["times"] ["started"]) >= 1
		):	
		'''
		
		started_at = internal_statuses [ status_path ] ["times"] ["started"]
		
		if (len (started_at) >= 1):
			if (time.time () - float (started_at) >= float (time_limit)):	
				try:
					the_scan_records = internal_statuses [ status_path ] ["records"]
				except Exception:
					the_scan_records = "not found"
			
				done_with_scan_move ({
					"path": status_path,
					"result":{
						"alarm": "time limit exceeded",
						"the records": the_scan_records
					}
				})
						
	except Exception as E1:
		add_anomaly ({
			"anomaly": "physical: time limit check exception",
			"status_path": status_path,
			"exception": parse_exception (E1)
		})

			
			
		
	
		
