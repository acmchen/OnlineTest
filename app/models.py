# -*- coding: utf-8 -*-
from datetime import datetime
from flask_login import UserMixin
from app.extensions import dbm,dbs

'''MysqlDb models'''
class UserLevel():
	STUDENT = 1
	TEACHER = 2
	ADMIN = 3

class UserInfo(dbs.Model):
	__tablename__ = 'userinfo'

	user_id = dbs.Column(dbs.String(64), primary_key=True)
	user_name = dbs.Column(dbs.String(64),nullable=False, unique=True)
	email = dbs.Column(dbs.String(64),unique=True)
	password = dbs.Column(dbs.String(128),nullable=False)
	nick_name = dbs.Column(dbs.String(64),nullable=False, unique=True)
	level = dbs.Column(dbs.Integer, default=UserLevel.STUDENT,nullable=False)
	reg_time = dbs.Column(dbs.DateTime, default=datetime.now(),nullable=False)
	major_name = dbs.Column(dbs.String(32))
	college_name = dbs.Column(dbs.String(32))
	grade = dbs.Column(dbs.Integer)
	classnum = dbs.Column(dbs.Integer)
	status = dbs.Column(dbs.Integer, default=1,nullable=False)


class UserLog(UserMixin):

	def __init__(self,user_id=None ,user_name=None,user_level=1):
		self.user_id = user_id
		self.user_name = user_name
		self.user_level = user_level

	def is_active(self):
		if UserInfo.query.filter(user_name=self.user_name).first().status == 1:
			return True
		return False

	def get_id(self):
		return unicode(self.user_id)

class ProType():
	CHOICE = 1
	BLANK = 2
	SHORT_ANSWER = 3

class ProblemInfo(dbs.Model):
	__tablename__ = 'probleminfo'

	pid = dbs.Column(dbs.String(64),primary_key=True)
	type = dbs.Column(dbs.String(32),nullable=False,default=ProType.CHOICE)
	desc_main = dbs.Column(dbs.Text,nullable=False)
	desc_other = dbs.Column(dbs.Text)
	answer = dbs.Column(dbs.Text,nullable=False)
	author = dbs.Column(dbs.String(32))
	tips = dbs.Column(dbs.Text)
	tags = dbs.Column(dbs.Text)
	date = dbs.Column(dbs.DateTime,default=datetime.now(),nullable=False)
	level = dbs.Column(dbs.Integer)
	belong_to_book = dbs.Column(dbs.String(64))
	belong_to_unit = dbs.Column(dbs.String(64))
	belong_to_section = dbs.Column(dbs.String(64))
	subject = dbs.Column(dbs.String(64))
	status = dbs.Column(dbs.Integer,default=1)

class BookInfo(dbs.Model):
	__tablename__ = 'bookinfo'

	book_id = dbs.Column(dbs.String(64),primary_key=True)
	book_name = dbs.Column(dbs.String(64),nullable=False)
	version = dbs.Column(dbs.String(32))
	subject = dbs.Column(dbs.String(32),nullable=False)
	author = dbs.Column(dbs.String(64))
	publisher = dbs.Column(dbs.String(64))
	publish_time = dbs.Column(dbs.String(64))

class UnitInfo(dbs.Model):
	__tablename__ = 'unitinfo'
	unit_id = dbs.Column(dbs.String(64),primary_key=True)
	unit_name = dbs.Column(dbs.String(64),nullable=False)
	belong_to_book = dbs.Column(dbs.String(64),dbs.ForeignKey('bookinfo.book_id',ondelete='CASCADE'),nullable=False)

class SectionInfo(dbs.Model):
	__tablename__ = 'sectioninfo'

	section_id = dbs.Column(dbs.String(64),primary_key=True)
	section_name = dbs.Column(dbs.String(64),nullable=False)
	belong_to_unit = dbs.Column(dbs.String(64),dbs.ForeignKey('unitinfo.unit_id',ondelete='CASCADE'),nullable=False)


'''MongoDb models'''

class ExamRegister():
	REGISTER_OFF = 0
	REGISTER_ON = 1

class ExamHidden():
	NOTHIDDEN = 0
	HIDDEN = 1

class ExamRandom():
	NORMAL = 0
	RANDOM = 1

class ExamResult():
	NOTSHOW = 0
	SHOW = 1


class LogInfo(dbm.EmbeddedDocument):
	login_time = dbm.DateTimeField()
	logout_time = dbm.DateTimeField()
	ip = dbm.StringField(required=True,max_length=32)
	#mac = dbm.StringField(required=True,max_length=64)

class MyAnswer(dbm.EmbeddedDocument):
	index = dbm.IntField()
	page = dbm.StringField()
	answer = dbm.DictField(default={})
	subtime = dbm.DateTimeField()
	grade = dbm.IntField(default=0)


class ExamInfo(dbm.Document):
	name = dbm.StringField(required=True, max_length=256)
	describe = dbm.StringField()
	count = dbm.IntField(default=1)

	during_time = dbm.IntField(required=True)
	start_time = dbm.DateTimeField(default=datetime.now())
	end_time = dbm.DateTimeField(default=datetime.now())

	apply_num = dbm.ListField(dbm.StringField(max_length=64))
	exam_num = dbm.ListField(dbm.StringField(max_length=64))
	creater = dbm.StringField(max_length=32)

	reg_start_time = dbm.DateTimeField()
	reg_end_time = dbm.DateTimeField()

	problem_list = dbm.ListField(dbm.StringField(max_length=128))
	problem_list_example = dbm.ListField(dbm.StringField(max_length=128))

	choice = dbm.DictField(default={'num':0,'score':0})
	blank = dbm.DictField(default={'num':0,'score':0})
	answer = dbm.DictField(default={'num':0,'score':0})

	is_random = dbm.IntField(default=ExamRandom.RANDOM)
	is_register = dbm.IntField(default=ExamRegister.REGISTER_OFF)
	is_hidden = dbm.IntField(default=ExamHidden.HIDDEN)
	is_show_result = dbm.IntField(default=ExamResult.NOTSHOW)

	def __unicode__(self):
		return self.name

class ExamConditionInfo(dbm.Document):
	student_id = dbm.StringField(required=True,max_length=64)
	exam_id = dbm.StringField(required=True,max_length=64)
	log_info = dbm.ListField(dbm.EmbeddedDocumentField(LogInfo))
	my_answer = dbm.ListField(dbm.EmbeddedDocumentField(MyAnswer))
	final_grade = dbm.IntField()
	status = dbm.BooleanField(default=True)




