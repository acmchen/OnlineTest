# -*- coding: utf-8 -*-
from app.models import UserInfo
from app.extensions import dbs
from app.settings import DevelopmentConfig

from werkzeug.security import generate_password_hash,check_password_hash


from datetime import datetime
import uuid
#分页每页显示条数
POST_PER_PAGE = 5
class UserService(object):
	#检查密码
	@staticmethod
	def check_password(passwdhash,password):
		return check_password_hash(passwdhash,password)
	#根据用户名获取用户信息
	@staticmethod
	def get_userinfo_by_uname(username):
		return UserInfo.query.filter_by(user_name=username).first()
	#根据id 获取用户信息
	@staticmethod
	def get_userinfo_by_id(id):
		return UserInfo.query.filter_by(user_id=id).first()
	#根据email获取用户信息
	@staticmethod
	def get_userinfo_by_email(email):
		return UserInfo.query.filter_by(email=email).first()
	#分页获取所有用户信息
	@staticmethod
	def get_all_userinfo(page):
		return UserInfo.query.paginate(page,POST_PER_PAGE,error_out=False)
	#条件查询用户
	@staticmethod
	def search_userinfo(userinfo,page):
		query = UserInfo.query
		if userinfo.has_key('username') and userinfo['username']:
			query = query.filter(UserInfo.user_name.like('%'+userinfo['username']+'%'))
		if userinfo.has_key('nickname') and userinfo['nickname'] :
			query = query.filter(UserInfo.nick_name.like('%'+userinfo['nickname']+'%'))
		if userinfo.has_key('major') and userinfo['major'] :
			query = query.filter(UserInfo.major_name.like('%'+userinfo['major']+'%'))
		if userinfo.has_key('college') and userinfo['college'] :
			query = query.filter(UserInfo.college_name.like('%'+userinfo['college']+'%'))
		if userinfo.has_key('grade') and userinfo['grade'] :
			query = query.filter_by(grade=int(userinfo['grade']))
		if userinfo.has_key('classnum') and userinfo['classnum'] :
			query = query.filter_by(classnum=int(userinfo['classnum']))
		if userinfo.has_key('level') and userinfo['level']!='0':
			query = query.filter_by(level=int(userinfo['level']))
		pagination = query.paginate(page,POST_PER_PAGE,error_out=False)
		return pagination
	#非分页条件查询用户信息，用户批量添加考试成员
	@staticmethod
	def search_userinfo_nopage(userinfo):
		query = UserInfo.query
		if userinfo.has_key('username') and userinfo['username']:
			query = query.filter(UserInfo.user_name.like('%' + userinfo['username'] + '%'))
		if userinfo.has_key('nickname') and userinfo['nickname']:
			query = query.filter(UserInfo.nick_name.like('%' + userinfo['nickname'] + '%'))
		if userinfo.has_key('major') and userinfo['major']:
			query = query.filter(UserInfo.major_name.like('%' + userinfo['major'] + '%'))
		if userinfo.has_key('college') and userinfo['college']:
			query = query.filter(UserInfo.college_name.like('%' + userinfo['college'] + '%'))
		if userinfo.has_key('grade') and userinfo['grade']:
			query = query.filter_by(grade=int(userinfo['grade']))
		if userinfo.has_key('classnum') and userinfo['classnum']:
			query = query.filter_by(classnum=int(userinfo['classnum']))
		if userinfo.has_key('level') and userinfo['level'] != '0':
			query = query.filter_by(level=int(userinfo['level']))
		return query.all()
	#添加用户信息
	@staticmethod
	def add_user(userinfo):
		user = UserInfo()
		user.user_id = str(uuid.uuid1())
		user.password = generate_password_hash(DevelopmentConfig.DEFAULT_PASSWORD)
		user.reg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		user.email = userinfo.username.data+'@OnlineTest.com'
		user.user_name = userinfo.username.data
		user.nick_name = userinfo.nickname.data
		user.college_name = userinfo.college.data
		user.major_name = userinfo.major.data
		user.grade = userinfo.grade.data
		user.classnum = userinfo.classnum.data
		user.level = userinfo.level.data
		dbs.session.add(user)
		dbs.session.commit()

	#注册用户
	@staticmethod
	def register_user(userinfo):
		user = UserInfo()
		user.user_id = str(uuid.uuid1())
		if userinfo.password :
			user.password = generate_password_hash(userinfo.password.data)
		else :
			user.password = generate_password_hash(DevelopmentConfig.DEFAULT_PASSWORD)
		user.reg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		user.email = userinfo.email.data
		user.user_name = userinfo.username.data
		user.nick_name = userinfo.nickname.data
		user.college_name = userinfo.college.data
		user.major_name = userinfo.major.data
		user.grade = userinfo.grade.data
		user.classnum = userinfo.classnum.data
		user.level = '1'
		dbs.session.add(user)
		dbs.session.commit()

	#更新用户密码，用于邮箱找回
	@staticmethod
	def update_userpasswd_by_confirm(userinfo):
		user = UserInfo.query.filter_by(user_id=userinfo.user_id).first()
		user.password = generate_password_hash(userinfo.password)
		dbs.session.commit()
	#更新用户信息
	@staticmethod
	def update_userinfo(userinfo,user_id):
		user = UserInfo.query.filter_by(user_id=user_id).first()
		user.nick_name = userinfo.nickname.data
		user.email = userinfo.email.data
		user.college_name = userinfo.college.data
		user.major_name = userinfo.major.data
		user.grade = userinfo.grade.data
		user.classnum = userinfo.classnum.data
		user.level = userinfo.level.data
		user.status = userinfo.status.data
		if userinfo.password.data:
			user.password = generate_password_hash(userinfo.password.data)
		dbs.session.commit()
	#普通用户更新用户信息，仅更新nickname和email
	@staticmethod
	def update_userinfo_auth(userinfo,user_id):
		user = UserInfo.query.filter_by(user_id=user_id).first()
		user.nick_name = userinfo.nickname.data
		user.email = userinfo.email.data
		dbs.session.commit()
	#删除用户
	@staticmethod
	def del_user(user_id):
		user = UserInfo.query.filter_by(user_id=user_id).first()
		dbs.session.delete(user)
		dbs.session.commit()
	#用户名重复性验证
	@staticmethod
	def username_is_exist(username):
		if UserInfo.query.filter_by(user_name=username).first():
			return True
		return False
	#邮箱重复性验证
	@staticmethod
	def email_is_exist(email):
		if UserInfo.query.filter_by(email=email).first():
			return True
		return False
	#昵称重复性验证
	@staticmethod
	def nickname_is_exist(nickname):
		if UserInfo.query.filter_by(nick_name=nickname).first():
			return True
		return False