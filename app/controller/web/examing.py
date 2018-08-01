# -*- coding: utf-8 -*-

from app.service import ExamService,ProLibService,ExamConditionService
from app.settings import Config
from flask_login import login_required,login_user,logout_user,current_user
from flask import request,render_template,redirect,url_for,flash,session
from app.filter import create_exam_filter,exam_filter

from . import bp

import time
import random
import json

#新建考试

@bp.route('/exam/<string:id>/<int:count>',methods=['GET'])
@login_required
@create_exam_filter
def examing(id,count):
    if request.method == 'GET':
        #记录登入信息,更新参考用户
        login_ip = request.remote_addr
        ExamConditionService.update_exam_condition_begin(id,current_user.user_id,login_ip)
        #生成考试页面存储到my_answer里
        page_dict = create_page(id)
        page_dict['now_time'] = int(time.time())
        page_dict['end_time'] = page_dict['now_time'] + page_dict['times'] * 60
        exam_page_json = json.dumps(page_dict)
        ExamConditionService.save_page(id, current_user.user_id, exam_page_json, None, count)
        return render_template('web/exam/exam.html',id=id)

@bp.route('/exam-continue/<string:id>/<int:count>',methods=['GET'])
@login_required
@exam_filter
def exam_continue(id,count):
    # 记录登入信息,更新参考用户
    login_ip = request.remote_addr
    ExamConditionService.update_exam_condition_begin(id, current_user.user_id, login_ip)

    return render_template('web/exam/exam.html',id=id,count=count)

def create_page(id):
    examAllInfo = ExamService.get_exam_detail_info(id)
    choice = []
    blank = []
    short_answer = []
    problem_list = []
    if examAllInfo.is_random == 1:
        problem_list = examAllInfo.problem_list
    elif examAllInfo.is_random == 0:
        problem_list = examAllInfo.problem_list_example

    for problem in problem_list:

        problem_detail = ProLibService.get_problem_detailed_info(problem)
        if problem_detail.type == Config.PROBLEM_TYPE['choice']:
            # 选项乱序
            list = problem_detail.desc_other.split('#$')
            problem_detail.desc_other = random.sample(list, len(list))
            choice.append(problem_detail)
        elif problem_detail.type == Config.PROBLEM_TYPE['blank']:
            blank.append(problem_detail)
        elif problem_detail.type == Config.PROBLEM_TYPE['short_answer']:
            short_answer.append(problem_detail)

            # 题目乱序
    choice_r = random.sample(choice, examAllInfo.choice['num'])
    blank_r = random.sample(blank, examAllInfo.blank['num'])
    short_answer_r = random.sample(short_answer, examAllInfo.answer['num'])

    # 生成json
    exam_page = {}
    exam_page['name'] = examAllInfo.name
    exam_page['choice'] = []
    exam_page['blank'] = []
    exam_page['short_answer'] = []
    exam_page['times']  = examAllInfo.during_time            #记录时长
    exam_page['now_time'] = int(time.time())                                  #当前时间(时间戳,在render前赋值保证精确)
    exam_page['end_time'] = exam_page['now_time'] + exam_page['times']        #结束时间(时间戳,在render前赋值保证精确)
    exam_page['choice_score'] = examAllInfo.choice['score']
    exam_page['blank_score'] = examAllInfo.blank['score']
    exam_page['short_answer_score'] = examAllInfo.answer['score']
    #count为当前考试在my_answer列表中的下标值
    exam_page['count'] = ExamConditionService.get_user_exam_count(id, current_user.user_id)
    '''
    {
        'choice':[
            {'pid':'123',
            'describe_main':'test1',
            'describe_other':['a','b','c','d'],
            },
            {'pid':'1234',
            'describe_main':'test2',
            'describe_other':['a','b','c','d','e'],
            }
        ],
        'blank':[
            {'pid':'1111',
            'describe_main':'test3',
            'describe_other':'',
            'answer':''
            }]
        'short_answer':[],
        'name':'Test',
        'times':'120',
        'now_time':''
        'end_time':''
        'choice_score':10,
        'blank_score':0,
        'short_answer_score':0
        'count':0
    }
    '''
    for problem in choice_r:
        problem_dict = {'pid': problem.pid, 'desc_main': problem.desc_main,
                        'desc_other': problem.desc_other, 'answer': ''}
        exam_page['choice'].append(problem_dict)
    for problem in blank_r:
        problem_dict = {'pid': problem.pid, 'desc_main': problem.desc_main,
                        'desc_other': problem.desc_other, 'answer': ''}
        exam_page['blank'].append(problem_dict)
    for problem in short_answer_r:
        problem_dict = {'pid': problem.pid, 'desc_main': problem.desc_main,
                        'desc_other': problem.desc_other, 'answer': ''}
        exam_page['short_answer'].append(problem_dict)



    return exam_page

@bp.route('/examing/getpage/<string:id>/<int:count>',methods=['GET'])
@login_required
def get_page(id,count):

    page,answer = ExamConditionService.get_page(id,current_user.user_id,count)
    page = json.loads(page)
    page['now_time'] = int(time.time())
    page_dict = {'page':page,'answer':answer}
    page_json = json.dumps(page_dict)

    return page_json

@bp.route('/examing/getpage-result/<string:id>/<int:count>',methods=['GET'])
@login_required
def get_page_result(id,count):

    page,answer = ExamConditionService.get_page(id,current_user.user_id,count)
    page = json.loads(page)
    true_answer = {}
    for item in page['choice']+page['blank']+page['short_answer']:
        pid = item['pid']
        true_answer[pid]=ProLibService.get_problem_detailed_info(item['pid']).answer

    page['now_time'] = int(time.time())
    page_dict = {'page':page,'answer':answer,'true_answer':true_answer}
    print true_answer
    page_json = json.dumps(page_dict)

    return page_json

@bp.route('/examing/save/<string:id>/<int:count>',methods=['POST'])
@login_required
@exam_filter
def save_page(id,count):

    try:
        answer_json = request.json
        print  answer_json
        # 在进入页面时loginfo列表添加了新的一项此时为对应下标应-1
        ExamConditionService.save_page(id,current_user.user_id,None,answer_json,count)
        return json.dumps({'key':'success'})
    except:
        return json.dumps({'key':'failed'})

@bp.route('/examing/finish/<string:id>/<int:count>',methods=['POST'])
@login_required
@exam_filter
def exam_finish(id,count):
    exam_answer = request.json
    ExamConditionService.save_page(id,current_user.user_id,None,exam_answer,count)
    print exam_answer
    logout_ip = request.remote_addr
    ExamConditionService.update_exam_condition(id,current_user.user_id,logout_ip,count)

    grade = 0
    problem_condition_dict = ExamService.get_problem_condition_dict_byid(id)

    for pid, answer in exam_answer['choice'].items():
        problem = ProLibService.get_problem_detailed_info(pid)
        if answer == problem.answer:
            grade += problem_condition_dict['choice']['score']

    ExamConditionService.update_user_exam_grade(id, current_user.user_id, grade, count)

    return json.dumps({'key':'success'})





