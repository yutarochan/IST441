# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""
from flask import render_template, request, redirect
import time
from app import app
from app import oer

# Application Parameters
MODEL_ROOT = 'app/model/'
MODEL_DIR = MODEL_ROOT + 'oer_.pickle'

SIM_THRESH = 0.25

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/query')
def query_result():
	# Extract Query from GET
	text = request.args.get('q')
	
	# Redirect if Empty Query
	if text is None or len(text) == 0: return redirect('/')

	# Perform Search Query
	start = time.time() 
	result = oer.query(text, 109650, SIM_THRESH)
	end = time.time()

	# Compute Query Walltime
	walltime = end - start

	return render_template('result.html', q=text, res=result, w_time=walltime, count=len(result))
