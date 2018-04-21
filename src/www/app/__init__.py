# -*- encoding: utf-8 -*-
'''
OER Commons - Initialization File
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
from flask import Flask

# Initialize Application
app = Flask(__name__, static_url_path='/static')

# Initialize Configuration
app.config.from_object('app.configuration.DevelopmentConfig')

# Import Modules
from app import views
