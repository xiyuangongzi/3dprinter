#-*- coding: UTF-8 -*-
#import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash,send_from_directory
from contextlib import closing
from werkzeug import secure_filename
from flask_saestorage import SaeStorage

DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
UPLOAD_FOLDER = 'templates'
ALLOWED_EXTENSIONS = set(['txt','gcode', 'html'])
SAE_BUCKET_NAME = 'zhaoyong'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sae_storage = SaeStorage(app)

#app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#def connect_db():
#    return sqlite3.connect(app.config['DATABASE'])

#def init_db():
#    with closing(connect_db()) as db:
#        with app.open_resource('schema.sql') as f:
#            db.cursor().executescript(f.read())
#            db.commit()

#@app.before_request
#def before_request():
#    g.db = connect_db()

#@app.teardown_request
#def teardown_request(exception):
#    g.db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def printd():
    #return redirect(sae_storage.url('abc.gcode'))
    return sae_storage.url('abc.gcode')

@app.route('/delete',methods=['GET'])
def delete():
    sae_storage.delete('abc.gcode')
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/printer')
def add_gcode():
    if not session.get('logged_in'):
        return "<h2>please login</h2>"
    return render_template('printer.html')

@app.route('/show',methods=['GET', 'POST'])
def show_module():
    if request.method == 'POST':
        file = request.files['file']
        if file :
            filename = 'abc.gcode'
            sae_storage.save(file, filename)
            return render_template('printer.html')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid password'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('index.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run()
