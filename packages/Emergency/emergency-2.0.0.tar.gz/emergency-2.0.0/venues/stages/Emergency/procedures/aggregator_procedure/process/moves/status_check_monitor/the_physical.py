




#----
#
from Emergency.procedures.aggregator_procedure.process.variables import retrieve_variables
from Emergency.procedures.aggregator_procedure.process.variables import add_anomaly
from Emergency.topics.exceptions import parse_exception
#
from .records import attach_records
#
from .alarm_checks.global_time_limit_exceeded import learn_if_global_time_limit_was_exceeded
#
from Emergency.topics.process_on.p_expect.parse_records import parse_p_expect_records
from Emergency.topics.show.variable import show_variable
#
#
from pprint import pprint
import time
import traceback
#
#
import rich
#
#----


'''
	This is run over and over again
	in a loop.
'''
def parse_and_check_is_alive_of_statuses ():
	aggregator_variables = retrieve_variables ()

	records_level = aggregator_variables ["records_level"]
	internal_statuses = aggregator_variables ["internal_statuses"]
	time_limit = aggregator_variables ["intro_variables"] ["time_limit"]

	statuses = {}
	unfinished = []
	for status_path in internal_statuses:
		
		status_of_path = internal_statuses [ status_path ]
		occurrences = status_of_path ["occurrences"]
		
		'''
			This checks if the pexpect 
			process is alive.
		'''
		try:
			if ("process" in internal_statuses [ status_path ]):
				if (
					type (internal_statuses [ status_path ] ["process"]) == dict and
					"process" in internal_statuses [ status_path ] ["process"]
				):
					occurrences ["scan process is alive"] = internal_statuses [ status_path ] ["process"] ["is_going"] ()
				
				'''
				if (
					type (internal_statuses [ status_path ] ["process"]) == dict and
					"process" in internal_statuses [ status_path ] ["process"]
				):
					if (type (internal_statuses [ status_path ] ["process"] ["process"]) != None):
						alive = internal_statuses [ status_path ] ["process"] ["process"].is_alive ()
						if (alive == True):
							occurrences ["scan process is alive"] = "yes"
						else:
							occurrences ["scan process is alive"] = "no"
				'''
				
		except Exception as E:
			add_anomaly ({
				"anomaly": "physical: process alive check exception",
				"status_path": status_path,
				"exception": parse_exception (E)
			})
		
			occurrences ["scan process is alive"] = "unknown"		
		
		
		attach_records (status_path)
		
		learn_if_global_time_limit_was_exceeded (status_path)
		


		
		'''
			This checks if a perhaps non started process didn't 
			notify the aggregator within 30 seconds.
		
			The before process line was reached:
				scan process venture started == "yes"
			
			The after process line was not reached:
				scan process venture started == "no"
		
			30 seconds elapsed
		'''
		try:
			if (
				occurrences ["scan process venture started"] == "yes" and
				occurrences ["scan process started"] == "no" and
				occurrences ["scan process notified aggregator"] == "no"
			):
				elapsed = time.time () - float (internal_statuses [ status_path ] ["times"] ["venture started"]);
				
				if (elapsed >= 30):		
					try:
						occurrences = internal_statuses [ status_path ] ["occurences"];
					except Exception:
						occurrences = "not found"				
				
					aggregator_variables ["internal_statuses"] [ status_path ] ["results_of_scan"] = {
						"path": status_path,
						
						"alarm": "After 30 seconds, the after process line was not reached and the process did not notify the aggregator.",
						"alarm notes": [],
						
						"occurrences": occurrences,
						
						"exited": True
					}
				
					aggregator_variables ["internal_statuses"] [ status_path ] ["status"] ["process"] = "done"
					aggregator_variables ["internal_statuses"] [ status_path ] ["occurrences"] ["done reason give"] = "The process didn't notify the aggregator within 5 seconds."
					
					aggregator_variables ["internal_statuses"] [ status_path ] ["process"] ["process"].terminate ()
					

		except Exception as E:
			add_anomaly ({
				"anomaly": "physical: process proceed no start check exception",
				"status_path": status_path,
				"exception": parse_exception (E)
			})
		
			pass;
			
		
		'''
			objective:
				The scan process was stopped, 
				but 10 seconds have passed
				and the proceeds were not retrieved.
		'''
		try:
			if (
				occurrences ["scan process was stopped"] == "yes" and
				occurrences ["scan proceeds were retrieved"] == "no"
			):
				elapsed = time.time () - float (internal_statuses [ status_path ] ["times"] ["venture started"]);
				
				if (elapsed >= 15):	
					aggregator_variables ["internal_statuses"] [ status_path ] ["results_of_scan"] = {
						"path": status_path,
						
						"alarm": "The scan process was stopped, but 15 seconds have passed and the proceeds were not retrieved.",
						"alarm notes": [],
						
						"occurrences": occurrences
					}
				
					aggregator_variables ["internal_statuses"] [ status_path ] ["status"] ["process"] = "done"

		except Exception as E:
			add_anomaly ({
				"anomaly": "physical: process proceed not retrieved check exception",
				"status_path": status_path,
				"exception": parse_exception (E)
			})
			
			pass;
		
		
		'''
			This checks if a started process didn't 
			notify the aggregator within 20 seconds.
		
				scan process started == "yes"
				scan process notified aggregator == "no"
				10 seconds elapsed
		'''
		try:
			if (
				occurrences ["scan process started"] == "yes" and
				occurrences ["scan process notified aggregator"] == "no"
			):
				elapsed = time.time () - float (internal_statuses [ status_path ] ["times"] ["venture started"]);
				
				if (elapsed >= 20):			
					try:
						occurrences = internal_statuses [ status_path ] ["occurences"];
					except Exception:
						occurrences = "not found"
					
					aggregator_variables ["internal_statuses"] [ status_path ] ["results_of_scan"] = {
						"path": status_path,
						
						"alarm": "After 20 seconds, the process did not notify the aggregator that it had started.",
						"alarm notes": [],
						
						"occurrences": occurrences,
						
						"exited": True
					}
				
					aggregator_variables ["internal_statuses"] [ status_path ] ["status"] ["process"] = "done"
					aggregator_variables ["internal_statuses"] [ status_path ] ["occurrences"] ["done reason give"] = "The process didn't notify the aggregator within 5 seconds."
					aggregator_variables ["internal_statuses"] [ status_path ] ["process"] ["process"].terminate ()
					
					show_variable ({
						"process may have stopped": status_path
					})
		except Exception as E:
			add_anomaly ({
				"anomaly": "physical: process proceed no notification check exception",
				"status_path": status_path,
				"exception": parse_exception (E)
			})
		
			pass;
		
		
		
		
		
		
		'''
			Alarm Possibility: 
				"The process exited before results could be sent."
		
			Description:
				This indicates the process is done,
				if while reading the path an exit occurred.
				
					examples:
						1 / 0
						exit ()
		'''
		try:
			if (
				occurrences ["scan process started"] == "yes" and		
				occurrences ["scan process notified aggregator"] == "yes" and

				occurrences ["scan process was stopped"] == "no" and

				occurrences ["scan process is alive"] != "yes"				
			):		
				aggregator_variables ["internal_statuses"] [ status_path ] ["results_of_scan"] = {
					"path": status_path,
					
					"alarm": "The process exited before results could be sent.",
					"alarm notes": [],
					"occurrences": occurrences,
					
					"exited": True
				}
			
				aggregator_variables ["internal_statuses"] [ status_path ] ["status"] ["process"] = "done"

		except Exception as E:
			add_anomaly ({
				"anomaly": "physical: process parse and check exception",
				"status_path": status_path,
				"exception": parse_exception (E)
			})
			
			pass;
		
		
		'''
			objective:
				This stops the process if:
					the process is alive, but unresponsive?
		'''
		

		
		'''
			This indicate that the process is done normally
		'''
		try:
			if (
				occurrences ["scan process is alive"] == "no" and

				occurrences ["scan process started"] == "yes" and
				occurrences ["scan process was stopped"] == "yes" and
				
				occurrences ["scan records were retrieved"] == "yes"
			):				
				aggregator_variables ["internal_statuses"] [ status_path ] ["status"] ["process"] = "done"

		except Exception as E:
			add_anomaly ({
				"anomaly": "physical: process is done normally check exception",
				"status_path": status_path,
				"exception": parse_exception (E)
			})
			pass;
		

	
	for status_path in internal_statuses:
		if (internal_statuses [ status_path ] ["status"] ["process"] != "done"):
			unfinished.append ({
				"path": status_path,
				"internals": aggregator_variables ["internal_statuses"] [ status_path ]
			})
	
		
	return unfinished

