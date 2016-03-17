#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 16:07:19 2016

@author: henry
"""

from flask import Flask
from faker import Faker
from livereload import Server
import sys

app = Flask(__name__)
fake = Faker()
row = "<tr><td>{:s}</td><td>{:s}</td></tr>"

# @app.route("/")
# def hello():
#    return "<h1>Helo World!</h1>"


@app.route("/")
def students():
    html = "<h3>Student List</h3>"
    html += "<table>"
    for i in range(10):
        # row = "<tr><td>{:s}</td><td>{:s}</td></tr>"
        html += row.format(fake.first_name(), fake.last_name())
    html += "</table>"
    return html

if __name__ == "__main__":
    app.debug = True
    # app.run()
    server = Server(app.wsgi_app)
    server.watch(sys.argv[0])
    server.serve(liveport=35729)
