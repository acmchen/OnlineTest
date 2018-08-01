# -*- coding: utf-8 -*-
from app.service import ExamConditionService,ExamService

from flask import url_for,render_template,request
from flask_login import current_user

from functools import wraps
from datetime import datetime
import time
#管理员权限过滤器
def admin_required(f):
    @wraps(f)
    def function(*args,**kwargs):
        failed = 'You do not have permission to enter'
        url = url_for('admin.login')
        if current_user.user_level < 3:
            return render_template("web/failed.html",failed=failed,url=url)
        return f(*args,**kwargs)
    return function
#教师权限过滤器
def teacher_required(f):
    @wraps(f)
    def function(*args,**kwargs):
        failed = 'You do not have permission to enter'
        url = url_for('web.index')
        if current_user.user_level < 2:
            return render_template("web/failed.html",failed=failed,url=url)
        return f(*args,**kwargs)
    return function

def create_exam_filter(f):
    @wraps(f)
    def function(*args, **kwargs):
        failed = 'You do not have permission to enter'
        url = url_for('web.exam_list')
        path = request.path.split('/')
        id = path[-2]
        count = int(path[-1])
        now_date = datetime.now()
        now_time = int(time.time())
        #考试设定信息
        exam_info = ExamService.get_exam_detail_info(id)
        #已经考的场数
        exam_count = ExamConditionService.get_user_exam_count(id, current_user.user_id)

        # 如果考试不是无限次那么已经考试次数>=设定次数就不能参加考试
        if exam_info.count != -1 and exam_count >= exam_info.count:
            return render_template("web/failed.html", failed=failed, url=url)

        #由于是新建考试,那么当前my_answer列表长度即新一场考试在列表中的下标,数值完全匹配才能够新建考试
        #(0号下标依然成立)
        if count != exam_count:
            return render_template("web/failed.html", failed=failed, url=url)

        if count != 0 :
            # 获得上一场考试的情况(用于验证上一场考试是否结束)
            exam_page = ExamConditionService.get_user_exam_page(id, current_user.user_id, count - 1)
            #如果要新建的考试不是第一场次考试, 那么检查上一场的考试
            if exam_page['now_time'] < exam_page['end_time']:
                if now_time < exam_page['end_time'] :
                    return render_template("web/failed.html", failed=failed, url=url)

        #验证考试时间
        if now_date < exam_info.start_time or now_date > exam_info.end_time:
            return render_template("web/failed.html", failed=failed, url=url)

        return f(*args, **kwargs)
    return function

def exam_filter(f):
    @wraps(f)
    def function(*args, **kwargs):
        failed = 'You do not have permission to enter'
        url = url_for('web.exam_list')
        path = request.path.split('/')
        id = path[-2]
        count = int(path[-1])
        now_date = datetime.now()
        exam_page = ExamConditionService.get_user_exam_page(id,current_user.user_id,count)
        exam_end_time = exam_page['end_time']
        #考试的设定信息
        exam_info = ExamService.get_exam_detail_info(id)
        #已经考的场数
        exam_count = ExamConditionService.get_user_exam_count(id, current_user.user_id)

        #中途加入的考试必须为最新的一场即下标为exam_count-1
        if count != exam_count - 1:
            return render_template("web/failed.html", failed=failed, url=url)

        #验证考试时间
        if now_date < exam_info.start_time or now_date > exam_info.end_time:
            return render_template("web/failed.html", failed=failed, url=url)

        #获取当前时间
        now_time = time.time()
        # +5s 延迟,防止js强制结束考试时无法提交
        if now_time > exam_end_time + 5 :
            return render_template("web/failed.html", failed=failed, url=url)
        return f(*args, **kwargs)
    return function