#!/usr/bin/env python3

# app/routes.py

from app import app

import csv, json, os, sys, time, datetime

from flask import Flask
from flask import render_template, request, make_response, jsonify

##### Define Constants ######
ucDateFormat = '%Y-%m-%d %H:%M:%S.%f' # date format from the microcontroller
#############################


@app.route('/')
@app.route('/index')
def route_Index():
	context = {}
	#context = {"performers": bandtools.getUniquePerformers("2019 Showband", videoConfig)}
	
	return render_template('home.jinja2', context=context)

@app.route('/postRangeData', methods=['POST'])
def route_postRangeData():
	"""
	Adds a ranging request, sent from a microcontroller-based (ESP8266) anchor node, to the database.

	Each ranging request represents a single ranging datapoint between a single anchor and a single tag at a given time.
	"""

	result = {"success": "true", "time_sec": time.time()}
	content = request.get_json()

	# For debugging only, copies the original request into the response
	result["request_copy"] = content

	# Store in the database

	# jsonify also sets the mimetype and other important web stuff
	return jsonify(result)