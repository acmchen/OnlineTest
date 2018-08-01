# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired,Email

'''管理员用户操作相关表单'''
#用户查询表单
class UserSearchForm(FlaskForm):
	username = StringField("Username")
	nickname = StringField("Nickname")
	college = StringField("College")
	major = StringField("Major")
	grade = StringField("Grade")
	classnum = StringField("ClassNum")
	level = SelectField("level",validators=[DataRequired()],choices=[('0',u'全部'),('1',u'学生'),('2',u'教师'),('3',u'管理员')],default='0')
	submit = SubmitField("Search")
	def to_dict(self):
		return {
			'username':self.username.data,
			'nickname':self.nickname.data,
			'college':self.college.data,
			'major':self.major.data,
			'grade':self.grade.data,
			'classnum':self.classnum.data,
			'level':self.level.data
		}

#用户信息更新表单
class UserinfoUpdateForm(FlaskForm):
	nickname = StringField("Nickname",validators=[DataRequired(message="Please enter nickname")])
	email = StringField("Email",validators=[])
	college = StringField("College",validators=[DataRequired(message="Please enter college name")])
	major = StringField("Major",validators=[DataRequired(message="Please enter major name")])
	grade = StringField("Grade",validators=[])
	classnum = StringField("Classnum",validators=[])
	level = SelectField("level",validators=[DataRequired()],choices=[('1',u'学生'),('2',u'教师'),('3',u'管理员')])
	status = SelectField("Status",validators=[DataRequired()],choices=[('0',u'禁用'),('1',u'启用')])
	password = StringField("Password(Reset)")
	submit = SubmitField("Submit")
#添加用户表单
class UserAddForm(FlaskForm):
	username = StringField("Username",validators=[DataRequired(message="Please enter username")])
	nickname = StringField("Nickname",validators=[DataRequired(message="Please enter nickname")])
	college = StringField("College",validators=[DataRequired(message="Please enter college name")])
	major = StringField("Major",validators=[DataRequired(message="Please enter major name ")])
	grade = StringField("Grade",validators=[])
	classnum = StringField("Class",validators=[])
	level = SelectField("Level",validators=[DataRequired()],choices=[('1',u'学生'),('2',u'教师'),('3',u'管理员')],default=1)
	status = SelectField("Status",validators=[DataRequired()],choices=[('0',u'禁用'),('1',u'启用')],default=1)
	submit = SubmitField("Add")