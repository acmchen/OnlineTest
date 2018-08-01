# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired,NumberRange
#考试查询表单
class ExamSearchForm(FlaskForm):
    name = StringField("ExamName",validators=[])
    creater = StringField("Creater",validators=[])
    start_time = StringField("StartTime",validators=[])
    end_time = StringField("EndTime",validators=[])
    is_register = SelectField("IsRegister",validators=[],choices=[('0',u'不启用'),('1',u'启用')],default='0')
    is_hidden = SelectField("IsHidden",validators=[],choices=[('0',u'开放'),('1',u'隐藏')],default='0')
    submit = SubmitField("Search")

    def to_dict(self):
        return {
            'name':self.name.data,
            'creater':self.creater.data,
            'start_time':self.start_time.data,
            'end_time':self.end_time.data,
            'is_register':self.is_register.data,
            'is_hidden':self.is_hidden.data
        }
#考试更新、添加表单
class ExamUpdateForm(FlaskForm):
    name = StringField("ExamName",validators=[DataRequired()],render_kw={'required':'true'})
    creater = StringField("CreaterName",validators=[DataRequired()])
    describe = TextAreaField("Describe",validators=[])
    count = IntegerField("ExamCount",validators=[DataRequired(),NumberRange(min=-1,max=10)],default=1,
                         description=u"此处为可考试次数,目前可输入范围为-1~10.1-10为可用范围即可重复考次数,-1为可一直重复考试(尽量不要使用)")
    during_time = StringField("DuringTime(min)",validators=[DataRequired()])
    start_time = StringField("StartTime",validators=[DataRequired()],render_kw={'required':'true'})
    end_time = StringField("EndTime",validators=[DataRequired()],render_kw={'required':'true'})
    reg_start_time = StringField("RegisterStartTime", validators=[])
    reg_end_time = StringField("RegisterEndTime", validators=[])
    is_register = SelectField("IsRegister",validators=[DataRequired()],choices=[('0',u'关闭注册'),('1',u'开放注册')])
    is_hidden = SelectField("IsHidden",validators=[DataRequired()],choices=[('0',u'开放'),('1',u'隐藏')],default=1)
    is_show_result = SelectField("IsShowResult",validators=[DataRequired()],choices=[('0',u'不显示'),('1',u'显示')])

    submit = SubmitField("Submit")
#下列两个表单并不是关系表的查询,是添加学生和试题时方便添加用的查询表单
#考试-学生查询表单
class ExamStudentSearchForm(FlaskForm):
    username = StringField("Username")
    nickname = StringField("Nickname")
    college = StringField("College")
    major = StringField("Major")
    grade = StringField("Grade")
    classnum = StringField("ClassNum")
    level = SelectField("level", validators=[DataRequired()],
                        choices=[('0', u'全部'), ('1', u'学生'), ('2', u'教师'), ('3', u'管理员')],
                        default='0')
    submit = SubmitField("Search")
    submit_add = SubmitField("AddAll")

    def to_dict(self):
        return {
            'username': self.username.data,
            'nickname': self.nickname.data,
            'college': self.college.data,
            'major': self.major.data,
            'grade': self.grade.data,
            'classnum': self.classnum.data,
            'level':self.level.data
        }

#考试-题目查询表单
class ExamProblemSearchForm(FlaskForm):
    book = SelectField("Book",choices=[('0', u'不选择')],render_kw={'id':'booklevel','onchange':'firstlevel_Click()'})
    unit = SelectField("Unit", choices=[('0', u'不选择')], render_kw={'id': 'unitlevel','onchange':'secondlevel_Click()'})
    section = SelectField("Section",choices=[('0',u'不选择')],render_kw={'id':'sectionlevel'})
    subject = StringField("Subject")
    type = SelectField("Type",choices=[('0',u'全部'),('1',u'选择题')])
    level = SelectField("Level",choices=[('0','default')])
    submit = SubmitField("Search")
    submit_add = SubmitField("AddAll")

    def to_dict(self):
        return {
            'book':self.book.data,
            'unit':self.unit.data,
            'section':self.section.data,
            'subject':self.subject.data,
            'type':self.type.data,
            'level':self.level.data
        }

#考试分值与题目数量设置表单
class ExamProblemNumForm(FlaskForm):
    choice_num = SelectField(u"选择题(数量/分值)", choices=[])
    choice_score = StringField()
    blank_num = SelectField(u"填空题(数量/分值)", choices=[])
    blank_score = StringField()
    short_answer_num = SelectField(u"简答题(数量/分值)", choices=[])
    short_answer_score = StringField()
    is_random = SelectField("IsRandom", validators=[DataRequired()], choices=[('0', u'不随机'), ('1', u'随机')])
    submit = SubmitField("Save")
