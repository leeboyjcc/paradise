from flask import Blueprint, render_template
from simpledu.decorators import admin_required
from simpledu.models import Course, User, db, Live
from flask import request, current_app
from flask import redirect, url_for, flash
from simpledu.forms import CourseForm, RegisterForm, LiveForm
from flask_login import current_user

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@admin_required
def index():
    print(request.__dict__)
    print(request.current_user)
    return render_template('admin/index.html')


@admin.route('/courses')
@admin_required
def courses():
	page = request.args.get('page', default=1, type=int)
	
	pagination = Course.query.paginate(
		page = page,
		per_page = current_app.config['ADMIN_PER_PAGE'],
		error_out = False
	)
	return render_template('admin/courses.html', pagination=pagination)

@admin.route('/courses/create', methods=['GET', 'POST'])
@admin_required
def create_course():
	form = CourseForm()
	if form.validate_on_submit():
		form.create_course()
		flash('课程创建成功', 'success')
		return redirect(url_for('admin.courses'))
	return render_template('admin/create_course.html', form=form)

@admin.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
	course = Course.query.get_or_404(course_id)
	form = CourseForm(obj=course)
	if form.validate_on_submit():
		form.update_course(course)
		flash('课程更新成功', 'success')
		return redirect(url_for('admin.courses'))
	return render_template('admin/edit_course.html', form=form, course=course)

@admin.route('/courses/<int:course_id>/delete')
@admin_required
def delete_course(course_id):
	course = Course.query.get_or_404(course_id)
	db.session.delete(course)
	db.session.commit()
	flash('课程 "{}" 删除成功'.format(course.name), 'success')
	return redirect(url_for('admin.courses'))

@admin.route('/users')
@admin_required
def users():
	page = request.args.get('page', default=1, type=int)
	pagination = User.query.paginate(
		page = page,
		per_page = current_app.config['ADMIN_PER_PAGE'],
		error_out = False
	)
	return render_template('admin/users.html', pagination=pagination)

@admin.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
	form = RegisterForm()
	if form.validate_on_submit():
		form.create_user()
		flash('用户创建成功', 'success')
		return redirect(url_for('admin.users'))
	return render_template('admin/create_user.html', form=form)

@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
	user = User.query.get_or_404(user_id)
	form =  RegisterForm(obj=user)
	if form.is_submitted():
		form.populate_obj(user)
		db.session.add(user)
		try:
			db.session.commit()
		except:
			db.session.rollback()
			flash('用户名或邮箱已经存在', 'error')
		else:
			flash('用户信息更新成功', 'success')
			return redirect(url_for('admin.users'))
	return render_template('admin/edit_user.html', form=form, user=user)

@admin.route('/users/<int:user_id>/delete', methods=['GET', 'POST'])
@admin_required
def delete_user(user_id):
	if current_user.id == user_id:
		flash('用户不能自我删除', 'error')
		return redirect(url_for('admin.users'))
	user = User.query.get_or_404(user_id)
	db.session.delete(user)
	db.session.commit()
	flash('用户已经被删除', 'success')
	return redirect(url_for('admin.users'))

@admin.route('/live')
@admin_required
def lives():
	page = request.args.get('page', default=1, type=int)
	pagination = Live.query.paginate(
		page = page,
		per_page = current_app.config['ADMIN_PER_PAGE'],
		error_out = False
	)
	return render_template('admin/lives.html', pagination=pagination)

@admin.route('/live/create', methods=['GET', 'POST'])
@admin_required
def create_live():
	form = LiveForm()
	if form.validate_on_submit():
		form.create_live()
		flash('直播创建成功', 'success')
		return redirect(url_for('admin.lives'))
	for field in form:
		print(field, field.label, field.data)
	return render_template('admin/create_live.html', form=form)


@admin.route('/admin/message', methods=['GET', 'POST'])
@admin_required
def send_message():
	return render_template('admin/message.html')
