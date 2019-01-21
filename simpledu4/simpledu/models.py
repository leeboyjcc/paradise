from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for

db = SQLAlchemy()

class Base(db.Model):
    """所有model的一个基类，默认添加了时间戳"""
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_STAFF = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    job = db.Column(db.String(64))
    publist_courses = db.relationship('Course')

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        """自动为password生成哈希值存入_password字段"""
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        """判断用户输入的密码和存储的hash密码是否相等"""
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_staff(self):
        return self.role == self.ROLE_STAFF
    

class Course(Base):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    description = db.Column(db.String(256))
    image_url = db.Column(db.String(256))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    author = db.relationship('User', backref=db.backref('course', cascade='all, delete-orphan'))
    chapters = db.relationship('Chapter')

    @property
    def url(self):
        return url_for('course.detail', course_id=self.id)

    def __repr__(self):
        return '<Course:{}>'.format(self.name)

class Chapter(Base):
    __tablename__ = 'chapter'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    description = db.Column(db.String(256))
    video_url = db.Column(db.String(256))
    video_duration = db.Column(db.String(24))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete="CASCADE"))
    course = db.relationship('Course',backref=db.backref('chapter', cascade='all, delete-orphan'))

    @property
    def url(self):
        return url_for('course.chapter', course_id=self.course_id, chapter_id=self.id)

    def __repr__(self):
        return '<Chapter:{}>'.format(self.name)