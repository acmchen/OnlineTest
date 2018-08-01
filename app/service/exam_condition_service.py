# -*- coding: utf-8 -*-
from app.models import ExamInfo,ExamConditionInfo,MyAnswer,LogInfo
from datetime import datetime
from bson import ObjectId
import json
class ExamConditionService(object):

    # 查询用户考试关系表中用户参加某场考试的次数
    @staticmethod
    def get_user_exam_count(exam_id, user_id):
        exam_condition = ExamConditionInfo.objects.filter(exam_id=exam_id, student_id=user_id).first()
        if exam_condition:
            return len(exam_condition.my_answer)
        return 0

    # 查询用户考试关系表中用户参加的所有考试的'参加次数'和'最后一场考试的结束时间'(返回字典)
    @staticmethod
    def get_user_exam_count_all(user_id):
        dic = {}
        exam_condition = ExamConditionInfo.objects.filter(student_id=user_id).all()
        for con in exam_condition:
            #检测考试记录长度,即考试次数,若考试次数不为0那么取最新一次考试的结束时间
            #用于做考试列表中,用户参与考试但中途退出的时间提示,以及保证count数(考试场次的正确行)
            if len(con.my_answer)!=0:
                page = json.loads(con.my_answer[-1].page)
                dic[ObjectId(con.exam_id)]=\
                    {'count':len(con.my_answer),'end_time':page['end_time'],'now_time':page['now_time']}
            else :
            #time为-1表示用户还没有参加过该考试,此时count数必然为0
                dic[ObjectId(con.exam_id)] = \
                    {'count': len(con.my_answer), 'end_time': -1,'now_time':-1}
        print dic
        return dic

    # 查询第count场考试答题答案情况
    @staticmethod
    def get_user_exam_answer(exam_id, user_id, count):
        exam_condition = ExamConditionInfo.objects.filter(exam_id=exam_id, student_id=user_id).first()
        return exam_condition.my_answer[count].answer

    # 查询第count场考试的结束时间戳
    @staticmethod
    def get_user_exam_page(exam_id, user_id, count):
        exam_condition = ExamConditionInfo.objects.filter(exam_id=exam_id, student_id=user_id).first()
        page = json.loads(exam_condition.my_answer[count].page)
        return page

    # 按考试id查询所有成员考试情况
    @staticmethod
    def get_user_exam_condition_by_examid(exam_id):
        return ExamConditionInfo.objects.filter(exam_id=exam_id).all()

    # 按用户id和考试id查询所有考试情况
    @staticmethod
    def get_user_exam_condition_by_userid(exam_id,user_id):
        return ExamConditionInfo.objects.filter(exam_id=exam_id,student_id=user_id).first()

    # 按用户id和考试id获取考试题目和答案
    @staticmethod
    def get_page(exam_id,student_id,count):
        exam_condition = ExamConditionInfo.objects.filter(exam_id=exam_id, student_id=student_id).first()
        return exam_condition.my_answer[count].page,exam_condition.my_answer[count].answer

    #生成用户-考试关系(考试管理添加成员时)
    @staticmethod
    def add_user_exam_condition(exam_id,user_id):
        if not ExamConditionInfo.objects.filter(exam_id=exam_id, student_id=user_id).first():
            exam_condition = ExamConditionInfo()
            exam_condition.exam_id = exam_id
            exam_condition.student_id = user_id
            exam_condition.my_answer = []
            exam_condition.save()

    #更新用户-考试关系(进入考试时)
    @staticmethod
    def update_exam_condition_begin(exam_id,user_id,login_ip):
        #ExamConditionInfo表(登入时间,登入ip)
        exam_condition = ExamConditionInfo.objects.filter(exam_id=exam_id, student_id=user_id).first()
        loginfo = LogInfo()
        loginfo.login_time = datetime.now()
        loginfo.logout_time = None
        loginfo.ip = login_ip
        exam_condition.log_info.append(loginfo)
        exam_condition.save()
        #ExamInfo表(添加实际参加考试用户)
        exam_info = ExamInfo.objects.filter(id=exam_id).first()
        if user_id not in exam_info.exam_num:
            exam_info.exam_num.append(user_id)
        exam_info.save()
    #保存答案
    @staticmethod
    def save_page(exam_id,user_id,page_dict,answer_dict,count):
        exam_condition = ExamConditionInfo.objects.filter(exam_id=exam_id,student_id=user_id).first()
        if count > len(exam_condition.my_answer)-1: #count是当前下标,len-1对应最大下标.如果大于最大下标则需append
            myanswer =  MyAnswer()
            myanswer.index = count
            myanswer.page = page_dict
            myanswer.subtime = datetime.now()
            myanswer.answer = {}
            exam_condition.my_answer.append(myanswer)
        else:
            exam_condition.my_answer[count].answer = answer_dict
            exam_condition.my_answer[count].subtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        exam_condition.save()

    #更新考试情况(退出考试时)退出时间，ip更新,now_time更新
    @staticmethod
    def update_exam_condition(exam_id,user_id,ip,count_ans):
        exam_condition = ExamConditionInfo.objects.filter(exam_id=exam_id,student_id=user_id).first()
        count_log = len(exam_condition.log_info)-1
        exam_condition.log_info[count_log].ip = ip
        exam_condition.log_info[count_log].logout_time = datetime.now()
        pagejson = json.loads(exam_condition.my_answer[count_ans].page)
        pagejson['now_time'] = pagejson['end_time'] + 10
        exam_condition.my_answer[count_ans].page = json.dumps(pagejson)
        exam_condition.save()
    #更新考试成绩
    @staticmethod
    def update_user_exam_grade(exam_id,user_id,grade,count):
        exam_condition = ExamConditionInfo.objects.filter(exam_id=exam_id, student_id=user_id).first()
        exam_condition.my_answer[count].grade = grade
        exam_condition.save()