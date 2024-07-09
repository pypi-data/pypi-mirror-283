

'''
	objectives:
	
		[ ] /aggregator/records
		
		[ ] /health_scans/paths
		
		[ ] /health_scan/{ path }		
'''

#----
#
from .spaces.done_with_scan import done_with_scan
from .spaces.paths_patch import paths_patch
from .spaces.the_health_scan_started import the_health_scan_started
#
from emergency.procedures.aggregator_procedure.process.variables import retrieve_aggregator_variables
from emergency.procedures.aggregator_procedure.process.variables import add_anomaly
#
#
from flask import Flask, request, jsonify
import rich
#
#
import json
import pathlib
import os
from os.path import dirname, join, normpath
import sys
import threading
import time
#
#----

def open_harbor (
	port = 0,
	records = 0
):
	if (records >= 1):
		print ("opening scan process keg on port:", port)

	#app = Flask (__name__)
	#app = Flask ("implicit procedure harbor")
	app = Flask ("aggregator harbor")

	'''
		This is what starts the aggregator
	'''
	paths_patch (app, aggregator_procedure_port = port)

	@app.route ("/", methods = [ 'GET' ])
	def home_get ():	
		return jsonify ({
			'/data/health_scan/<path:health_scan_path>': [ "get" ],
			'/data/health_scans/paths': [ "get" ],
			'/on': [ "get" ],
			'/anomalies': [ "get" ]
		})


	@app.route ("/on", methods = [ 'GET' ])
	def on_get ():	
		return "yes"
		
	@app.route ("/data/proceeds", methods = [ 'GET' ])
	def on_data_proceeds ():	
		try:
			aggregator_variables = retrieve_aggregator_variables ()
			
			return jsonify ({
				"proceeds built": aggregator_variables ["proceeds_built"],
				"proceeds": aggregator_variables ["proceeds"]
			})			
			
		except Exception as E:
			print (E)
		
			pass;
	
		return "not parseable"	
		
	@app.route ("/data/anomalies", methods = [ 'GET' ])
	def on_anomalies ():	
		try:
			aggregator_variables = retrieve_aggregator_variables ()
			
			exception_count = 0
			parsed_anomalies = []
			unparsed_anomalies = aggregator_variables ["anomalies"]
			for anomaly in unparsed_anomalies:
				try:
					parsed_anomalies.append (json.dumps (unparsed_anomalies, indent = 4))
				except Exception as E:
					print ("anomaly parsing exception:", E)
					print ("anomaly parsing string exception:", str (E))
				
					exception_count += 1
			
			return jsonify ({
				"anomalies": aggregator_variables ["anomalies"],
				"exception_count": exception_count
			})
			
		except Exception as E:
			print (E)
			
		
			pass;
			
		return "not parseable"


	@app.route ("/data/waiting_for", methods = [ 'GET' ])
	def on_waiting_for ():	
		try:
			aggregator_variables = retrieve_aggregator_variables ()
			internal_statuses = aggregator_variables ["internal_statuses"]

			waiting_for = []
			for status_path in internal_statuses:
				occurrences = "not parseable"
				try:
					occurrences = aggregator_variables ["internal_statuses"] [ status_path ] ["occurrences"]
				except Exception:
					pass;
					
				records = "not parseable"
				try:
					records = aggregator_variables ["internal_statuses"] [ status_path ] ["records"]
				except Exception:
					pass;
					
				times = "not parseable"
				try:
					times = aggregator_variables ["internal_statuses"] [ status_path ] ["times"]
				except Exception:
					pass;
			
				if (internal_statuses [ status_path ] ["status"] ["process"] != "done"):
					waiting_for.append ({
						"path": status_path,
						"occurrences": occurrences,
						"records": records,
						"times": times
					})
			
			return jsonify ({
				"waiting_for": waiting_for
			})
			
		except Exception as E:
			print ("exception:", E)
			pass;
			
		return "not parseable"
	
	

	
	@app.route ('/data/health_scans/paths', methods = [ 'GET' ])
	def on__get__health_scans__paths ():	
		aggregator_variables = retrieve_aggregator_variables ()
		
		the_paths = {}
		
		for path in aggregator_variables ["internal_statuses"]:
			the_paths [ path ] = ""
	
		return jsonify (the_paths)
		
	@app.route ('/data/health_scan/<path:health_scan_path>', methods = [ 'GET' ])
	def on__get__health_scan__path (health_scan_path):	
		return "yes"
	
	
	the_health_scan_started (app)
	
	done_with_scan (app)
	
	

	app.run (
		'0.0.0.0',
		port = port,
		debug = False
	)