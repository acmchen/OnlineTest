# -*- coding: utf-8 -*-

from app.service import ExamService,UserService,ProLibService,BookService,ExamConditionService
from app.forms import ExamProblemSearchForm,ExamStudentSearchForm,ExamUpdateForm,ExamSearchForm,ExamProblemNumForm
from app.settings import Config
from app.filter import admin_required

from flask import request,render_template,redirect,url_for,flash
from flask_login import login_required,current_user

from . import bp
import re
import json
import base64
import random

#考试管理主页面
@bp.route('/exam-manage/',methods=['GET','POST'])
@bp.route('/exam-manage/<int:page>',methods=['GET','POST'])
@bp.route('/exam-manage/<int:page>/values/<string:values>',methods=['GET','POST'])
@login_required
@admin_required
def exam_manage(page=1,values=''):
    form = ExamSearchForm()

    if request.method == 'GET':
        values_json = {}
        if values != '':
            values_json = json.loads(base64.b64decode(values))
        pagination = ExamService.search_exam_info(values_json,page)
        return render_template('admin/exam/exam_manage.html',
                               form = form,
                               values = values,
                               pagination = pagination,
                               exam_list = pagination.items,
                               is_register = Config.IS_REGISTER,
                               status = Config.IS_HIDDEN,
                               active = Config.ADMIN_PAGE_ACTIVE['exam'])

    if form.validate_on_submit():
        values = base64.b64encode(json.dumps(form.to_dict()))
        return redirect(url_for('admin.exam_manage', page=1, values=values))

    return redirect(url_for('admin.exam_manage', page=page))

#新建考试
@bp.route('/exam-manage/add',methods=['GET','POST'])
@login_required
@admin_required
def exam_add():
    form = ExamUpdateForm()

    if request.method == 'GET':
        form.creater.data = current_user.user_name
        return render_template('admin/exam/exam_add.html',
                               form = form,
                               active = Config.ADMIN_PAGE_ACTIVE['exam'])

    if form.validate_on_submit():
        try:
            ExamService.add_exam(form)
            flash("Add exam success","success")
            return redirect(url_for('admin.exam_manage'))
        except:
           flash("Add exam field","danger")

    return render_template('admin/exam/exam_add.html',
                           form = form,
                           active = Config.ADMIN_PAGE_ACTIVE['exam'])
#更新考试信息
@bp.route('/exam-manage/update/<string:id>',methods=['GET','POST'])
@login_required
@admin_required
def exam_update(id):
    form = ExamUpdateForm()

    if request.method == 'GET':
        exam_info = ExamService.get_exam_detail_info(id)
        form.describe.data = exam_info.describe
        form.name.data = exam_info.name
        form.creater.data = exam_info.creater
        form.count.data = exam_info.count
        form.during_time.data = exam_info.during_time
        form.start_time.data = exam_info.start_time
        form.end_time.data = exam_info.end_time
        form.reg_start_time.data = exam_info.reg_start_time
        form.reg_end_time.data = exam_info.reg_end_time
        form.is_register.data = str(exam_info.is_register)
        form.is_hidden.data = str(exam_info.is_hidden)
        return render_template('admin/exam/exam_update.html',
                               id = id,
                               form = form,
                               active = Config.ADMIN_PAGE_ACTIVE['exam'])
    if form.validate_on_submit():
        try:
            ExamService.update_exam(form,id)
            flash("Update exam success")
            return redirect(url_for('admin.exam_update',id=id))
        except:
            flash("Update exam failed")

    flash("Update exam failed")
    return redirect(url_for('admin.exam_update', id=id))

#删除考试(慎用)
@bp.route('/exam-manage/del/<string:id>')
@login_required
@admin_required
def del_exam(id):
    try :
        ExamService.del_exam(id)
        flash("Del exam success")
    except:
        flash("Del exam failed")
    return redirect(url_for('admin.exam_manage'))

#添加考试成员
@bp.route('/exam-manage/<string:id>/add-member/<int:page>',methods=['GET','POST'])
@bp.route('/exam-manage/<string:id>/add-member/<int:page>/values/<string:values>',methods=['GET','POST'])
@login_required
@admin_required
def exam_add_member(id,page=1,values=''):
    form = ExamStudentSearchForm()
    apply_num = ExamService.get_apply_num_by_id(id)

    if request.method == 'GET':
        values_json = {}
        if values != '':
            values_json = json.loads(base64.b64decode(values))
        pagination = UserService.search_userinfo(values_json,page)
        return render_template('admin/exam/exam_add_member.html',
                               id = id,
                               values = values,
                               form = form,
                               pagination = pagination,
                               user_list = pagination.items,
                               apply_num = apply_num,
                               level = Config.USER_LEVEL,
                               status = Config.STATUS,
                               active = Config.ADMIN_PAGE_ACTIVE['exam'])

    if form.validate_on_submit():
        #查询
        if form.submit.data:
            values = base64.b64encode(json.dumps(form.to_dict()))
            return redirect(url_for('admin.exam_add_member', id=id, page=1, values=values))
        #批量添加参考成员
        elif form.submit_add.data:
            user_filter_list = UserService.search_userinfo_nopage(form.to_dict())
            ExamService.add_exam_member_by_list(id,user_filter_list)
            return redirect(url_for('admin.exam_add_member', id=id, page=page))
    else :
        return redirect(url_for('admin.exam_add_member',id=id,page=page))


#添加考试题库
@bp.route('/exam-manage/<string:id>/add-problem/<int:page>',methods=['GET','POST'])
@bp.route('/exam-manage/<string:id>/add-problem/<int:page>/values/<string:values>',methods=['GET','POST'])
@login_required
@admin_required
def exam_add_problem(id,page=1,values=''):
    form = ExamProblemSearchForm()
    problem_list_exam = ExamService.get_prolbem_list_by_id(id)

    if request.method == 'GET':
        values_json = {}
        if values != '':
            values_json = json.loads(base64.b64decode(values))
        pagination = ProLibService.search_problem_info(values_json,page)
        return render_template('admin/exam/exam_add_problem.html',
                               id = id,
                               values = values,
                               form = form,
                               pagination = pagination,
                               problem_list = pagination.items,
                               problem_list_exam = problem_list_exam,
                               type = Config.PROBLEM_TYPE_HTML,
                               status=Config.STATUS,
                               active = Config.ADMIN_PAGE_ACTIVE['exam'])

    if form.validate_on_submit():
        #查询
        if form.submit.data:
            values = base64.b64encode(json.dumps(form.to_dict()))
            return redirect(url_for('admin.exam_add_problem', id=id, page=1, values=values))
        #批量添加考试题目
        elif form.submit_add.data:

            problem_filter_list = ProLibService.search_problem_info_nopage(form.to_dict())
            ExamService.add_exam_problem_by_list(id,problem_filter_list)
            return redirect(url_for('admin.exam_add_problem', id=id, page=page))
    else:
        return redirect(url_for('admin.exam_add_problem', id=id, page=page))


#考试题库列表管理
@bp.route('/exam-manage/<string:id>/problem',methods=['GET','POST'])
@login_required
@admin_required
def exam_problem(id):
    form = ExamProblemNumForm()
    examinfo = ExamService.get_exam_detail_info(id)
    problem_list_exam = examinfo.problem_list                     #考试题库题目id列表
    problem_list_example = examinfo.problem_list_example          #考试样例试卷题目id列表
    problem_condition_dict = ExamService.get_problem_condition_dict_byid(id)     #考题情况字典
    choice = []
    blank = []
    short_answer = []
    choice_ex = []
    blank_ex = []
    short_answer_ex = []
    # 考试题目列表仅仅有id，通过循环获取
    # 题目相关信息，下一循环同理
    # 区别在于题库和样例试卷的题目不同
    for problem in problem_list_exam:
        problem_detail = ProLibService.get_problem_detailed_info(problem)
        book = BookService.get_book_by_id(problem_detail.belong_to_book)
        problem_detail.belong_to_book = book.book_name + '(' + book.version + ')'
        problem_detail.belong_to_unit = BookService.get_unit_by_id(problem_detail.belong_to_unit).unit_name
        problem_detail.belong_to_section = BookService.get_section_by_id(problem_detail.belong_to_section).section_name
        if problem_detail.type == Config.PROBLEM_TYPE['choice']:
            choice.append(problem_detail)
        elif problem_detail.type == Config.PROBLEM_TYPE['blank']:
            blank.append(problem_detail)
        elif problem_detail.type == Config.PROBLEM_TYPE['short_answer']:
            short_answer.append(problem_detail)

    for problem in problem_list_example:
        problem_detail = ProLibService.get_problem_detailed_info(problem)
        book = BookService.get_book_by_id(problem_detail.belong_to_book)
        problem_detail.belong_to_book = book.book_name + '(' + book.version + ')'
        problem_detail.belong_to_unit = BookService.get_unit_by_id(problem_detail.belong_to_unit).unit_name
        problem_detail.belong_to_section = BookService.get_section_by_id(problem_detail.belong_to_section).section_name
        if problem_detail.type == Config.PROBLEM_TYPE['choice']:
            choice_ex.append(problem_detail)
        elif problem_detail.type == Config.PROBLEM_TYPE['blank']:
            blank_ex.append(problem_detail)
        elif problem_detail.type == Config.PROBLEM_TYPE['short_answer']:
            short_answer_ex.append(problem_detail)

    #各题型考试题库字典
    problem_list_dict = dict((('choice',choice),('blank',blank),('short_answer',short_answer)))
    #样例试卷字典
    problem_list_example_dict = dict((('choice', choice_ex), ('blank', blank_ex), ('short_answer', short_answer_ex)))

    if request.method == 'GET':
        #右侧考试配置工具栏赋值
        form.choice_num.choices = [ (i,i) for i in range(len(choice)+1) ]
        form.blank_num.choices = [ (i,i) for i in range(len(blank)+1)]
        form.short_answer_num.choices = [ (i,i) for i in range(len(short_answer)+1)]
        form.choice_num.data = str(problem_condition_dict['choice']['num'])
        form.choice_score.data = str(problem_condition_dict['choice']['score'])
        form.blank_num.data = str(problem_condition_dict['blank']['num'])
        form.blank_score.data = str(problem_condition_dict['blank']['score'])
        form.short_answer_num.data = str(problem_condition_dict['short_answer']['num'])
        form.short_answer_score.data = str(problem_condition_dict['short_answer']['num'])
        form.is_random.data = str(problem_condition_dict['is_random'])
        return render_template('admin/exam/exam_problem.html',
                               form = form,
                               id = id,
                               is_random = problem_condition_dict['is_random'],
                               problem_num_dict = problem_condition_dict,
                               problem_list_dict = problem_list_dict,
                               problem_list_example = problem_list_example_dict,
                               status=Config.STATUS,
                               active=Config.ADMIN_PAGE_ACTIVE['exam'])

    if request.method == 'POST':
        #更新各类型考试题目的数量和分值
        ExamService.update_problem_number(form,id)
        return redirect(url_for('admin.exam_problem',id=id))

#参考成员管理
@bp.route('/exam-manage/<string:id>/member',methods=['GET','POST'])
@login_required
@admin_required
def exam_member(id):
    form = ExamStudentSearchForm()
    apply_num = ExamService.get_apply_num_by_id(id)
    member_list = []
    for student in apply_num:
        member_list.append(UserService.get_userinfo_by_id(student))

    if request.method == 'GET':
        return render_template('admin/exam/exam_member.html',
                               id = id,
                               form = form,
                               member_list = member_list,
                               status=Config.STATUS,
                               active=Config.ADMIN_PAGE_ACTIVE['exam'])
    #对当前页面中用户进行筛选
    filter = []
    if form.validate_on_submit():

        if form.username.data:
            username = re.compile('.*'+form.username.data+'.*')
        if form.nickname.data:
            nickname = re.compile('.*'+form.nickname.data+'.*')
        if form.college.data:
            college = re.compile('.*'+form.college.data+'.*')
        if form.major.data:
            major = re.compile('.*'+form.major.data+'.*')
        for item in member_list:
            if username and username.search(item.user_name):
                filter.append(item)
                continue
            if nickname and nickname.search(item.nick_name):
                filter.append(item)
                continue
            if college and college.search(item.college_name):
                filter.append(item)
                continue
            if major and major.search(item.major_name):
                filter.append(item)
                continue
            if item.grade == form.grade.data or item.classnum == form.classnum.data:
                filter.append(item)
                continue

    return render_template('admin/exam/exam_member.html',
                           id=id,
                           form=form,
                           member_list=filter,
                           active=Config.ADMIN_PAGE_ACTIVE['exam'])

#单独添加考试成员
@bp.route('/exam-manage/<string:id>/member/add/<string:user_id>/page/<int:page>')
@bp.route('/exam-manage/<string:id>/member/add/<string:user_id>/page/<int:page>/values/<string:values>')
@login_required
@admin_required
def add_exam_member_single(id,user_id,page=1,values=''):
    try:
        if UserService.get_userinfo_by_id(user_id).status:
            ExamService.add_exam_member_single(id,user_id)
            ExamConditionService.add_user_exam_condition(id,user_id)
            flash('success')
        else:
            flash('failed')
    except:
        flash('failed')

    if values == '':
        return redirect(url_for('admin.exam_add_member', id=id, page=page))

    return redirect(url_for('admin.exam_add_member',id=id,page=page,values=values))

#单独添加考试题目
@bp.route('/exam-manage/<string:id>/problem/add/<string:problem_id>/page/<int:page>')
@bp.route('/exam-manage/<string:id>/problem/add/<string:problem_id>/page/<int:page>/values/<string:values>')
@login_required
@admin_required
def add_exam_problem_single(id,problem_id,page=1,values=''):
    try:
        if ProLibService.get_problem_detailed_info(problem_id).status:
            ExamService.add_exam_problem_single(id,problem_id)
            flash('success')
        else:
            flash('failed')
    except:
        flash('failed')

    if values == '':
        return redirect(url_for('admin.exam_add_problem',id=id,page=page))

    return redirect(url_for('admin.exam_add_problem', id=id, page=page, values=values))
#单独删除考试成员
@bp.route('/exam-manage/<string:id>/member/del/<string:user_id>')
@login_required
@admin_required
def del_exam_member_single(id,user_id):
    try:
        ExamService.del_exam_member(id,user_id)
        flash('success')
    except:
        flash('failed')
    return redirect(url_for('admin.exam_member',id=id))
#单独删除考试题目
@bp.route('/exam-manage/<string:id>/problem/del/<string:problem_id>')
@login_required
@admin_required
def del_exam_problem_single(id,problem_id):
    try:
        ExamService.del_exam_problem(id,problem_id)
        flash('success')
    except:
        flash('failed')

    return redirect(url_for('admin.exam_problem',id=id))

#生成样例试卷
@bp.route('/exam-manage/<string:id>/makexamplepage')
@login_required
@admin_required
def make_example_page(id):
    #获取全考题列表
    problem_list_exam = ExamService.get_prolbem_list_by_id(id)
    #获取考题配置
    problem_condition_dict = ExamService.get_problem_condition_dict_byid(id)
    choice = []
    blank = []
    short_answer = []
    #生成样例试卷
    for problem in problem_list_exam:
        problem_detail = ProLibService.get_problem_detailed_info(problem)
        if problem_detail.type == Config.PROBLEM_TYPE['choice']:
            choice.append(problem_detail.pid)
        elif problem_detail.type == Config.PROBLEM_TYPE['blank']:
            blank.append(problem_detail.pid)
        elif problem_detail.type == Config.PROBLEM_TYPE['short_answer']:
            short_answer.append(problem_detail.pid)

    choice_r = random.sample(choice,problem_condition_dict['choice']['num'])
    blank_r = random.sample(blank,problem_condition_dict['blank']['num'])
    short_answer_r = random.sample(short_answer,problem_condition_dict['short_answer']['num'])

    List = choice_r + blank_r + short_answer_r

    ExamService.update_problem_list_example(List,id)

    return redirect(url_for('admin.exam_problem',id=id))
