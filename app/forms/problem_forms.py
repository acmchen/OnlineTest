# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField,HiddenField
from wtforms.validators import DataRequired
#考题筛选查询表单
class ProblemSearchForms(FlaskForm):
    book = SelectField("Book",choices=[('0', u'不选择')],render_kw={'id':'book','onchange':'firstlevel_Click()'})
    unit = SelectField("Unit", choices=[('0', u'不选择')], render_kw={'id': 'unit','onchange':'secondlevel_Click()'})
    section = SelectField("Section",choices=[('0',u'不选择')],render_kw={'id':'section'})
    subject = StringField("Subject")
    type = SelectField("Type",choices=[('0',u'全部'),('1',u'选择题'),('2',u'填空题'),('3',u'简答题')])
    level = SelectField("Level",choices=[('0','default')])
    submit = SubmitField("Search")

    def to_dict(self):
        return {
            'book':self.book.data,
            'unit':self.unit.data,
            'section':self.section.data,
            'subject':self.subject.data,
            'type':self.type.data,
            'level':self.level.data
        }

#考题添加表单
class ProblemAddForms(FlaskForm):

    type = SelectField("*Type", validators=[DataRequired()], choices=[('1', u'选择题')])
    desc_main = TextAreaField("*Description main",description=u'该题目的题干',validators=[DataRequired()])
    desc_other = TextAreaField("Description other",description=u'对于题干的额外补充内容,如选择题的选项,选项请用\"#$\"组合分开')
    answer = TextAreaField("*Answer",validators=[DataRequired()])
    author = StringField("Author", validators=[])
    tips = TextAreaField("Tips", validators=[])
    tags = StringField("Tags", validators=[])

    subject = StringField("Subject",description=u'请规范的填写改题目所属课程名',validators=[])
    level = SelectField("*Level",choices=[('0','default')],validators=[DataRequired()])
    book = SelectField("Book", choices=[('0', u'不选择')], render_kw={'id': 'book', 'onchange': 'firstlevel_Click()'},validators=[DataRequired()])
    unit = SelectField("Unit", choices=[('0', u'不选择')],
                       render_kw={'id': 'unit', 'onchange': 'secondlevel_Click()'})
    section = SelectField("Section", choices=[('0', u'不选择')], render_kw={'id': 'section'})
    status = SelectField("*Status",validators=[DataRequired()],choices=[('0',u'禁用'),('1',u'启用')])
    submit = SubmitField("Submit")

#考题更新表单
class ProblemUpdateForms(FlaskForm):
    type = SelectField("Type", validators=[DataRequired()], choices=[('1', u'选择题')])
    desc_main = TextAreaField("Description main", description=u'该题目的题干', validators=[DataRequired()])
    desc_other = TextAreaField("Description other", description=u'对于题干的额外补充内容,如选择题的选项,选项请用\'/\'号分开')
    answer = TextAreaField("Answer", validators=[DataRequired()])
    author = StringField("Author", validators=[])
    tips = TextAreaField("Tips", validators=[])
    tags = StringField("Tags", validators=[])

    subject = StringField("Subject", description=u'请规范的填写改题目所属课程名', validators=[])
    level = SelectField("Level", choices=[('0', 'default')], validators=[DataRequired()])
    b_book_id = HiddenField(validators=[DataRequired()])
    b_book = StringField("Book",render_kw={'readonly':'true'})
    book = SelectField("update to",choices=[('0', u'不选择')], render_kw={'id': 'book', 'onchange': 'firstlevel_Click()'},
                       validators=[DataRequired()],description=u'若课本不做选择默认为无改动,有关书本的所有信息依旧为原信息.但课本一旦有新的选择则全部刷新')
    b_unit_id = HiddenField(validators=[DataRequired()])
    b_unit = StringField("Unit",render_kw={'readonly':'true'})
    unit = SelectField("update to",choices=[('0', u'不选择')],
                       render_kw={'id': 'unit', 'onchange': 'secondlevel_Click()'})
    b_section_id = HiddenField(validators=[DataRequired()])
    b_section = StringField("Section",render_kw={'readonly':'true'})
    section = SelectField("update to",choices=[('0', u'不选择')], render_kw={'id': 'section'})
    status = SelectField("Status", validators=[DataRequired()], choices=[('0', u'禁用'), ('1', u'启用')])
    submit = SubmitField("Submit")