from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, DataRequired, URL, NumberRange
from simpledu.models import db, User, Course, Live
from wtforms import ValidationError, TextAreaField, IntegerField

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(3, 24)])
    email = StringField('邮箱', validators=[DataRequired(), Email(message='请输入合法的email地址')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24, message='密码长度要在6到24个字符之间')])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password', message='两次输入的密码不相同')])
    submit = SubmitField('提交')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email(message='请输入合法的email地址')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24, message='密码长度要在6到24个字符之间')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱未注册')
    
    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')

class CourseForm(FlaskForm):
    name = StringField('课程名称', validators=[DataRequired(), Length(5, 32, message='课程名称长度要在5到32个字符之间')])
    description = TextAreaField('课程简介', validators=[DataRequired(), Length(20,512)])
    image_url = StringField('封面图片', validators=[DataRequired(), URL(message='无效的url地址')])
    author_id = IntegerField('作者ID', validators=[DataRequired(), NumberRange(min=1, message='无效的用户ID')])
    submit = SubmitField('提交')

    def validate_author_id(self, field):
        if not User.query.get(field.data):
            raise ValidationError('用户不存在')

    def create_course(self):
        course = Course()
        # 使用课程表单数据填充course对象
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self, course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course
        
class LiveForm(FlaskForm):
    name = StringField('直播名称', validators=[DataRequired(), Length(5, 128, message='课程名称长度要在5到128个字符之间')])
    liveuser_id = IntegerField('直播用户ID', validators=[DataRequired(), NumberRange(min=1, message='无效的用户ID')])
    submit = SubmitField('提交')

    def validate_liveuser_id(self, field):
        if not User.query.get(field.data):
            raise ValidationError('用户不存在')

    def create_live(self):
        live = Live()
        # 使用直播表单数据填充course对象
        self.populate_obj(live)
        db.session.add(live)
        db.session.commit()
        return live
