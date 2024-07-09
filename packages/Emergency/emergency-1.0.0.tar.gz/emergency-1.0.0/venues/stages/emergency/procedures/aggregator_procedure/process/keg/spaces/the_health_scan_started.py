


#----
#
from emergency.topics.show.variable import show_variable
from emergency.procedures.aggregator_procedure.process.variables import aggregator_variables
#
#
from flask import Flask, request
import rich
#
#
import json
#
#----

def the_health_scan_started (app):
	@app.route ("/the_health_scan_started", methods = [ 'PATCH' ])
	def patch__the_health_scan_started ():
		show_variable ("received /the_health_scan_started", mode = "condensed")
	
		the_packet = json.loads (request.data.decode ('utf8'))
		the_path = the_packet ["path"]
		
		show_variable ("parsed packet from /the_health_scan_started", mode = "condensed")
		
		aggregator_variables ["internal_statuses"] [ the_path ] ["occurrences"] ["scan process notified aggregator"] = "yes"

	
		return "received"

