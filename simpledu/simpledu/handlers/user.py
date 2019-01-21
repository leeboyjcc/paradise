from flask import Blueprint, render_template
from simpledu.models import User

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/<username>')
def index(username):
    userobj = User.query.filter_by(username=username)
    user = User.query.filter_by(username=username).first_or_404()
    for course in user.publish_courses:
        print(course, course.name)
    return render_template('detail.html', user=user)
