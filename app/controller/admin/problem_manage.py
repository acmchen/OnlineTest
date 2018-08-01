# -*- coding: utf-8 -*-

from app.service import ProLibService,BookService
from app.forms import ProblemSearchForms,ProblemUpdateForms,ProblemAddForms
from app.settings import Config
from app.filter import admin_required

from flask_login import login_required,current_user
from flask import request,render_template,redirect,url_for,flash

from . import bp
import json
import base64

#考题管理主页面
@bp.route('/problem-manage/',methods=['GET','POST'])
@bp.route('/problem-manage/<int:page>',methods=['GET','POST'])
@bp.route('/problem-manage/<int:page>/values/<string:values>',methods=['GET','POST'])
@login_required
@admin_required
def problem_manage(page=1,values=''):
    form = ProblemSearchForms()
    if request.method=='GET':
        values_json={}
        print values
        if values!='':
            values_json = json.loads(base64.b64decode(values))
        pagination = ProLibService.search_problem_info(values_json,page)
        return render_template('admin/problem/problem_manage.html',
                               form = form,
                               values = values,
                               pagination = pagination,
                               problem_list = pagination.items,
                               type = Config.PROBLEM_TYPE_HTML,
                               status = Config.STATUS,
                               active = Config.ADMIN_PAGE_ACTIVE['problem'])

    values = base64.b64encode(json.dumps(form.to_dict()))
    return redirect(url_for('admin.problem_manage', page=1, values=values))

#添加考题
@bp.route('/problem-manage/add',methods=['GET','POST'])
@login_required
@admin_required
def problem_add():
    form = ProblemAddForms()

    if request.method=='GET':
        form.author.data = current_user.user_name
        return render_template('admin/problem/problem_add.html',
                               form=form,
                               active=Config.ADMIN_PAGE_ACTIVE['problem'])

    try:
        ProLibService.add_problem(form)
        flash("Add problem success","success")
    except:
        flash("Add problem field","danger")
    return redirect(url_for('admin.problem_manage'))

#更新考题
@bp.route('/problem-manage/update/<string:id>',methods=['GET','POST'])
@login_required
@admin_required
def problem_update(id):
    form = ProblemUpdateForms()

    proIsExist = ProLibService.get_problem_detailed_info(id)
    if proIsExist is None:
        return redirect(url_for('admin.problem_manage'))

    if request.method=='GET':
        problem = ProLibService.get_problem_detailed_info(id)
        book = BookService.get_book_by_id(problem.belong_to_book)
        unit = BookService.get_unit_by_id(problem.belong_to_unit)
        section = BookService.get_section_by_id(problem.belong_to_section)
        form.type.data = problem.type
        form.desc_main.data = problem.desc_main
        form.desc_other.data = problem.desc_other
        form.author.data = problem.author
        form.answer.data = problem.answer
        form.tips.data = problem.tips
        form.tags.data = problem.tags
        form.subject.data = problem.subject
        form.level.data = str(problem.level)
        form.status.data = str(problem.status)
        if book :
            form.b_book_id.data = book.book_id
            form.b_book.data = book.book_name
        if unit :
            form.b_unit_id.data = unit.unit_id
            form.b_unit.data = unit.unit_name
        if section:
            form.b_section_id.data = section.section_id
            form.b_section.data = section.section_name

        return render_template('admin/problem/problem_update.html',
                               form=form,
                               active = Config.ADMIN_PAGE_ACTIVE['problem'])

    if form.book.data == '0':
        form.book.data = form.b_book_id.data
        form.unit.data = form.b_unit_id.data
        form.section.data = form.b_section_id.data
    #存在js级联查询,不能使用表单验证,如果使用必然不通过
    try:
        ProLibService.update_problem(form,id)
        flash("Update problem information success","success")

    except:
        flash("Update problem infomation failed","danger")

    return redirect(url_for('admin.problem_update',id=id))

#考题删除（备用）
@bp.route('/problem-manage/delete/<string:id>')
@login_required
@admin_required
def problem_delete(id):
    ProLibService.del_problem(id)
    return redirect(url_for('admin.problem_manage'))

