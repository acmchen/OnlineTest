# -*- coding: utf-8 -*-

from app.service import UserService
from app.filter import admin_required
from app.forms import UserSearchForm,UserinfoUpdateForm,UserAddForm
from app.settings import Config

from flask_login import login_required
from flask import request,render_template,redirect,url_for,flash

from . import bp
import json
import base64

#用户管理界面
@bp.route('/user-manage/',methods=['GET','POST'])
@bp.route('/user-manage/<int:page>',methods=['GET','POST'])
@bp.route('/user-manage/<int:page>/values/<string:values>',methods=['GET','POST'])
@login_required
@admin_required
def user_manage(page=1,values=''):
    form = UserSearchForm()

    if request.method=='GET':
        values_json={}
        #如果values有值则解码进行筛选查询
        if values!='':
            values_json = json.loads(base64.b64decode(values))
            print json.loads(base64.b64decode(values))
        pagination = UserService.search_userinfo(values_json,page)
        return render_template('admin/user/user_manage.html',
                                form = form,
                                values = values,
                                user_list = pagination.items,
                                pagination = pagination,
                                level = Config.USER_LEVEL,
                                status = Config.STATUS,
                                active = Config.ADMIN_PAGE_ACTIVE['user'])

    if form.validate_on_submit():
        #对于筛选查询的内容转为json格式并编码,做url参数
        values=base64.b64encode(json.dumps(form.to_dict()))
        return redirect(url_for('admin.user_manage',page=1,values=values))

    return redirect(url_for('admin.user_manage', page=page))

#用户信息更新
@bp.route('/user-manage/update/<string:id>',methods=['GET','POST'])
@login_required
@admin_required
def user_update(id):
    form = UserinfoUpdateForm()
    if request.method=='GET':
        user = UserService.get_userinfo_by_id(id)
        form.nickname.data = user.nick_name
        form.email.data = user.email
        form.college.data = user.college_name
        form.major.data = user.major_name
        form.grade.data = user.grade
        form.classnum.data = user.classnum
        form.level.data = str(user.level)
        form.status.data = str(user.status)
        return render_template('admin/user/user_update.html',
                               form=form,
                               active=Config.ADMIN_PAGE_ACTIVE['user'])

    if form.validate_on_submit():
        try :
            UserService.update_userinfo(form,id)
            flash("update sucess","success")
        except:
            flash("update failed","danger")

    return render_template('admin/user/user_update.html',
                            form=form,
                            active=Config.ADMIN_PAGE_ACTIVE['user'])


#用户删除（非特殊情况不使用）
@bp.route('/user-manage/delete/<string:id>')
@login_required
@admin_required
def user_delete(id):
    try:
        UserService.del_user(id)
        flash("delete user success","success")
    except:
        flash("delete user failed!","danger")
    return redirect(url_for('admin.user_manage'))

#添加用户
@bp.route('/user-manage/add',methods=['GET','POST'])
@login_required
@admin_required
def user_add():
    form = UserAddForm()

    if request.method == 'GET':
        return render_template('admin/user/user_add.html',
                               form=form,active=Config.ADMIN_PAGE_ACTIVE['user'])

    if form.validate_on_submit():
        try:
            UserService.add_user(form)
            flash("Add user success")

        except:
            flash("Add user failed")

    return redirect(url_for('admin.user_manage'))