#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from datetime import datetime



app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/paradise'

# create mongodb client
client = MongoClient('127.0.0.1', 27017)
# create mongodb database
mdb = client.spirit

db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category(name=%s)>' % self.name

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    content = db.Column(db.Text)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('files', lazy='dynamic'))

    def __init__(self, title, category, content, created_time=None):
        self.title = title
        self.category = category
        self.content = content
        if created_time is None:
            created_time = datetime.now()
        self.created_time = created_time

    def __repr__(self):
        return '<File(title=%s)>' % self.title

    def add_tag(self, tag_name):
        if not mdb.tag.find_one({'file_id':self.id, 'tag':tag_name}):
            mdb.tag.insert_one({'file_id': self.id, 'tag': tag_name})

    def remove_tag(self, tag_name):
        mdb.tag.delete({'file_id': self.id, 'tag': tag_name})

    @property
    def tags(self):
        taglist = []
        for item in mdb.tag.find({'file_id': self.id}, {'tag': 1, '_id': 0}):
            taglist.append(item)
        return taglist


@app.route('/')
def index():
    files= db.session.query(File).all()
    return render_template('index.html',files=files)


@app.route('/files/<file_id>')
def file(file_id):
    fileobject = db.session.query(File).filter(File.id == int(file_id)).first()
    if not fileobject:
        abort(404)
    return render_template('file.html',fileobject=fileobject)

@app.errorhandler(404)
def nothing(error):
    return render_template('404.html'),404
