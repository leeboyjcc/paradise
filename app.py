#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask,render_template
import os
import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

dirpath = '/home/shiyanlou/files/'
@app.route('/')
def index():
    titlelist = []
    for item in os.listdir(dirpath):
        with open(dirpath+item,'r') as f:
            filedict = json.load(f)
            titlelist.append(filedict['title'])
    return render_template('index.html',titlelist=titlelist)


@app.route('/files/<filename>')
def file(filename):
    filepath = dirpath+filename+'.json'
    if not os.path.exists(filepath):
        abort(404)
    with open(filepath,'r') as f:
        filecontent = json.load(f)
    return render_template('file.html',filecontent=filecontent)

@app.errorhandler(404)
def nothing(error):
    return render_template('404.html'),404
