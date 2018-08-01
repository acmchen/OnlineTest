# -*- coding: utf-8 -*-
from app.models import ProblemInfo
from app.extensions import dbs
from datetime import datetime

import uuid
import copy
POST_PER_PAGE = 1
class ProLibService(object):
	#按条件分页查询题库中题目信息
	@staticmethod
	def search_problem_info(proinfo,page):
		query = ProblemInfo.query
		if proinfo.has_key('subject') and proinfo['subject']:
			query = query.filter(ProblemInfo.subject.like('%'+proinfo['subject']+'%'))
		if proinfo.has_key('book') and proinfo['book']!='0':
			query = query.filter_by(belong_to_book=proinfo['book'])
		if proinfo.has_key('unit') and proinfo['unit']!='0':
			query = query.filter_by(belong_to_unit=proinfo['unit'])
		if proinfo.has_key('section') and proinfo['section']!='0':
			query = query.filter_by(belong_to_section=proinfo['section'])
		if proinfo.has_key('type') and proinfo['type']!='0':
			query = query.filter_by(type=proinfo['type'])
		pagination = query.paginate(page,per_page=POST_PER_PAGE,error_out=False)
		return pagination
	#不分页条件查询题目信息，用于批量添加到考试
	@staticmethod
	def search_problem_info_nopage(proinfo):
		query = ProblemInfo.query
		if proinfo.has_key('subject') and proinfo['subject']:
			query = query.filter(ProblemInfo.subject.like('%'+proinfo['subject']+'%'))
		if proinfo.has_key('book') and proinfo['book']!='0':
			query = query.filter_by(belong_to_book=proinfo['book'])
		if proinfo.has_key('unit') and proinfo['unit']!='0':
			query = query.filter_by(belong_to_unit=proinfo['unit'])
		if proinfo.has_key('section') and proinfo['section']!='0':
			query = query.filter_by(belong_to_section=proinfo['section'])
		if proinfo.has_key('type') and proinfo['type']!='0':
			query = query.filter_by(type=proinfo['type'])

		return query.all()
	#根据id获取题目的详细信息
	@staticmethod
	def get_problem_detailed_info(pid):
		pro_detailed_info = copy.deepcopy(ProblemInfo.query.filter_by(pid = pid).first())
		return pro_detailed_info
	#分页查询所有题目信息
	@staticmethod
	def get_all_problems(page):
		return ProblemInfo.query.paginate(page,POST_PER_PAGE,error_out=False)
	#添加题目
	@staticmethod
	def add_problem(proinfo):
		problem = ProblemInfo()
		problem.pid = str(uuid.uuid1())
		problem.date = str(datetime.now())
		problem.type = proinfo.type.data
		problem.desc_main = proinfo.desc_main.data
		problem.desc_other = proinfo.desc_other.data
		problem.author = proinfo.author.data
		problem.answer = proinfo.answer.data
		problem.tips = proinfo.tips.data
		problem.tags = proinfo.tags.data
		problem.belong_to_book = proinfo.book.data
		problem.belong_to_unit = proinfo.unit.data
		problem.belong_to_section = proinfo.section.data
		problem.subject = proinfo.subject.data
		problem.level = proinfo.level.data
		problem.status = proinfo.status.data
		dbs.session.add(problem)
		dbs.session.commit()
	#更新题目
	@staticmethod
	def update_problem(proinfo,pid):
		problem = ProblemInfo.query.filter_by(pid=pid).first()
		problem.type = proinfo.type.data
		problem.desc_main = proinfo.desc_main.data
		problem.desc_other = proinfo.desc_other.data
		problem.author = proinfo.author.data
		problem.answer = proinfo.answer.data
		problem.tips = proinfo.tips.data
		problem.tags = proinfo.tags.data
		problem.belong_to_book = proinfo.book.data
		problem.belong_to_unit = proinfo.unit.data
		problem.belong_to_section = proinfo.section.data
		problem.subject = proinfo.subject.data
		problem.level = proinfo.level.data
		problem.status = proinfo.status.data
		dbs.session.commit()
	#删除题目
	@staticmethod
	def del_problem(pid):
		pid = ProblemInfo.query.filter_by(pid=pid).first()
		dbs.session.delete(pid)
		dbs.session.commit()
