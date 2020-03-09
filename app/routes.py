#!/usr/bin/env python3

# app/routes.py

from app import app

import csv, json, os, sys, time

from flask import Flask
from flask import render_template, request, make_response

@app.route('/')
@app.route('/index')
def routeIndex():
	context = {}
	#context = {"performers": bandtools.getUniquePerformers("2019 Showband", videoConfig)}
	
	return render_template('home.jinja2', context=context)