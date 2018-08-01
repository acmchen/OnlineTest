# -*- coding: utf-8 -*-
from app.models import UserInfo,UserLog
from app.extensions import login_manager
from app.service import UserService,send_email,generate_email_token,verify_email_token
from app.forms import LoginForm,GetbackPwdForm,ReplacePasswdForm,RegisterForm,AuthUpdateForm

from flask_login import login_required,login_user,logout_user,current_user
from flask import request,render_template,redirect,url_for,flash,session

from . import bp
#首页路由
@bp.route("/",methods=["GET"])
@bp.route("/index")
def index():
	return render_template("web/index.html",
						   current_user = current_user)
#查看个人信息
@bp.route('/my-info',methods=['GET'])
@login_required
def user_info():
	if request.method == 'GET':
		userinfo = UserService.get_userinfo_by_id(current_user.user_id)
		return render_template('web/auth/info.html',user_info = userinfo)
#登录
@bp.route("/login",methods=["GET","POST"])
def login():
	form = LoginForm()

	if session.has_key('user_id') and session['user_id']:
		return redirect(url_for('web.index'))
	if request.method=='GET':
		return render_template('web/auth/login.html',form=form)

	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		userinfo = UserService.get_userinfo_by_uname(username)
		if userinfo:
			user = UserLog(userinfo.user_id, userinfo.user_name, userinfo.level)
			if user and userinfo.status \
					and UserService.check_password(userinfo.password, password):
				login_user(user)
				return redirect(url_for('web.index'))
			else:
				flash(u'您的用户名或密码错误')
		else:
			flash(u'您的用户名或密码错误')
	return render_template('web/auth/login.html',form=form)
#注册
@bp.route("/register",methods=["GET","POST"])
def register():
	form = RegisterForm()

	if current_user.is_authenticated:
		return render_template('web/index.html')
	if request.method=='GET':
		return render_template('web/auth/register.html',form=form)

	if form.validate_on_submit():
		try:
			UserService.register_user(form)
		except Exception,e:
			print e
			flash('regist failed')
			return render_template('web/auth/register.html', form=form)
		flash('regist success ! please login :)')
		return redirect(url_for('web.login'))
	return render_template('web/auth/register.html', form=form)
#更新个人信息
@bp.route("/update-info",methods=['GET','POST'])
@login_required
def update_info():
	form = AuthUpdateForm()

	if request.method == 'GET':
		userinfo = UserService.get_userinfo_by_id(current_user.user_id)
		form.nickname.data = userinfo.nick_name
		form.email.data = userinfo.email
		form.college.data = userinfo.college_name
		form.major.data = userinfo.major_name
		form.grade.data = userinfo.grade
		form.classnum.data = userinfo.classnum
		return render_template('web/auth/update_info.html',form = form)

	if form.validate_on_submit():
		try:
			UserService.update_userinfo_auth(form,current_user.user_id)
			flash('Update Success')
		except:
			flash('Update Failed')

	return render_template('web/auth/update_info.html',form=form)
#找回密码
@bp.route("/resetpwd",methods=["GET","POST"])
def getback():
	form = GetbackPwdForm()

	if request.method == 'GET':
		return render_template('web/auth/forgotpwd.html', form=form)

	if form.validate_on_submit():
		username = form.username.data
		email = form.email.data
		user = UserService.get_userinfo_by_email(email)
		if user is None or username != user.user_name:
			flash(u'您的用户名和邮箱不匹配,请确认后重新输入')
			return redirect(url_for('web.getback'))

		token = generate_email_token(email)
		confirm_url = url_for('web.confirm_email',token=token,external=True)
		html = 'Please click url to finishing confirm. After, you can replace your password.<br>'+confirm_url
		sender = 'sdutonlinetest@163.com'
		subject = 'OnlineTest Confirm Email'
		try :
			send_email(subject,sender,email,html)
			flash('Your confirm email send successful! :)','success')
		except:
			flash('Your confirm email send failed :(','danger')

		return redirect(url_for('web.getback'))
	return render_template('web/auth/forgotpwd.html', form=form)
#邮件跳转验证
@bp.route("/confirm/<string:token>", methods=['GET','POST'])
def confirm_email(token):
	success = 'You have replaced your password successfully!'
	failed = 'The confirmation link is invalid or has expired.'
	url_f = url_for('web.getback')
	url_s = url_for('web.login')
	form = ReplacePasswdForm()
	try :
		email = verify_email_token(token)
		if email is None:
			return render_template("web/failed.html",failed=failed,url=url_f)
	except :
		return render_template("web/falied.html",failed=failed,url=url_f)

	if request.method == 'GET':
		return render_template('web/auth/update_password.html',form=form)

	if form.validate_on_submit():
		password = form.password.data
		password_again = form.password_again.data
		try:
			user = UserService.get_userinfo_by_email(email['email'])
			user.password = password_again
			UserService.update_userpasswd_by_confirm(user)
			flash(u"您的密码已经成功更新,请登录")
			return redirect(url_for('web.logout'))
		except:
			flash(u"您的密码更新失败,请重试")
			return redirect(url_for('web.confirm_email',token=token))

	return render_template('web/auth/update_password.html',form=form)

#回调函数获取user信息
@login_manager.user_loader
def load_user(id):
	if id is None:
		redirect(url_for('web.login'))
	userinfo = UserService.get_userinfo_by_id(id)
	user = UserLog(userinfo.user_id,userinfo.user_name,userinfo.level)
	if user.is_active:
		return user
	else :
		return None
#登出
@bp.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('web.login'))


