 # -*- coding: utf-8 -*-

from app.service import ExamService,ExamConditionService,UserService

from flask_login import login_required,login_user,logout_user,current_user
from flask import request,render_template,redirect,url_for,flash,session

from . import bp
import time

@bp.route('/exam-list/<int:page>',methods=['GET'])
@bp.route('/exam-list',methods=['GET'])
@login_required
def exam_list(page=1):
    if request.method=='GET':
        pagination = ExamService.get_user_exam_during(current_user,page)
        exam_count = ExamConditionService.get_user_exam_count_all(current_user.user_id)
        now_time = int(time.time())
        return render_template('web/exam/exam_list.html',
                               pagination = pagination,
                               exam_count = exam_count,
                               nowtime = now_time,
                               exam_list = pagination.items,
                               current_user = current_user)

@bp.route('/exam-history/<int:page>',methods=['GET'])
@bp.route('/exam-history/',methods=['GET'])
@login_required
def exam_history(page=1):
    if request.method=='GET':
        pagination = ExamService.get_user_exam_history(current_user,page)
        exam_count = ExamConditionService.get_user_exam_count_all(current_user.user_id)
        return render_template('web/exam/own_exam.html',
                               pagination = pagination,
                               exam_count = exam_count,
                               exam_list = pagination.items,
                               current_user = current_user)

@bp.route('/show-exam/<string:id>',methods=['GET'])
@login_required
def show_exam(id):
    if request.method == 'GET':
        user_info = {}
        if current_user.user_level > 1:
            condition = ExamConditionService.get_user_exam_condition_by_examid(id)
            for con in condition:
                user_info[con.sutdent_id] = UserService.get_userinfo_by_id(con.sutdent_id)
            condition = zip(condition,range(1,len(condition)+1))
            return render_template('web/exam/look_exam.html',
                                   condition = condition,
                                   user_info = user_info,
                                   current_user = current_user)

        elif current_user.user_level == 1:
            user_info_dict = {}
            condition_list = []
            condition = ExamConditionService.get_user_exam_condition_by_userid(id,current_user.user_id)
            user_info = UserService.get_userinfo_by_id(current_user.user_id)
            user_info_dict[condition.student_id] = user_info
            condition_list.append(condition)
            condition_list = zip(condition_list,range(1,len(condition_list)+1))
            return render_template('web/exam/look_exam.html',
                                   condition = condition_list,
                                   user_info = user_info_dict,
                                   current_user = current_user)

@bp.route('/exam-detail/<string:id>/count/<int:count>',methods=['GET'])
@login_required
def exam_detail(id,count):
    return render_template('web/exam/result.html',id=id,count=count)
