# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

from flask import render_template, request, redirect
# from flask.ext.login import login_user, logout_user, current_user, login_required
# from forms import ExampleForm, LoginForm
# from models import User
from app import app

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/query')
def query_result():
	# Extract Query from GET
	query = request.args.get('q')

	# Redirect if Empty Query
	if query is None or len(query) == 0: return redirect('/')

	return render_template('result.html', q=query)
