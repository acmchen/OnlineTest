# -*- coding: utf-8 -*-
from app.models import ExamConditionInfo,ExamInfo,MyAnswer,LogInfo
from datetime import datetime
from bson import ObjectId
POST_PER_PAGE = 10
'''考试相关数据层'''
class ExamService(object):
    #多条件查询
    @staticmethod
    def search_exam_info(examinfo,page):
        query = ExamInfo.objects
        if examinfo.has_key('name') and examinfo['name'] :
            query = query.filter(name__contains=examinfo['name'])
        if examinfo.has_key('start_time') and examinfo['start_time']:
            start_time = datetime.strptime(examinfo['start_time'],'%Y-%m-%d %H:%M:%S')
            query = query.filter(start_time__gte=start_time)
        if examinfo.has_key('end_time') and examinfo['end_time']:
            end_time = datetime.strptime(examinfo['end_time'],'%Y-%m-%d %H:%M:%S')
            query = query.filter(end_time__lte=end_time)
        if examinfo.has_key('creater') and examinfo['creater']:
            query = query.filter(creater__contains=examinfo['creater'])
        if examinfo.has_key('is_register') and examinfo['is_register']:
            query = query.filter(is_register=examinfo['is_register'])
        if examinfo.has_key('is_hidden') and examinfo['is_hidden']:
            query = query.filter(is_hidden=examinfo['is_hidden'])
        pagination = query.paginate(page=page,per_page=POST_PER_PAGE)
        return pagination
    #多条件查询(非后台,教师账号用)
    @staticmethod
    def search_exam_info_teacher(examinfo,user,page):
        query = ExamInfo.objects
        if examinfo.has_key('name') and examinfo['name'] :
            query = query.filter(name__icontains=examinfo['name'])
        if examinfo.has_key('start_time') and examinfo['start_time']:
            start_time = datetime.strptime(examinfo['start_time'],'%Y-%m-%d %H:%M:%S')
            query = query.filter(start_time__gte=start_time)
        if examinfo.has_key('end_time') and examinfo['end_time']:
            end_time = datetime.strptime(examinfo['end_time'],'%Y-%m-%d %H:%M:%S')
            query = query.filter(end_time__lte=end_time)
        if examinfo.has_key('creater') and examinfo['creater']:
            query = query.filter(creater__icontaions=examinfo['creater'])
        if examinfo.has_key('is_register') and examinfo['is_register']:
            query = query.filter(is_register=examinfo['is_register'])
        if examinfo.has_key('is_hidden') and examinfo['is_hidden']:
            query = query.filter(is_hidden=examinfo['is_hidden'])
        pagination = query.filter(creater=user.user_name).paginate(page=page, per_page=POST_PER_PAGE)
        return pagination
    #分页获取所有考试信息
    @staticmethod
    def get_all_exam(page):
        return ExamInfo.objects.paginate(page=page,per_page=POST_PER_PAGE)
    #针对用户查询所有考试
    @staticmethod
    def get_all_exam_by_user(user,page):
        return ExamInfo.objects.filter(creater=user.user_name).paginate(page=page,per_page=POST_PER_PAGE)

    #针对用户查询所在考试(历史考试)
    @staticmethod
    def get_user_exam_history(user,page):
        now_time = datetime.now()
        query = ExamInfo.objects.filter(end_time__lte=now_time)
        if user.user_level == 1:
            user_id = user.user_id
            query = query.filter(apply_num=user_id,is_hidden=0)
        else:
            query = query.filter(creater=user.user_name)
        return query.paginate(page=page,per_page=POST_PER_PAGE)

    #针对用户查询所在考试(正在进行)
    @staticmethod
    def get_user_exam_during(user,page):
        now_time = datetime.now()
        query = ExamInfo.objects.filter(start_time__lte=now_time,end_time__gte=now_time)
        if user.user_level == 1:
            user_id = user.user_id
            query = query.filter(apply_num=user_id,is_hidden=0)
        else:
            query = query.filter(creater=user.user_name)
        return query.paginate(page=page,per_page=POST_PER_PAGE)

    #根据id获取单个考试详细信息
    @staticmethod
    def get_exam_detail_info(exam_id):
        return ExamInfo.objects.filter(id=exam_id).first()

    #根据id获取参与该考试的成员信息
    @staticmethod
    def get_apply_num_by_id(exam_id):
        return ExamInfo.objects.filter(id=exam_id).first().apply_num

    #根据id获取该考试中的题库情况
    @staticmethod
    def get_prolbem_list_by_id(exam_id):
        return ExamInfo.objects.filter(id=exam_id).first().problem_list

    #根据id获取该考试中的各题型题数和出题情况
    @staticmethod
    def get_problem_condition_dict_byid(exam_id):
        dic = {}
        exam = ExamInfo.objects.filter(id=exam_id).first()
        dic['choice'] = exam.choice
        dic['blank'] = exam.blank
        dic['short_answer'] = exam.answer
        dic['is_random'] = exam.is_random
        return dic

    #添加考试
    @staticmethod
    def add_exam(exam_info):
        exam = ExamInfo()
        exam.name = exam_info.name.data
        exam.during_time = int(exam_info.during_time.data)
        exam.creater = exam_info.creater.data
        exam.describe = exam_info.describe.data
        exam.count = exam_info.count.data
        exam.start_time = datetime.strptime(exam_info.start_time.data,'%Y-%m-%d %H:%M:%S')
        exam.end_time = datetime.strptime(exam_info.end_time.data,'%Y-%m-%d %H:%M:%S')
        exam.is_register = exam_info.is_register.data
        if exam.is_register == 1:                                                                                       #若开放注册则添加注册时间信息
            exam.reg_start_time = datetime.strptime(exam_info.reg_start_time.data,'%Y-%m-%d %H:%M:%S')
            exam.reg_end_time = datetime.strptime(exam_info.reg_end_time.data,'%Y-%m-%d %H:%M:%S')
        exam.is_register = exam_info.is_register.data
        exam.is_hidden = exam_info.is_hidden.data
        exam.is_show_result = exam_info.is_show_result.data
        exam.save()

    #添加单个考试成员
    @staticmethod
    def add_exam_member_single(exam_id,member_id):
        exam = ExamInfo.objects.filter(id=exam_id).first()

        if not ExamConditionInfo.objects.filter(exam_id=exam_id, student_id=member_id).first():
            exam_condition = ExamConditionInfo()
            exam_condition.exam_id = exam_id
            exam_condition.student_id = member_id
            exam_condition.save()
        exam.apply_num.append(member_id)
        exam.save()

    #添加单个题目到考试题库
    @staticmethod
    def add_exam_problem_single(exam_id,problem_id):
        exam = ExamInfo.objects.filter(id=exam_id).first()
        exam.problem_list.append(problem_id)
        exam.save()

    #批量添加考题
    @staticmethod
    def add_exam_problem_by_list(exam_id,problem_list):
        exam = ExamInfo.objects.filter(id=exam_id).first()
        for problem in problem_list:
            exam.problem_list.append(problem.pid)
        exam.save()

    # 批量添加考试成员
    @staticmethod
    def add_exam_member_by_list(exam_id,user_list):
        exam = ExamInfo.objects.filter(id=exam_id).first()
        for user in user_list:
            #添加用户-考试关系
            if not ExamConditionInfo.objects.filter(exam_id=exam_id, student_id=user.user_id).first():
                exam_condition = ExamConditionInfo()
                exam_condition.exam_id = exam_id
                exam_condition.student_id = user.user_id
                exam_condition.save()
            exam.apply_num.append(user.user_id)
        exam.save()

    #更新考试信息
    @staticmethod
    def update_exam(exam_info,exam_id):
        exam = ExamInfo.objects.filter(id=exam_id).first()
        exam.name = exam_info.name.data
        exam.describe = exam_info.describe.data
        exam.count = exam_info.count.data
        exam.during_time = exam_info.during_time.data
        exam.start_time = exam_info.start_time.data
        exam.end_time = exam_info.end_time.data
        exam.creater = exam_info.creater.data
        if exam.is_register == 1:                                                                                       #若开放注册则添加注册时间信息
            exam.reg_start_time = datetime.strptime(exam_info.reg_start_time.data,'%Y-%m-%d %H:%M:%S')
            exam.reg_end_time = datetime.strptime(exam_info.reg_end_time.data,'%Y-%m-%d %H:%M:%S')
        exam.is_register = exam_info.is_register.data
        exam.is_hidden = exam_info.is_hidden.data
        exam.is_show_result = exam_info.is_show_result.data
        exam.save()

    #更新考题情况(各题型数量以及分值)
    @staticmethod
    def update_problem_number(problem_num,exam_id):
        exam = ExamInfo.objects.filter(id=exam_id).first()
        exam.choice['num'] = int(problem_num.choice_num.data)
        exam.blank['num'] = int(problem_num.blank_num.data)
        exam.answer['num'] = int(problem_num.short_answer_num.data)
        exam.choice['score'] = int(problem_num.choice_score.data)
        exam.blank['score'] = int(problem_num.blank_score.data)
        exam.answer['score'] = int(problem_num.short_answer_score.data)
        exam.is_random = problem_num.is_random.data
        exam.save()

    #保存样例试题
    @staticmethod
    def update_problem_list_example(list,exam_id):
        exam = ExamInfo.objects.filter(id=exam_id).first()
        exam.problem_list_example = list
        exam.save()

    #删除考试
    @staticmethod
    def del_exam(exam_id):
        ExamInfo.objects.filter(id=exam_id).delete()
        ExamConditionInfo.objects.filter(exam_id=exam_id).delete()

    #按id删除单个考试成员
    @staticmethod
    def del_exam_member(exam_id,user_id):
        exam = ExamInfo.objects.filter(id=exam_id).first()
        exam.apply_num.remove(user_id)
        exam.save()

    #按id删除单个考题
    @staticmethod
    def del_exam_problem(exam_id,problem_id):
        exam = ExamInfo.objects.filter(id=exam_id).first()
        exam.problem_list.remove(problem_id)
        exam.save()
