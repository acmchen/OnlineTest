# -*- coding: utf-8 -*-
from app.models import UserLog
from app.extensions import login_manager
from app.service.user_service import UserService
from app.forms import LoginForm
from app.filter import admin_required

from flask_login import current_user,login_required,login_user,logout_user
from flask import request,render_template,redirect,url_for,flash,session

from . import bp

#管理员首页路由

@bp.route("/")
@bp.route("/index")
@login_required
@admin_required
def index():
	return render_template("admin/index.html",current_user=current_user)

#管理员登录
@bp.route("/login",methods=["GET","POST"])
def login():
	form = LoginForm()

	if session.has_key('user_id') and session['user_id']:
		return redirect(url_for('admin.index'))
	if request.method=='GET':
		return render_template('admin/login.html',form=form)

	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		userinfo = UserService.get_userinfo_by_uname(username)
		if userinfo:
			user = UserLog(userinfo.user_id,userinfo.user_name,userinfo.level)
			if user and userinfo.status \
					and UserService.check_password(userinfo.password,password):
				login_user(user)
				return redirect(url_for('admin.index'))
		else:
			flash('unable to login')
	return render_template('admin/login.html',form=form)

#回调函数,用于current_user获取相关user信息
@login_manager.user_loader
def load_user(id):
	if id is None:
		redirect(url_for('admin.login'))
	userinfo = UserService.get_userinfo_by_id(id)
	user = UserLog(userinfo.user_id,userinfo.user_name,userinfo.level)
	if user.is_active:
		return user
	else :
		return None
#登出
@bp.route("/logout")
@login_required
@admin_required
def logout():
	logout_user()
	return redirect(url_for('admin.login'))

