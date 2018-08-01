# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

#书籍查询表单(右侧工具栏)
class BookSearchForm(FlaskForm):
    bookname = StringField("BookName",validators=[])
    subject = StringField("Subject",validators=[])
    submit = SubmitField("Search")

    def to_dict(self):
        return {
            'bookname':self.bookname.data,
            'subject':self.subject.data
        }
#章添加表单(右侧工具栏)
class UnitAddForm(FlaskForm):
    bookid = StringField(render_kw={'readonly':'true'})
    unitname = StringField("SectionName",validators=[DataRequired()],render_kw={'placeholder':u'第x章 xxx'})
    submitunit = SubmitField("Add")
#节添加表单(右侧工具栏)
class SectionAddForm(FlaskForm):
    unitid = SelectField("SectionList",validators=[DataRequired()])
    sectionname = StringField("UnitName",validators=[DataRequired()],render_kw={'placeholder':u'第x节 xxx'})
    submitsection = SubmitField("Add")
#书籍更新、添加表单
class BookUpdateForm(FlaskForm):
    book_name = StringField("*BookName",validators=[DataRequired(message="Please enter book name")],
                            render_kw={'required':'true'})
    version = StringField("Version",render_kw={'placeholder':u'例如:第1版(版号请用阿拉伯数字)'})
    author = StringField("Author")
    publisher = StringField("Publisher")
    publish_time = StringField("PublishTime")
    subject = StringField("*Subject",validators=[DataRequired(message="Please enter subject")],render_kw={'required':'true'})
    submit = SubmitField("Submit")
