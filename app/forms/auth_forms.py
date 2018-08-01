# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired,Email,EqualTo,InputRequired,ValidationError,NumberRange

from app.service import UserService
import re
#
#自定义验证器如果用自定义验证函数的方法实现,必须写在form类之前
#
#登录时用户名合法性验证
def validate_username_login(form,field):
	pattern = re.compile(r'^[0-9a-zA-Z_]{2,15}$')
	if not pattern.match(field.data):
		raise ValidationError('Username input is illegal')
#登录表单
class LoginForm(FlaskForm):
	username = StringField("Username",validators=[
		DataRequired(message="Please enter your username"),validate_username_login])
	password = PasswordField("Password",validators=[
		DataRequired(message="Please enter your password")])
	submit = SubmitField("Login")


#用户名输入合法性验证
def validate_username_reg(form,field):
	pattern = re.compile(r'^[0-9a-zA-Z_]{2,15}$')
	#组成合法性
	if not pattern.match(field.data):
		raise ValidationError('Username input is illegal')
	#查重
	if UserService.username_is_exist(field.data):
		raise ValidationError('Username already registered')
#昵称合法性验证
def validate_nickname(form,field):
	pattern = re.compile(r'^[0-9a-zA-Z_\u4E00-\u9FA5]{3,24}$')
	#组成合法性
	if not pattern.match(field.data):
		raise ValidationError('Nickname input is illegal')
	#查重
	if UserService.nickname_is_exist(field.data):
		raise  ValidationError('Nickname already registered')
#邮箱合法性验证,查重
def validate_email(form,field):
	if UserService.email_is_exist(field.data):
		raise ValidationError('Email already binded')
#验证年级合法性
def validate_grade(form,field):
	min = 1
	max = 3000
	pattern = re.compile(r'^[0-9]{1,4}$')
	if pattern.match(field.data):
		number = int(field.data)
		if number < min and number > max:
			raise ValidationError('Number input is illegal')
	else:
		raise ValidationError('Please input number')
#验证班级合法性
def validate_classnum(form,field):
	min = 1
	max = 20
	pattern = re.compile(r'^[0-9]{1,2}$')
	if pattern.match(field.data):
		number = int(field.data)
		if number < min and number > max:
			raise ValidationError('Number input is illegal')
	else:
		raise ValidationError('Please input number')

#注册表单
class RegisterForm(FlaskForm):
	username = StringField("* Username",validators=[
		DataRequired(message="Please enter your username"),validate_username_reg])
	nickname = StringField("* Nickname",validators=[
		DataRequired(message="Please enter your nickname"),validate_nickname])
	password = PasswordField("* Password",validators=[
		DataRequired(message="Please enter your password")])
	password_again = PasswordField("* PasswordAgain",validators=[
		DataRequired(message="Please enter your password again"),
		EqualTo('password',message="Password must be match")])
	email = StringField("*Email",description=u'Email绑定你的邮箱用于找回密码',validators=[
		DataRequired(message="Please enter your email"),
		Email(message="Your Email input is illegal"),validate_email])
	college = StringField("* College",validators=[
		DataRequired(message="Please enter your college name")])
	major = StringField("* Major",validators=[
		DataRequired(message="Please enter your major name")])
	grade = StringField("Grade",validators=[
		validate_grade])
	classnum = StringField("Class",validators=[
		validate_classnum])

	level = StringField()

	submit = SubmitField("Regist")


#用户信息更新（面向用户与UserUpdateForm不同）
class AuthUpdateForm(FlaskForm):
	nickname = StringField("Nickname", validators=[DataRequired()])
	email = StringField("Email", validators=[Email()])
	college = StringField("College", validators=[DataRequired()],render_kw={'readonly': 'true'})
	major = StringField("Major", validators=[DataRequired()],render_kw={'readonly': 'true'})
	grade = StringField("Grade", validators=[DataRequired()],render_kw={'readonly': 'true'})
	classnum = StringField("Classnum", validators=[DataRequired()],render_kw={'readonly': 'true'})
	submit = SubmitField("Submit")

#找回密码表单
class GetbackPwdForm(FlaskForm):
	username = StringField("Username",validators=[
		DataRequired(message="Please enter your username"),validate_username_login])
	email = StringField("Email",validators=[
		DataRequired(message="Please enter your email"),
		Email(message="Your email input is illegal")])
	submit = SubmitField("Send")

#重置密码表单
class ReplacePasswdForm(FlaskForm):
	password = PasswordField("Password",validators=[
		DataRequired(message="Please enter your new password")])
	password_again = PasswordField("PasswordAgain",validators=[
		DataRequired(message="Please enter your new password again"),
		EqualTo('password',message="Password must be match")])
	submit = SubmitField("Submit")