#!/usr/bin/env python3

# app/routes.py

from app import app, db

import csv, json, os, sys, time, datetime

from flask import Flask
from flask import render_template, request, make_response, jsonify, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError

from app.models import RangingRequest, AnchorSettings
from app.forms import AddAnchorForm

##### Define Constants ######
ucDateFormat = '%Y-%m-%d %H:%M:%S.%f' # date format from the microcontroller
#############################

# Helper Function
def flash_errors(form):
	for field, errors in form.errors.items():
		for error in errors:
			flash(u"Error in the %s field - %s" % (
				getattr(form, field).label.text,
				error
			), 'info')


@app.route('/')
@app.route('/index')
def route_index():
	context = {}
	#context = {"performers": bandtools.getUniquePerformers("2019 Showband", videoConfig)}
	
	return render_template('home.jinja2', context=context)

@app.route('/postRangeData', methods=['POST'])
def route_postRangeData():
	"""
	Adds a ranging request, sent from a microcontroller-based (ESP8266) anchor node, to the database.

	Each ranging request represents a single ranging datapoint between a single anchor and a single tag at a given time.
	"""

	result = {"success": "true", "time_sec": time.time(), "successAddCount": 0}
	content = request.get_json()

	# For debugging only, copies the original request into the response
	result["request_copy"] = content

	for thisRangeRequest in content.get("BufferArray", []):
		thisRangeRequest["AnchorNumber"] = content.get("AnchorNumber")
		thisRangeRequest["AccountNumber"] = content.get("AccountNumber")
		thisRangeRequest["RangeDate"] = datetime.datetime.strptime(thisRangeRequest.get("Date", ""), ucDateFormat)
		thisRangeRequest["TransmitDate"] = datetime.datetime.strptime(content.get("Date", ""), ucDateFormat)

		# Store in the database
		try:
			newRangingRequest = RangingRequest(thisRangeRequest)
			db.session.add(newRangingRequest)
			result["successAddCount"] += 1
		except IntegrityError:
			db.session.rollback()

	db.session.commit()

	# jsonify also sets the mimetype and other important web stuff
	return jsonify(result)

@app.route('/anchors')
def route_anchors():
	"""
	Shows existings anchors, with options to add and delete anchors
	"""

	context = {}
	addForm = AddAnchorForm(request.form)
	context["anchors"] = AnchorSettings.query.order_by(AnchorSettings.anchorNumber).all()

	return render_template('anchors.jinja2', context=context, addForm=addForm)

@app.route('/anchors/add', methods=['POST'])
def route_addAnchor():

	context = {}
	form = AddAnchorForm(request.form)

	if request.method == 'POST':
		if form.validate_on_submit():
			newAnchor = AnchorSettings(form.anchorNumber.data, form.enabled.data, (form.anchorCoordX.data, form.anchorCoordY.data), (form.anchorCoordXSteps.data, form.anchorCoordYSteps.data))
			try:
				db.session.add(newAnchor)
				db.session.commit()
				flash('New Anchor, #{}, added!'.format(newAnchor.anchorNumber), 'success')
			except IntegrityError as e:
				flash("Error. Ensure a unique Anchor Number was selected.", 'error')
				print(e)

		else:
			flash_errors(form)
			flash('Error! Anchor was not added. Invalid field options in fields.', 'error')


	return redirect(url_for('route_anchors'))

@app.route('/anchors/<int:id>/remove')
@app.route('/anchors/<int:id>/delete')
def route_removeAnchor(id):
	"""
	Removes an anchor by its ID, not by its anchorNumber.

	Note: this doesn't use forms, may be vulnerable to CRSF attack (?).
	"""

	db.session.delete(AnchorSettings.query.filter_by(id=id).first())
	db.session.commit()

	return redirect(url_for('route_anchors'))

