#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 16:07:19 2016

@author: henry
"""

from flask import *
from faker import Faker
from livereload import Server
import sys

app = Flask(__name__)
fake = Faker()


@app.route("/")
def index():
    # return render_template(
    # return render_template(
    #     'index.jade',
    #     title="Welcom",
    #     header="Hello Jade",
    #     content=fake.text(1000))
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("username=%s, password=%s;" %
              (request.form['username'], request.form['password']))
        if request.form['password'] == 'test':
            session['username'] = request.form['username']
            return redirect(url_for('welcome'))
        else:
            return render_template('login.jade', error="Login failed")
    elif request.method == "GET":
        return render_template('login.jade')


@app.route("/logout")
def logout():
    del(session['username'])
    return redirect(url_for('login'))


@app.route('/home')
def welcome():
    if 'username' in session:
        return render_template('welcome.jade',
                               username=session['username'])
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
    app.debug = True
    app.secret_key = 'top$escrete999'
    # app.run()
    server = Server(app.wsgi_app)
    server.watch(sys.argv[0])
    server.serve(liveport=35729)
